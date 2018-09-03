#!/usr/bin/python3

from flask import Flask, render_template
import subprocess
from flask_socketio import SocketIO, emit
from time import sleep

# TODO - Plan:
# Have a site with a iframe that leads to a /file url that displays an img
# /file pulls from the :8080 gateway, using an already known file
# Use socketIO to have the server tell the browser when to refresh the iframe
# In the background, the server is resolving the IPNS hash constantly, to see
# if it changes. If it does, that is when it sends the broadcast

app = Flask(__name__, template_folder=".")
app.config['SECRET_KEY'] = "nohackplzitsjustademoiknowitsopensourcebutcomeonman"
app.config
socketio = SocketIO(app)

ipfs = ""  # IPFS ref to file that IPNS address points to

@app.route("/")
def mainpage():
    return render_template("home.html")

# The client sends a "success" message once it has connected
@socketio.on("success")
def on_success(message):
    global ipfs
    # Now the client is connected, the IPNS polling can begin
    while True:
        # Hardcoded demo key, from the key file included in the repo
        ipfs2 = subprocess.run(["ipfs", "name", "resolve", "QmbfT8139rgMeKZdLDgz45zQQVzCuKnHRtzohuT5aqcRV8"],
                               stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        # If the file has changed
        if ipfs != ipfs2:
            ipfs = ipfs2
            # Tell the client - it will update the iframe img
            emit("update", "update", broadcast=True)
        sleep(1)


if __name__ == '__main__':
    socketio.run(app)  # Runs the production eventlet server unless in dev mode
