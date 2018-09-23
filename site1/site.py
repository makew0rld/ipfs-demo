#!/usr/bin/python3

from flask import Flask, render_template, flash, request, redirect
from werkzeug.utils import secure_filename
import os
import subprocess
import eventlet

app = Flask(__name__, template_folder=".")

# Setup file uploading
UPLOAD_FOLDER = "/tmp/ipfs-demo"  # Linux specific
ALLOWED_EXTENSIONS = set(["jpg", "png", "jpeg", "gif"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Max file size is 16 MB
# XXX - was causing Too Large errors with files within the limit
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Mainpage
# XXX: will this work with /demo on nginx?
@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)  # Redirect back to upload page
        file = request.files['file']
        # If user does not select file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Secure the filename by removing slashes, etc.
            filename = secure_filename(file.filename)
            # Save it
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filepath)
            file.save(filepath)
            # Add to IPFS
            # strip() is used because the output ends in \n
            hash = subprocess.run(["ipfs", "add", "-Q", "--pin=false", filepath],
                                  stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
            # IPNS publish
            # Takes a long time unless pubsub is enabled, or you are in an
            # isolated system, ie the demo environment
            subprocess.run(
                ["ipfs", "name", "publish", "--key=demo", hash])

            return redirect("done")  # Show them the successful upload page
    # Return the webpage, they are not uploading
    return render_template("home.html")


# Successful upload page
@app.route("/done")
def done():
    return render_template("done.html")


if __name__ == '__main__':
    app.run(port=6001)
    # XXX production code
    #eventlet.wsgi.server(eventlet.listen(("/demo", 80)), app)
