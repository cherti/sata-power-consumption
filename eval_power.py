#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt

if 'hidpi' in sys.argv[2:]:
	# for hidpi-displays, play around with the 75
	import matplotlib as mpl
	mpl.rcParams['figure.dpi'] = 75

folder = sys.argv[1] if len(sys.argv) >= 2 else 'power_consumption_measurement_data'

sh = np.loadtxt(folder + '/sact_hipm')*1e-6
sd = np.loadtxt(folder + '/sact_dipm')*1e-6
ah = np.loadtxt(folder + '/aact_hipm')*1e-6
ad = np.loadtxt(folder + '/aact_dipm')*1e-6
nh = np.loadtxt(folder + '/nact_hipm')*1e-6
nd = np.loadtxt(folder + '/nact_dipm')*1e-6

# if we have med_power available...
sm, am, nm = None, None, None
smed, amed, nmed = None, None, None
try:
	sm = np.loadtxt(folder + '/sact_medp')*1e-6
	am = np.loadtxt(folder + '/aact_medp')*1e-6
	nm = np.loadtxt(folder + '/nact_medp')*1e-6
	smed = np.loadtxt(folder + '/sact_mipm')*1e-6
	amed = np.loadtxt(folder + '/aact_mipm')*1e-6
	nmed = np.loadtxt(folder + '/nact_mipm')*1e-6
except:
	pass


t = np.linspace(0, (len(sh)-1)*3, len(sh))

def plot_all():
	plt.plot(t, ah, 'r-.', label='async/HIPM')
	plt.plot(t, ad, 'k-.', label='async/DIPM')
	plt.plot(t, sh, 'r--', label='sync/HIPM')
	plt.plot(t, sd, 'k--', label='sync/DIPM')
	plt.plot(t, nh, 'r-', label='idle/HIPM')
	plt.plot(t, nd, 'k-', label='idle/DIPM')

	if med_power_avail:
		plt.plot(t, am, 'b-.', label='async/med_power')
		plt.plot(t, sm, 'b--', label='sync/med_power')
		plt.plot(t, nm, 'b-', label='idle/med_power')

	plt.legend()
	plt.xlabel('time [s]')
	plt.ylabel('power consumption [W]')


def plot_by_mode(title, hipm, dipm, med=None, med_with_dipm=None, filename=None):
	plt.plot(t, ah, 'r', label='max_performance')
	plt.plot(t, ad, 'k', label='min_power')
	if med is not None:
		plt.plot(t, med, 'b', label='medium_power')
	if med_with_dipm is not None:
		plt.plot(t, med_with_dipm, 'g', label='med_power_with_dipm')

	plt.title(title)
	plt.legend()
	plt.xlabel('time [s]')
	plt.ylabel('power consumption [W]')
	if filename:
		plt.savefig(filename)
	else:
		plt.show()


plot_by_mode('idle, no disk activity', nh, nd, nmed, nm)
plot_by_mode('activity asynchronous to measurement', ah, ad, amed, am)
plot_by_mode('activity synchronous to measurement', sh, sd, smed, sm)
