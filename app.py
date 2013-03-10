import hashlib
import json
import pymongo
from bson import json_util

from flask import Flask, render_template, request, Response

DOMAIN = "http://commonsfeed.us"

app = Flask(__name__)

connection = pymongo.MongoClient()
db = connection.commonsfeed
users = db.users

def dump_obj(obj):
    return json.dumps(obj, default=json_util.default)

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

@app.route('/wiki/<filename>')
def show(filename):
    data = {
            "current_url": DOMAIN + request.path,
            "commons_url": make_commons_url(filename),
            "display_title": make_display_name(filename),
            "image_url": make_image_url(filename)
            }
    return render_template("shim.html", **data)

@app.route('/user', methods=['POST'])
def add_user():
    commons_username = request.form['commons_username']
    facebook_userid = request.form['facebook_userid']
    data = {
        'commons_username': commons_username, 
        'facebook_userid': facebook_userid
    }
    db.users.insert(data)

    return Response(dump_obj(data), mimetype="application/json")

@app.route('/user/<fb_userid>')
def show_user(fb_userid):
    user = db.users.find_one({'facebook_userid': fb_userid})
    if user:
        return Response(dump_obj(user), mimetype="application/json")
    else:
        return Response({}, mimetype="application/json") #FIXME: Be a nice HTTP citizen, mkay?

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
