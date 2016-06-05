# web app for monitoring the rider status

import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, redirect, make_response, request, url_for
from flask_socketio import SocketIO, emit
from threading import Thread
from time import sleep
import glob, os, re, psutil
import datetime

#from rider_status import read_tts_state

app = Flask(__name__)

socketio = SocketIO(app, async_mode='eventlet')

PROCNAME = "gm2"

@app.route('/')
def home():
    return render_template('status.html', midas_file_nums=range(1,2), art_file_nums=range(1,2), analysis_file_nums=range(1,2), log_file_nums=range(1,2), proc_nums=range(1,3))


def emit_status():
    while True:
        sleep(1)
        for i in range(1,2):
            newest1 = max(glob.iglob('/home/g2muon/data.slac/run*mid'), key=os.path.getctime)
            size1 = os.path.getsize(newest1) >> 20
	    socketio.emit('get status', {'ftype': 1, 'name': newest1, 'num': i, 'stat' : size1})
        
	for i in range(1,2):
            newest2 = max(glob.iglob('/data1/slac2016/art/gm2slac_*art'), key=os.path.getctime)
            size2 = os.path.getsize(newest2) >> 20
            socketio.emit('get status', {'ftype': 2, 'name': newest2, 'num': i, 'stat' : size2})
        
	for i in range(1,2):
            newest3 = max(glob.iglob('/data1/slac2016/analysis/gm2slac_*root'), key=os.path.getctime)
            size3 = os.path.getsize(newest3) >> 20
            socketio.emit('get status', {'ftype': 3, 'name': newest3, 'num': i, 'stat' : size3})
        
	for i in range(1,2):
            newestlog = max(glob.iglob('/data1/slac2016/log/gm2slac_*log'), key=os.path.getctime)
            report = 0
	    with open(newestlog) as f:
            	for line in f:
            		if "Events total" in line:
             			report = line
	    socketio.emit('get status', {'ftype': 4, 'name': newestlog, 'num': i, 'stat' : report})

        iproc = 1 
	for p in psutil.process_iter():
            if p.name() == PROCNAME and p.parent().cmdline()[0] == '/bin/bash':
		print p.parent().cmdline()
                if(len(p.parent().cmdline()) == 4):
			newestproc = p.parent().cmdline()[3]
                if(len(p.parent().cmdline()) == 3):
			newestproc = p.parent().cmdline()[2]
                socketio.emit('get status', {'ftype': 5, 'name': p.cmdline()[4], 'num': iproc, 'stat' : newestproc})
                iproc += 1
    


if __name__ == '__main__':
    emitting_thread = Thread(name='emittingthread', target=emit_status)
    emitting_thread.start()
    socketio.run(app, port=4000, host="0.0.0.0")
