import os
from flask import Flask, request, Response, jsonify
from functools import wraps


# Custom error handler. Raise this exception
# to return a status_code, message, and body
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


print(__name__)

app = Flask(__name__)

# set the default error handler
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(debug=True)

# dummy users
USERS = [
    {'id': 0, 'first': 'Joe', 'last': 'Bloggs',
        'email': 'joe@bloggs.com', 'role': 'student', 'active': True},
    {'id': 1, 'first': 'Ben', 'last': 'Bitdiddle',
        'email': 'ben@cuny.edu', 'role': 'student', 'active': True},
    {'id': 2, 'first': 'Alissa P', 'last': 'Hacker',
        'email': 'missalissa@cuny.edu', 'role': 'professor', 'active': True},
]

# Your code here...
# E.g.,

# Problem 1
@app.route("/users",methods=["GET"])
def get_users():
    return jsonify(USERS)
    
# Problem 2
@app.route("/users/<int:id>",method=["GET"])
def get_user_id(id):
    for user in USERS:
        if user['id']==id:
            return jsonify(user)
        abort(404)
                         

# Problem 3
@app.route("/Users",method=["POST"])
def add_user():
    req_data=request.get_json()
    if "first" not in req_data.keys():
        return Response(status=422)
    if "last" not in req_data.keys():
        return Response(status=422)
    if "email" not in req_data.keys():
        return Response(status=422)
    if "role" not in req_data.keys():
        return Response(status=422)
    
    # add users
    req_data["id"]=len(USERS)
    req_data["active"]=True
    USERS.append(req_data)
    return Response(status=201)
    
# Problem 4
@app.route("/users/<int:id>",method=["PATCH","PUT"])
def update_user(id):
    for user in USERS:
        if user['id']==id:
            req_data=request.get_json()
            for k in req_data.keys():
                if k == "first" or k == "last" or k == "email" or k== "role":
                    user[k] =req_data[k]
                else:
                    return Response(status=422)
                return jsonify(user)
            return Response(status=404)

# Problem 5
@app.route("/users/<int:id>/deactivate",method=["POST"])
def deactivate_user(id):
    for user in USERS:
        if user['id']==id:
            user['active']=False
            return jsonif(user)
        abort(404)