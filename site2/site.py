#!/usr/bin/python3

from flask import Flask, render_template
import subprocess
from flask_socketio import SocketIO

app = Flask(__name__, template_folder=".")
app.config['SECRET_KEY'] = "demosocketkey"
app.config
socketio = SocketIO(app)


@app.route("/")
def mainpage():
    return render_template("home.html")


@socketio.on("update")
def update():
    print(":: Started update func")
    # Hardcoded demo key, from the key file included in the repo
    ipfs = subprocess.run(["ipfs", "name", "resolve", "QmbfT8139rgMeKZdLDgz45zQQVzCuKnHRtzohuT5aqcRV8"],
                          stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    # Tell the client - it will update the iframe img with the new url
    print(":: Told the client")
    return ipfs


if __name__ == '__main__':
    # Runs the production eventlet server unless in dev mode
    socketio.run(app, port=6002, debug=True)
