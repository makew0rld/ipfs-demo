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
app.config['SECRET_KEY'] = "demosocketkey"
app.config
socketio = SocketIO(app)


@app.route("/")
def mainpage():

    print(":: rendered homepage")
    return render_template("home.html")

# The client sends a "success" message once it has connected
@socketio.on("success")
def on_success(message):
    ipfs = ""  # IPFS ref to file that IPNS address points to
    # Now the client is connected, the IPNS polling can begin
    print(":: Started update loop")
    while True:
        # Hardcoded demo key, from the key file included in the repo
        ipfs2 = subprocess.run(["ipfs", "name", "resolve", "QmbfT8139rgMeKZdLDgz45zQQVzCuKnHRtzohuT5aqcRV8"],
                               stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        print(":: Resolved to:", ipfs2)
        # If the file has changed
        if ipfs != ipfs2:
            ipfs = ipfs2
            print(":: Updated the ipfs var")
            # Tell the client - it will update the iframe img with the new url
            emit("update", {"data": ipfs}, broadcast=True)
            print(":: Told the client")
        sleep(2)


if __name__ == '__main__':
    socketio.run(app)  # Runs the production eventlet server unless in dev mode
