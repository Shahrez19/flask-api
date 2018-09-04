#!flask/bin/python
from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask import json
from flask_marshmallow import Marshmallow
from flask import abort
import os
import uuid
from datetime import date, datetime

app = Flask(__name__)

"Load datasource or data"
file_path = os.path.abspath(os.getcwd())+"/database.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class person(db.Model):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    dob = db.Column(db.String)
    gender = db.Column(db.String)
    status = db.Column(db.String)
    terms_accepted = db.Column(db.Integer)
    terms_accepted_at = db.Column(db.String)
    address_street = db.Column(db.String)
    address_city = db.Column(db.String)
    address_state = db.Column(db.String)
    address_zip = db.Column(db.String)
    phone = db.Column(db.String)

    def __init__(self,id,first_name,middle_name,last_name,email,dob):
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.dob =  dob

class personSchema(ma.ModelSchema):
    class Meta:
        model = person

json_file = open('person.json','r')
data = json.load(json_file)

@app.route('/', methods = ['GET'])
def get_all_users():
    output = []
    p =  person.query.all()
    person_schema = personSchema()
    for patient in p:
        info = person_schema.dump(patient).data
        age = calculate_age(datetime.strptime(info["dob"], "%Y-%m-%d"))
        info["age"] =  age
        if age >=8 :
            output.append(info)
    return jsonify(output)


@app.route('/<string:id>', methods = ['GET'])
def get_user(id):
    dat = person.query.filter_by(id = id).first()
    if dat:
        person_schema = personSchema()
        output = person_schema.dump(dat).data
        return jsonify(output)
    return jsonify({"message": "The patient was not found!"})

@app.route('/newpatient', methods = ['POST'])
def create_user():
    data =  request.get_json()
    uid = uuid.uuid4().hex[:8]
    new_patient = person(id =  uid, first_name = data["first_name"], middle_name =  data["middle_name"], last_name = data["last_name"], email = data["email"], dob = data["dob"])
    db.session.add(new_patient)
    db.session.commit() 
    return jsonify({'message': 'New User Created'})

@app.route('/updatepatient/<string:id>', methods = ['POST'])
def update_user(id):
    user = person.query.filter_by(id=id).first()

    if not user:
        return jsonify({"message": "The patient was not found!"})
    
    data = request.get_json()

    if data["dob"]:
        try:
            datetime.strptime(data["dob"], "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "Bad date of birth"})

    db.session.query(person).filter_by(id=id).update(data)
    db.session.commit()
    return jsonify({'message': 'Patient Updated!'})
 
@app.route('/deletepatient/<string:id>', methods = ['POST'])
def delele_user(id):
    patient =  person.query.filter_by(id=id).first()

    if not patient:
        return jsonify({"message": "No Patient Found!"})
    
    db.session.delete(patient)
    db.session.commit()

    return jsonify({"message": "The patient has been deleted!"})

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def bad_request():
    abort(404)

# Start the program here
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)