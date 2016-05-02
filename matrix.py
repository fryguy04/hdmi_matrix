#!/usr/bin/python

from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
import socket
import sys
from sets import Set
import time

# Flask serves hdmi.html from 'static/hdmi.html' ... below redirect / requests here to make it even easier
# That page lets you select HDMI Inputs/Outputs and does a GET request to /video
# /video is served by flask (below), parses the GET request into HDMI Serial commands then
# connects via Socket to Global Cache (GC100) on port 4999 which translates IP to ASCII SERIAL
# Works well with browser or iPhone

# VARIABLES
HOST = '192.168.0.70'	# GC100 IP
PORT = 4999

# Below as formatted by hdmi.html GET Form submission
OUTPUTS = {'family rm':1, 'bedroom':2, 'kitchen':3, 'basement':4}
INPUTS  = {'comcast':1, 'bluray':2, 'apple tv':3, 'computer':4}

# HDMI Inputs:
# 1 Comcast
# 2 Blueray
# 3 AppleTV
# 4 Computer

# HDMI Outputs:
# 1 Family Rm
# 2 Kitchen
# 3 Bedroom
# 4 Basement


app = Flask(__name__)

@app.route('/')
def buttons():
    return send_from_directory('static','hdmi.html') 
    #return render_template('index.html') 
	

	
@app.route('/video')
def video():
	outputs = request.args.get('column1').split(',')	# Outputs
	input   = request.args.get('column2')               # Input ... only should be one!
	
	#print outputs
	#print input
	
	outsFormatted  = Set()
	cmds = []
	
	for x in outputs:
		outsFormatted.add(str(OUTPUTS[x]))
		
	inFormatted = str(INPUTS[input])
	
	for out in outsFormatted:
		cmds.append(out+inFormatted)
	
	print "** ", cmds
	for cmd in cmds:
		sendHdmiCmd(cmd)
		#time.sleep(1)
	
	return "commands: ", str(cmds)


# cmd examples: 
#  XXYY where XX is Output, YY is Inputs
#  23 - Have AppleTV(3) display on Kitchen(2) TV
def sendHdmiCmd(cmd):
	global HOST, PORT
	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.sendall(str(cmd) + "\r")
	response = s.recv(24) #This is the echo back from iTach
	print "Response from send():", response
	s.close()
	
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
