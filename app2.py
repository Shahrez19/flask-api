#!flask/bin/python
from flask import Flask,jsonify, render_template
from flask import Blueprint
# from flask_paginate import Pagination, get_page_parameter
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

app = Flask(__name__)


file_path = os.path.abspath(os.getcwd())+"\database.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))


@app.route("/patient/<int:page_num>")
def patient(page_num):
    patients = Patient.query.paginate(per_page=20,page=page_num,error_out=True)
    return render_template('patient.html',patients=patients)

@app.route("/patient")
def index():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM person")
    data = cur.fetchmany(20)
    return render_template('patient.html',data=data)

# Get methods
# @app.route('/todo/api/v1.0/<int:task_id>',methods=['GET'])
# def get_tasks(task_id):
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'tasks':task[0]})

# Post Methods
# @app.route("/todo/api/v1.0/tasks", methods=['POST'])
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': task}), 201

    

# Error Message
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error':'Not found'}),404)


# Start the program here
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
