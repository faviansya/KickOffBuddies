from blueprints import db
from flask_restful import fields


class PlayerList(db.Model):

    __tablename__ = 'playerlist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer)
    pemain_id = db.Column(db.Integer)
    pemain_name = db.Column(db.String(1000))
    pemain_image = db.Column(db.String(1000))
    jumlah_pemain = db.Column(db.Integer)
    pemain_saat_ini = db.Column(db.Integer)
    
    response_field = {
        'id': fields.Integer,
        'booking_id': fields.Integer,
        'pemain_id': fields.Integer,
        'pemain_name': fields.String,
        'pemain_image': fields.String,
        'jumlah_pemain': fields.Integer,
        'pemain_saat_ini': fields.Integer,

    }

    def __init__(self, id, booking_id, pemain_id,pemain_name,pemain_image,jumlah_pemain,pemain_saat_ini):
        self.id = id
        self.booking_id = booking_id
        self.pemain_id = pemain_id
        self.pemain_name = pemain_name
        self.pemain_image = pemain_image
        self.jumlah_pemain = jumlah_pemain
        self.pemain_saat_ini = pemain_saat_ini

    def __repr__(self):
        return '<%r>' % self.id