##!/usr/bin/env python
# -*- coding: utf-8 -*- 

import subprocess
from subprocess import check_output
import string
import uuid
import shutil
import os, os.path
from os import path
import cherrypy
from os import listdir
from os.path import isfile, join

cherrypy.config.update({'server.socket_host':'0.0.0.0'}) #hs
#cherrypy.config.update({'server.socket_host':'10.0.1.17'}) #hs
#cherrypy.config.update({'server.socket_host':'192.168.178.67'}) #fhfl
#cherrypy.config.update({'server.socket_host':'192.168.178.167'}) #@home
cherrypy.config.update({'server.socket_port': 8080}) 
pics_path = "/home/pi/CherryServer/docs/"
screen_timer = 11;
lamp_color = "green"

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
	pics = []
	pics.extend(sorted(os.listdir(pics_path)))
	html_string = ''	
        html_string += """<html>
          <head>
		<link id="themecss" href="/static/css/style.css" rel="stylesheet" type="text/css" />
	  </head>
          <body>
	    <form action="/del_pic" method="GET">
		<div class="picbox">"""
	for i in pics:
		html_string += """<div class="picdiv"><img src="docs/%s" />
			 <input type="checkbox" name="pics" value="%s"></input>
       		         <h3>%s</h3>
		         </div> """ % (i, i, i)
		
	html_string +="""	
	      </div>
	        <div class="buttons">
		<div class="circles-parent">
                   <div class="circle" style="background: %s;"></div>
                </div>
		<input class="delete_button" type= "submit" name="pics" value="Delete selected"/>
		</form>
		<form class="add_form" action="add_pic" method='post' enctype='multipart/form-data'>
		  <input type='file' class="inputfile" id="uploader" name='jpgFile'/>
              	  <input class="add_button" type="submit" value="Upload" />
            	</form>

		<form class="update_button" action="update_fbi">
                  <button type="submit">Start</button>
                </form>

		<form class="stop_button" action="stop_fbi">
                  <button type="submit">Stop</button>
                </form>

		<form class="shutdown_button" action="shutdown_pi">
                  <button type="submit">Shutdown</button>
                </form>
		<form class="reboot_button" action="reboot_pi">
                  <button type="submit">Reboot</button>
                </form>
		<form class="timer_form" action="set_timer" method="post">
		  <input type="number" class="timer_box" name="time" value = "%s">
		  <button class="timer_button" type="submit">Set timer</button>
		</form>
	      </div>
          </body>
          </html>""" % (lamp_color, screen_timer)

	return html_string
	
    @cherrypy.config(**{'response.timeout': 3600})  # default is 300s
    @cherrypy.expose()
    def add_pic(self, jpgFile):
        if not jpgFile.filename.endswith('/'):
	        try:
        	    _tmpfilename = jpgFile.filename.split('/')[-1:][0]
	        except (IndexError, AttributeError):
        	    _tmpfilename = 'undefined_name_{}.jpg'.format(uuid.uuid4())
	        try:
	            _tmpfilename = jpgFile.filename.split('\\')[-1:][0]
	        except (IndexError, AttributeError):
	            _tmpfilename = 'undefined_name_{}.jpg'.format(uuid.uuid4())

        	_CONFIRMATIONPATH = pics_path

	        _destination = path.join(_CONFIRMATIONPATH, _tmpfilename)
		
		if not _destination.endswith('/'):
	        	with open(_destination, 'wb') as f:
		            shutil.copyfileobj(jpgFile.file, f)
        self.return_to_main()	

    @cherrypy.expose
    def del_pic(self, **kwargs):
       if kwargs.get("pics"):
	  for pic in kwargs.get("pics"):
	      path = os.path.join("docs", pic).encode("utf-8")
   	      os.system("rm %s" %path)
       self.return_to_main()

    @cherrypy.expose
    def update_fbi(self):
	os.system("fbi -d /dev/fb0 -T 2 -noverbose -t 5 /home/pi/CherryServer/docs/*.jpg")
	global lamp_color
	lamp_color = "green"
	self.return_to_main()
	
    @cherrypy.expose
    def set_timer(self, time):
        global screen_timer
	screen_timer = time
        self.return_to_main()

    @cherrypy.expose
    def stop_fbi(self):
	global lamp_color
	lamp_color = "red"
	os.system("killall fbi")
       	self.return_to_main()

    @cherrypy.expose
    def shutdown_pi(self):
        os.system("shutdown now -h")

    @cherrypy.expose
    def reboot_pi(self):
        os.system("reboot")

    def return_to_main(self):
	raise cherrypy.HTTPRedirect("/")
   
if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '/home/pi/CherryServer/public'
        },
	'/docs':{
	  'tools.staticdir.on': True,
	  'tools.staticdir.dir': '/home/pi/CherryServer/docs'
	}
    }

os.system("fbi -d /dev/fb0 -T 2 -noverbose -t 5 /home/pi/CherryServer/docs/*.jpg")
cherrypy.quickstart(StringGenerator(), '/', conf)
#raise cherrypy.HTTPRedirect("/update_fbi")
