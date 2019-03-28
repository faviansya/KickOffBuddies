from blueprints import db
from flask_restful import fields


class Pemain(db.Model):

    __tablename__ = 'pemain'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_no = db.Column(db.String(100))
    address = db.Column(db.String(100))
    favourite_sport= db.Column(db.String(100))
    user_type = db.Column(db.String(100))
    created_time = db.Column(db.String(100))

    response_field = {
        'id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'name': fields.String,
        'email': fields.String,
        'phone_no': fields.String,
        'address': fields.String,
        'favourite_sport': fields.String,
        'user_type': fields.String,
        'created_time': fields.String,

    }

    def __init__(self, username, password, name,email,phone_no,address,favourite_sport, user_type, created_time):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.phone_no = phone_no
        self.address = address
        self.favourite_sport = favourite_sport
        self.user_type = user_type
        self.created_time = created_time

    def __repr__(self):
        return '<Pemain %r>' % self.id