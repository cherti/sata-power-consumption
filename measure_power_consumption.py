#!/usr/bin/env python3

datap = 300   # number of measurement points
timestep = 3  # seconds
convergence_time = 600  # time to wait until power consumption converges


import subprocess, time, os, sys, re

target_dir = 'power_consumption_measurement_data'
halfstep = timestep/2
activity_command = 'echo {} >> throughput.log && dd if=/dev/zero of=testfile bs=1M count=1 conv=fdatasync >> throughput.log 2>&1'
power_consumption_file = '/sys/class/power_supply/BAT0/power_now'


def sanatize_blkdev(blkdev):
	# sanatize, just in case
	blkdev = blkdev.split("/")[-1]
	for i in range(10):
		blkdev = blkdev.replace(str(i), "")
	return blkdev

def get_host(blkdev):
	lsout = subprocess.getoutput("ls -l /sys/block/{}".format(blkdev))
	for part in lsout.split('/'):
		if re.match('^host[0-9]+$', part):
			return part

	return None

# get information from user
print(" :: Hi, thanks for participating in this research!")
print("    Please give some information beforehand to make data evaluation easier.")

disk_name_human = input(" Disk model, if known [unknown]: ") or 'unknown'
blockdevice     = sanatize_blkdev(input(" SATA-device to measure [sda]: ") or 'sda')

scsi_host = get_host(blockdevice)

if not scsi_host:
	print("Error getting device node, cannot proceed, sorry. :(", file=sys.stderr)
	exit(1)

target_disk_policy_file = '/sys/class/scsi_host/{}/link_power_management_policy'.format(scsi_host)


def set_policy(pol, polfile):
	with open(polfile, 'w') as f:
		print(pol, file=f)

	# check if policy was set
	with open(polfile, 'r') as f:
		if f.read().strip() != pol:
			raise ValueError("Unable to set policy")


# test if we can write to the policy-file
try:
	set_policy('max_performance', target_disk_policy_file)
except PermissionError:
	print(' ! Script must be run as root, otherwise we cannot switch SATA power management policies.', file=sys.stderr)
	print(' ! Please run as root. If you did and it still failed, please contact the author. Thanks!', file=sys.stderr)
	exit(2)


# test if we can read power consumption
with open(power_consumption_file, 'r') as f:
	if f.read().strip() == "0":
		print(' ! Error reading power consumption. Have you unplugged your charger?', file=sys.stderr)
		exit(3)


print(' :: estimated runtime:', round((4*3*datap*timestep + 4*convergence_time)/60, 2), 'min')
print(' :: The screen will be turned off to save power, please turn of wifi and other things')
print('    that could consume power to keep the measurements as clean as possible. Thanks!')
print('    Please do not use the computer until the measurement has finished')

input('Press enter when ready to start the measurement.')


def measure_without_activity():
	perfdata = []
	for _ in range(datap):
		with open(power_consumption_file) as f:
			perfdata.append(f.read())
		time.sleep(timestep)

	return perfdata


def measure_with_activity_sync():
	perfdata = []
	cmd = activity_command.format('sync')
	for _ in range(datap):
		subprocess.call(cmd, shell=True)
		with open(power_consumption_file) as f:
			perfdata.append(f.read())
		time.sleep(timestep)

	return perfdata


def measure_with_activity_async():
	perfdata = []
	cmd = activity_command.format('async')
	for _ in range(datap):
		subprocess.call(cmd, shell=True)
		time.sleep(halfstep)
		with open(power_consumption_file) as f:
			perfdata.append(f.read())
		time.sleep(halfstep)

	return perfdata


# blank the screen
subprocess.call("xset dpms force off", shell=True)


# prepare data storage
os.makedirs(target_dir, exist_ok=True)
os.chdir(target_dir)

subprocess.call("touch throughput.log", shell=True)


### Do the measurement

set_policy('max_performance', target_disk_policy_file)
time.sleep(convergence_time)
hpdn = measure_without_activity()
hpds = measure_with_activity_async()
hpda = measure_with_activity_sync()

set_policy('min_power', target_disk_policy_file)
time.sleep(convergence_time)
lpdn = measure_without_activity()
lpds = measure_with_activity_async()
lpda = measure_with_activity_sync()

set_policy('medium_power', target_disk_policy_file)
time.sleep(convergence_time)
mpdn = measure_without_activity()
mpds = measure_with_activity_async()
mpda = measure_with_activity_sync()

try:
	set_policy('med_power_with_dipm', target_disk_policy_file)
	time.sleep(convergence_time)
	medn = measure_without_activity()
	meds = measure_with_activity_async()
	meda = measure_with_activity_sync()
except ValueError:
	# might simply be a kernel too old for med_power
	pass


# save data
def save_data(fname, data):
	with open(fname, 'w') as f:
		print(''.join(data), file=f)


save_data('nact_hipm', hpdn)
save_data('nact_dipm', lpdn)
save_data('nact_medp', medn)
save_data('sact_hipm', hpds)
save_data('sact_dipm', lpds)
save_data('sact_medp', meds)
save_data('aact_hipm', hpda)
save_data('aact_dipm', lpda)
save_data('aact_medp', meda)
save_data('nact_mipm', mpdn)
save_data('sact_mipm', mpds)
save_data('aact_mipm', mpda)

device_model = "unknown"
try:
	with open('/sys/block/{}/device/model'.format(blockdevice), 'r') as f:
		device_model = f.read().strip()
except:
	pass


with open('parameters', 'w') as f:
	print("datapoints:", datap, file=f)
	print("timestep:", timestep, file=f)
	print("convergence_time:", convergence_time, file=f)
	print("power_source:", power_consumption_file, file=f)
	print("disk_name_human:", disk_name_human, file=f)
	print("disk_model:", device_model, file=f)

os.chdir('..')

# pack it up
try:
	subprocess.call(['tar', '-czf', 'powerconsumption.tar.gz', target_dir])
except:
	pass


subprocess.call("xset dpms force on", shell=True)
print("Thank you for participating in this study!")
print("Please send the file powerconsumption.tar.gz to cherti-sammelt{}letopolis.de".format(chr(64)))
print("or get it to me on any other way.")
