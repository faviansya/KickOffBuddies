from blueprints import db
from flask_restful import fields


class Pemain(db.Model):

    __tablename__ = 'pemain'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    response_field = {
        'id': fields.Integer,
        'password': fields.String,
        'username': fields.String,

    }

    def __init__(self, username, password, name, urlimage, alamat, status, level,transaction,kota):
        self.username = username
        self.password = password


    def __repr__(self):
        return '<Pemain %r>' % self.id

