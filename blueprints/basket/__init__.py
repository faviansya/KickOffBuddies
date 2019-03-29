from blueprints import db
from flask_restful import fields


class Basket(db.Model):

    __tablename__ = 'basket'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer)
    pemain_id = db.Column(db.Integer)
    pebisnis_id = db.Column(db.Integer)
    pemain_name = db.Column(db.String(100))
    pebisnis_name = db.Column(db.String(100))

    response_field = {
        'id': fields.Integer,
        'booking_id': fields.Integer,
        'pemain_id': fields.Integer,
        'pebisnis_id': fields.Integer,
        'pemain_name': fields.String,
        'pebisnis_name': fields.String,
    }

    def __init__(self, id, booking_id, pemain_id,pebisnis_id,pemain_name,pebisnis_name):
        self.id = id
        self.booking_id = booking_id
        self.pemain_id = pemain_id
        self.pebisnis_id = pebisnis_id
        self.pemain_name = pemain_name
        self.pebisnis_name = pebisnis_name

    def __repr__(self):
        return '<%r>' % self.id