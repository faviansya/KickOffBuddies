from blueprints import db
from flask_restful import fields


class PlayerList(db.Model):

    __tablename__ = 'playerlist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer)
    pemain_id = db.Column(db.Integer)
    pemain_name = db.Column(db.String(100))

    response_field = {
        'id': fields.Integer,
        'booking_id': fields.Integer,
        'pemain_id': fields.Integer,
        'pemain_name': fields.String,
    }

    def __init__(self, id, booking_id, pemain_id,pemain_name):
        self.id = id
        self.booking_id = booking_id
        self.pemain_id = pemain_id
        self.pemain_name = pemain_name

    def __repr__(self):
        return '<%r>' % self.id