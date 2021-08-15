import os
import flask
import mongoengine
from flask import Flask, make_response, request, flash, url_for, send_from_directory
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename, redirect

import json
from bson.objectid import ObjectId

app = Flask(__name__)

# DB config
app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://localhost/hospitols'
}
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/hospitols")
db = mongodb_client.db

# Upload function variables
UPLOAD_FOLDER = '/home/mattrank/Desktop/PhotosRepo'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def newEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route("/hospital/<state>")
def get_Hospital_input(state):
    state_req = request.args.get('state')
    hospitals = db.hosp_info.find({"state": state})
    return json.dumps([hospital for hospital in hospitals], default=newEncoder )

@app.route("/hospital")
def get_Hospital_req():
    state_req = request.args.get('state')
    hospitals = db.hosp_info.find({"state": state_req})
    return json.dumps([hospital for hospital in hospitals], default=newEncoder )

@app.route("/hospital-test")
def get_Hospital_req_test():
    all_req = request.args.get()
    hospitals = db.hosp_info.find({all_req: all_req})
    return json.dumps([hospital for hospital in hospitals], default=newEncoder )


@app.route("/user", methods=['post'])
def add_one_user():
    user_body = request.get_json()
    print(user_body['name'])
    db.users.insert_one({'name': user_body['name'], 'phone': user_body['phone']})
    return flask.jsonify(message="success")


@app.route("/user", methods=['get'])
def find_one_user():
    name_req = request.args
    print(name_req['name'])
    if name_req["phone"] is None:
        user = db.users.find_one({"name": name_req['name']})
        return json.dumps(user, default=newEncoder)

    else:
        user = db.users.find_one({"phone": name_req['phone']})
        return json.dumps(user, default=newEncoder)


@app.route("/add_one_hospital")
def add_one_hospital():
    db.hosp_info.insert_one({'provider_id': "000003", 'body': "todo two"})
    return flask.jsonify(message="success")




if __name__ == '__main__':
    app.run()


