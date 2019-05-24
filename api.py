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
#@app.route("/users", methods=["GET"])


# Problem 1
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(USERS)

# Problem 2
@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    lista = [user for user in USERS if user['id']==int(id)]
    
    if len(lista) ==0:
        raise InvalidUsage(message='Error 404, id Not Found', status_code=404)
    
    return jsonify(lista[0]), 200
  
        
# Problem 3
@app.route("/users", methods=["POST"])
def create_user():

    if 'first' in request.get_json() and 'last' in request.get_json() and 'email' in request.get_json():
        user = {'id': USERS[-1]['id'] + 1,
                'first': request.get_json().get('first'),
                'last': request.get_json().get('last'),
                'email': request.get_json().get('email'),
                'role': request.get_json().get('role'),
                'active': True}

        USERS.append(user)
        return jsonify(user), 201
    else:
        raise  InvalidUsage(message='Missing item', status_code=422)

        

# Problem 4
@app.route("/users/<id>", methods=["PATCH", "POST"])
def update_user(id):
  
    lista = [user for user in USERS if user['id']==int(id)]
    
    if len(lista) == 0:
        raise InvalidUsage(message='User not Found', status_code=404)

    if len(lista) !=0:
        
        if 'first' in request.get_json():
            lista[0]['first'] = request.get_json().get('first')

        if 'last' in request.get_json():
            lista[0]['last'] = request.get_json().get('last')

        if 'email' in request.get_json():
            lista[0]['email'] = request.get_json().get('email')
        
        return jsonify(lista[0]), 200

    else:
        raise InvalidUsage(message='Error', status_code=422)


# Problem 5
@app.route("/users/<id>/deactivate", methods=["POST"])
def deactivate_user(id):

    lista = [user for user in USERS if user['id']==int(id)]

    if len(lista) == 0:
        raise InvalidUsage(message='User not Found', status_code=404)
    
    lista[0]['active']=False

    return jsonify(lista[0])

