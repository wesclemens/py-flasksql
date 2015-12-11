# http://flask-sqlalchemy.pocoo.org/
# ~150 test cases / ~1000 losc
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


#
# Setup / Config
#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/people_pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


#
# Database Setup
#
db = SQLAlchemy(app)


#
# Models
#
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(500), unique=True)


class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(50))


#
# Routes
#
@app.route("/")
def hello():
    user = db.session.query(User).filter_by(name="Will").first()
    return jsonify(id=user.id,
                   name=user.name,
                   email=user.email)


@app.route("/pets/<int:pet_id>")
def pets(pet_id):
    pet = Pet.query.filter_by(id=pet_id).first()
    return jsonify(id=pet.id,
                   type=pet.type,
                   name=pet.name)

if __name__ == "__main__":
        app.run(debug=True)
