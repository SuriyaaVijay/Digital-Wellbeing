# Digital-Wellbeing

This project aims to bring the digital wellbeing and screen time management features, similar to those found in Samsung Android phones, to Linux operating systems. The project is primarily built using HTML, JavaScript, and Python, with additional programming in Shell and CSS.

## Getting Started

**To start recording**

1. Clone the repository to some folder: `$ git clone https://github.com/SuriyaaVijay/Digital-Wellbeing.git`
2. If you're on Ubuntu, make sure you have the dependencies: `$ sudo apt-get install xdotool wmctrl`. On Fedora, you may also need `sudo yum install gnome-screensaver`.
3. `cd` inside and run `$ ./ulogme.sh` (note: this will ask you for sudo authentication which is required for `showkey` command). This will launch two scripts. One records the frequency of keystrokes and the other records active window titles. Both write their logs into log files in the `logs/` directory. Every log file is very simply just the unix time stamp followed by data, one per line.


**The user interface**

1. **Important**. As a one-time setup, copy over the example settings file to your own copy: `$ cp render/render_settings_example.js render/render_settings.js` to create your own `render_settings.js` settings file. In this file modify everything to your own preferences. Follow the provided example to specify title mappings: A raw window title comes in, and we match it against regular expressions to determine what type of activity it is. For example, the code would convert "Google Chrome - some cool website" into just "Google Chrome". Follow the provided example and read the comments for all settings in the file.
2. Once that's set up, start the web server viewer: `$ python ulogme_serve.py`, and go to to the provided address) for example `http://localhost:8123`) in your browser. Hit the refresh button on top right every time you'd like to refresh the results based on most recently recorded activity
3. If your data isn't loading, try to explicitly run `python export_events.py` and then hit refresh. This should only be an issue the very first time you run ulogme.
   
## Features

1. Screen Time Monitoring: Keep track of the time you spend on your Linux device and monitor your daily usage patterns. 
2. App Usage Statistics: Get detailed insights into the apps you use the most and how much time you spend on each app.
3. App Limits: Set limits on the usage of specific applications to encourage a healthy balance between screen time and other activities. 
4. Usage History: View your historical data to track your progress and make informed decisions about your digital habits.
5. User Profiles: Create individual profiles for different users to personalize their digital wellbeing settings.
