# reMarkable Sleep Screen Editor via HTML

***Use this script at your own risk!***

***This script uses dev mode to make changes to your device. Please enable dev mode and use at your own risk.***

Tested on a ***reMarkable Paper Pro v3.17.0.72***

When a reMarkable user selects to show their personal information on the sleep screen via the options at `settings>security>Personal Information` they can fill in `Name` and `Contact` info to be displayed on the sleep screen. 

These values gets stored on the device in a config file at `/data/xochitle.conf`. This script automates the editing of these values, so you don't have to manually go into the device to change them. 

This allows you to change the sleep screen by injecting limited HTML of your choice. For example, you can load a remote image to display on the device.  

This script will replace the contents of `/data/xochitl.conf` fields `IdleContact` and `IdleName` (if uncommented in the script),with the `-f` file you specify when running. I've included a basic HTML file for test. 

To run, clone the repo and chmod+x the python script, then:

```
./reMarkableSleepScreenEditor.py -i {reMarkableIPAddress} -f {htmlFile}
```

Or to rest the conf file fields to blank:

```
./reMarkableSleepScreenEditor.py -i {reMarkableIPAddress} --reset

```

See the blog post [https://pizzapower.org]([pizzapower.org](https://www.pizzapower.me/2025/02/06/remarkable-paper-pro-html-injection/)). 