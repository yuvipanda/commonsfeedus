from flask import Flask, render_template, request
import hashlib

DOMAIN = "http://commonsfeed.us"

app = Flask(__name__)

def make_image_url(filename):
    name = filename.replace("File:", "").replace(" ", "_")
    md5 = hashlib.md5(name).hexdigest()
    # FIXME
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/1500px-%s" % (md5[0], md5[0:2], name, name)

def make_display_name(filename):
    return ".".join(filename.replace("File:", "").replace("_", " ").split(".")[:-1])

def make_commons_url(filename):
    return "https://commons.wikimedia.org/wiki/File:%s" % (filename.replace("File:", ""), )

@app.route('/channel.html')
def fb_channel():
    return '<script src="//connect.facebook.net/en_US/all.js"></script>'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/file/<filename>')
def show(filename):
    data = {
            "current_url": DOMAIN + request.path,
            "commons_url": make_commons_url(filename),
            "display_title": make_display_name(filename),
            "image_url": make_image_url(filename)
            }
    return render_template("shim.html", **data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
