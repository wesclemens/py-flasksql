# http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/
# No test cases
import sqlalchemy as sa

from flask import Flask, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#
# Setup /Config
#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/people_pets'


#
# Database Setup
#
engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                          convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


@app.teardown_appcontext
def shutdown_session(exception=None):
        db_session.remove()


#
# Models
#
class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), unique=True)
    email = sa.Column(sa.String(500), unique=True)


class Pet(Base):
    __tablename__ = 'pets'
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.String(50))
    name = sa.Column(sa.String(50))


#
# Routes
#
@app.route("/")
def hello():
    user = db_session.query(User).filter_by(name="Will").first()
    return jsonify(id=user.id,
                   name=user.name,
                   email=user.email)


@app.route("/pets/<int:pet_id>")
def pets(pet_id):
    pet = db_session.query(Pet).filter_by(id=pet_id).first()
    return jsonify(id=pet.id,
                   type=pet.type,
                   name=pet.name)

if __name__ == "__main__":
        app.run(debug=True)
