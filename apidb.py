import os
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
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

# initializer
def init_db():
    # create a global variable __db__ that you can use from route handlers
    global __db__
        
    # use in-memory database for debugging
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    __db__ = SQLAlchemy(app)
    engine = __db__.engine

    # put your database initialization statements here
    # create the users table
        
    table_stmnt = """create table USERS(
        id integer primary key, 
        first text not null, 
        last text not null,
        email text not null,
        role text not null,
        active blob not null
        );
        """
    engine.execute(table_stmnt)
    

    # insert each item from USERS list into the users table
    users = [
            (0, 'Joe', 'Bloggs', 'joe@bloggs.com', 'student', True),
            (1, 'Ben', 'Bitdiddle', 'ben@cuny.edu', 'student', True),
            (2, 'Alissa P', 'Hacker', 'missalissa@cuny.edu', 'professor', True)
        ]
    
    stmnt = """
    insert into USERS (id, first, last, email, role, active)
        values(?, ?, ?, ?, ?, ?)
        """
    for i in users:
        engine.execute(stmnt, *i)


if __name__ == 'apidb':
    
    # save database handle in module-level global
    init_db()
    app.run(debug=True)
        
# Problem 1, retrieve the whole table
@app.route("/users", methods=["GET"])
def get_users():
    
    engine = __db__.engine
    
    users = engine.execute("select * from USERS")
    
    lista = [dict(user) for user in users]
    
    return jsonify(lista)

# Problem 2, get an user by it's ID
@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    
    engine = __db__.engine
    
    stmnt = "select * from USERS where id == {}".format(str(id))
    
    users = engine.execute(stmnt)
    
    lista = [dict(user) for user in users]
    
    if len(lista) ==0:
        raise InvalidUsage(message='Error 404, id Not Found', status_code=404)
    
    return jsonify(lista[0]), 200

# Problem 3, create a new user
@app.route("/users", methods=["GET", "PATCH", "POST"])
def create_user():
    
    engine = __db__.engine
    
    users = engine.execute("select * from USERS")
    
    lista = [dict(user) for user in users]
    
    if 'first' in request.get_json() and 'last' in request.get_json() and 'email' in request.get_json() and 'role' in request.get_json():
        
        ids = int(lista[-1]['id']) + 1
        first = request.get_json().get('first')
        last = request.get_json().get('last')
        email = request.get_json().get('email')
        role = request.get_json().get('role')
        active = True
        
        insert_stmnt = """
insert into USERS (ids, first, last, email, role, active)
  values(?, ?, ?, ?, ?, ?)
"""
    
        user = [
        (ids, first, last, email, role, active)
    ]
    
        engine.execute(insert_stmnt, user[0])
    
        stmnt2 = "select * from USERS where id == {}".format(str(ids))
    
        user2 = dict(engine.execute(stmnt2))
    
        return jsonify(user2), 201
        
    if 'first' in request.get_json() and 'last' in request.get_json() and 'email' in request.get_json():
        
        ids = int(lista[-1]['id']) + 1
        first = request.get_json().get('first')
        last = request.get_json().get('last')
        email = request.get_json().get('email')
        role = "aaaa"
        active = 'True'
        
        insert_stmnt = """
        insert into USERS (id, first, last, email, role, active)
          values(?, ?, ?, ?, ?, ?)"""
    
        user = [
        (ids, first, last, email, role, active),
    ]
    
        engine.execute(insert_stmnt, user[0])
    
        stmnt2 = "select * from USERS where id == {}".format(str(ids))
    
        user2 = engine.execute(stmnt2)
        
        lista2 = [dict(usr) for usr in user2]
    
        return jsonify(lista2[0]), 201
    
    else:
        raise  InvalidUsage(message='Missing item', status_code=422)
        
        
# Problem 4, update an existing user
@app.route("/users/<id>", methods=["GET", "PATCH", "POST"])
def update_user(id):
    
    engine = __db__.engine
    
    stmnt = "select * from USERS where id == {}".format(str(id))
    
    users = engine.execute(stmnt)
    
    lista = [dict(user) for user in users]
    
    if len(lista) ==0:
        raise InvalidUsage(message='Error 404, id Not Found', status_code=404)
    
    if len(lista) !=0:
    
        if 'first' in request.get_json():
            first = request.get_json().get("first")
            update_stmnt = """
            update USERS 
            set first = ? 
            where id == ?
            """
            engine.execute(update_stmnt, first, str(id))
        
        if 'last' in request.get_json():
            last = request.get_json().get("last")
            update_stmnt = """
            update USERS 
            set last = ? 
            where id == ?
            """
            engine.execute(update_stmnt, last, str(id))
    
        if 'email' in request.get_json():
            email = request.get_json().get("email")
            update_stmnt = """
            update USERS 
            set email = ? 
            where id == ?
            """
            engine.execute(update_stmnt, email, str(id))
        
        if 'role' in request.get_json():
            role = request.get_json().get("role")            
            update_stmnt = """
            update USERS 
            set role = ? 
            where id == ?
            """
            engine.execute(update_stmnt, role, str(id))
            
        
        stmnt2 = "select * from USERS where id == {}".format(str(id))
    
        users2 = engine.execute(stmnt2)
    
        lista2 = [dict(usr) for usr in users2]
    
        return jsonify(lista2[0]), 200
    
    else:
        raise InvalidUsage(message='Error', status_code=422)

        
# Problem 5, user deactivation
@app.route("/users/<id>/deactivate", methods=["GET", "PUT", "POST"])
def deactivate_user(id):
    
    engine = __db__.engine
    
    stmnt = "select * from USERS where id == {}".format(str(id))
    
    user = engine.execute(stmnt)
    
    lista = [dict(usr) for usr in user]
    
    if len(lista) == 0:
        raise InvalidUsage(message='Error 404, id Not Found', status_code=404)
    
    stmnt2 = """
    update USERS
    set active == ?
    where id == ?
    """
    
    engine.execute(stmnt2, False, id)
    
    stmnt3 = "select * from USERS where id == {}".format(str(id))
    
    user2 = engine.execute(stmnt3)
    
    lista2 = [dict(usr2) for usr2 in user2]
    
    return jsonify(lista2[0]), 200
    
