# Measuring the effect of SATA power link management onto your battery life

Results gathered with this code can be seen [here](https://insanity.industries/post/sata-power-consumption/).

## Introduction

This is a project to evaluate the impact of SATA power link management onto the battery life of your laptop.
Experiments on my own machines yielded a reduced power consumption by a, for my tastes, significant margin (up to 30% reduced consumption with screen turned off) for one device.
Therefore I'm interested to have a more gerenal assesment of this effect.

Available power link management policies for SATA-devices are

  * `max_performance`
  * `min_power`
  * `medium_power`
  * `med_power_with_dipm` since Linux 4.15

If you want to help out by contributing measurement data, the instructions to do so are listed below.
<strike>Once the data is collected and evaluated, I'll link the writeup where the data will be analyzed and how you can use that for your own benefit here in the README, besides other places.</strike> [Go here to see results.](https://insanity.industries/post/sata-power-consumption/).


## Contributing data

To contribute data, you first need a laptop

  * running linux
  * housing an SSD<sup>1</sup> via SATA (aka shows up as `/dev/sd...`)
  * having at least ~3h of battery life

<sup>1) HDDs are not really of interest for this measurement as the power link management policy would also imply spindowns and therefore the performance impact would be too significant to be of practical use. Nevertheless, you could use the measurement-script for this as well, of course. For this dataset, however, I'm only interested in SSD-data.</sup>

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

## Data collected

For clarity, this is a list of data that will be collected and is contained in the `tar.gz`-file:

  * power consumption measurement data for the three different policies + the name of the source file for the power consumption in `/sys`
  * throughput measurement data<sup>2</sup>
  * measurement parameters (time, number of datapoints etc.)
  * disk model (both the human readable name you give it and what the model calls itself<sup>3</sup>


<sup>2) Beware that this data is *not* suited for judging the actual performance of the disk and the measurement type is *not* tailored towards measuring the performance of the disk, but merely to trigger some activity. For measuring the performance impact of the different policies, use a dedicated benchmarking tool such as for example [fio](https://github.com/axboe/fio).</sup>

<sup>3) As some disk models have specified quite useless information in their readable model-parameter, the script asks you to name the disk model yourself, although this seems redundant in the first moment. It's just a precautionary measure. Don't worry too much if you don't know the exact name of the model. For example if it came with the machine, just specify something like `came with laptop <laptop model name>`. :)</sup>
