# ~ CherryScreen v0.2 ~

This is my first python project: a simple InfoScreen tool for the use with a Raspberry PI and a HDMI Screen.

#### Reminder

Has been just lightly tested :)

#### Description

This application is used as a simplest digital information board (info screen for opening times, pending events or whatever). 
It is written in Python and uses the CherryPy framework and is controlled by a Web interface, reachable via local WiFi. 
The Images are displayed with the tool fbi, using framebuffer. Therefore no OS with a GUI is needed on the PI. 
Currently only .jpg format is enabled.
#### Components

- RasberryPi Zero or another PI, connected to WiFi successfully (and power of course :)
- Monitor or TV with HDMI output, connected to the PI
- SDCard for the PI. (For OS and the pictures) The size depends on the amount of pictures you want to display. 8 GB were enough for me.
- Any operation system installed on the SD card. (no need for a GUI!) I used [Linux raspberrypi 4.4] for the development.
- Python Framework with CherryPy support installed. My OS supports Python 2.7 and 3.4. I used CherryPy 10.2.2

#### Installation

    1. download unzip the folder on your PI under the default path /home/pi/CherryServer (or change paths in the console.py script manually)
    2. If you want to prepare some pictures, put them in programms docs/ folder in .jpg format
    3. (optional)Change the IP address of the PI (and the port if needed) on the first lines of the control.py script, e.g: 
       cherrypy.config.update({'server.socket_host':'192.1.1.111'}) (default: webserer starts at device's ip adress)
       cherrypy.config.update({'server.socket_port': 8080})
    4. start the control.py script as root in an own terminal session by 
       sudo python control.py
       or create a startup script
    5. The Web Interface is reachable at device startup in the local WiFi via the device's IP address, e.g.:  http://192.1.1.111:8080
    -> If it is not reachable, make sure any firewall isn't blocking (check out the port!)

#### ToDo  

- remove static paths
- clean up code
- switch to python3 convention
- use 'stringbuilder' array for html strings
- check out what happens if doc dir is empty and fbi is started
- disable timer, if only one picture is in the dir or timer is set to 0 (show only the first one?)
- enable support for more file formats
