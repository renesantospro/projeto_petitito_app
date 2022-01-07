#!/home/rene/anaconda3/bin/python

from flask import Flask, jsonify, request, render_template, redirect, url_for
import json, os, signal, psutil
from webbrowser import open

global ip
ip = '127.0.0.1'
global port
port = 5000    
url = ip + ':' + str(port)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reset')
def reset():
    return redirect(url_for('home'))

@app.route('/shut_down', methods=['GET'])
def shut_down():
    os.kill(os.getpid(), signal.SIGINT)
    # return  jsonify({ "success": True, "message": "Server is shutting down..." })

if __name__ == '__main__':
    open(url, new=2)
    app.debug = True
    app.run(host = ip, port = port)

processes = []

def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    for i in range( len(list(psutil.process_iter(["name", "exe", "cmdline"])))):
        p = list(psutil.process_iter(["name", "exe", "cmdline"]))
        if len(p[i].info['cmdline']) > 0 and p[i].info['cmdline'][0].endswith(name) == True:
                processes.append([list(psutil.process_iter())[i].pid, list(psutil.process_iter())[i].name(), p[i].info['cmdline'][0]])
            
def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=True,
                   timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callback function which is
    called as soon as a child terminates.
    """
    assert pid != os.getpid(), "won't kill myself"
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        try:
            p.send_signal(sig)
        except psutil.NoSuchProcess:
            pass
    gone, alive = psutil.wait_procs(children, timeout=timeout,
                                    callback=on_terminate)

find_procs_by_name('firefox')

kill_proc_tree(processes[0][0])