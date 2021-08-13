import flask
import mongoengine
from flask import Flask, make_response, request
from flask_pymongo import PyMongo


import json
from bson.objectid import ObjectId

app = Flask(__name__)


app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://localhost/hospitols'
}
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/hospitols")
db = mongodb_client.db



def newEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__



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


