# Measuring the effect of SATA power link management onto your battery life

## Introduction

This is a project to evaluate the impact of SATA power link management onto the battery life of your laptop.
Experiments on my own machine yielded a reduced power consumption by a significant margin (up to 30% reduced consumption excluding the screen) for one device.
Therefore I'm interested to have a more gerenal assesment of this effect.

Available power link management policies for SATA-devices are

  * `max_performance`
  * `min_power`
  * `med_power_with_dipm` since Linux 4.15

If you want to help out by contributing measurement data, the instructions to do so are listed below.
Once the data is collected and evaluated, I'll link the writeup where the data will be analyzed and how you can use that for your own benefit here in the README, besides other places.


## Contributing data

To contribute data, you first need a laptop

  * running linux
  * housing an SSD via SATA (aka shows up as `/dev/sd...`)
  * having at least ~3h of battery life

Then do the following:

  1. Clone this repository.
  2. Unplug your computer from your charger, such that it runs on battery.
  3. Run the Python-script in this repo *as root* (because we need to write some system APIs).
  4. Follow the instructions and leave the laptop alone (especially don't touch mouse or keyboard as this will wake up the screen again, compromising the measurement).
  5. Once done, there will be a `tar.gz`-file containing the data. Send this to me, please. :)

As the measurement (intentionally) takes some time (~3h), to gather enough data to reduce the impact of system services waking up and consuming power etc. onto the overall measurement, the procedure is best run overnight.

The script will attempt to disable your screen to eliminate one of the major power consumers of your laptop.
It will attempt to wake it up again at the end of the measurement, however, it might be that your system thinks otherwise as the screen was also due to be turned off due to inactivity.
If the system is long overdue it's specified measurement time, you can check, but please redo the measurement if the measurement wasn't actually stopped to keep our datasets clean. :)

If you run it overnight and want to suspend your laptop after the measurement if finished, you could run it like

    python3 measure_power_consumption.py; systemctl suspend

if run in a rootshell, if run with sudo, it would look like

    sudo python3 measure_power_consumption.py; systemctl suspend

Thanks for helping out!

## Visualizing the results

If you want to see yourself how the power consumption of your disk behaves, you can use `eval_power.py` in this repo.

To use it, ensure that you have all dependencies for `eval_power.py` installed:

  * `python3-numpy`
  * `python3-matplotlib`

Then `eval_power.py` should visualise the measured data when run inside the repository root.
