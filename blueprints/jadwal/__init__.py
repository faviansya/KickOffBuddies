from blueprints import db
from flask_restful import fields

class Jadwal(db.Model):

    __tablename__ = 'jadwal'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pebisnis = db.Column(db.Integer)
    id_lapangan = db.Column(db.Integer)
    jam = db.Column(db.String(100))
    tanggal = db.Column(db.String(100))

    response_field = {
        'id': fields.Integer,
        'id_pebisnis': fields.Integer,
        'id_lapangan': fields.Integer,
        'jam' : fields.String,
        'tanggal' : fields.String,
    }

    def __init__(self, id, id_pebisnis, id_lapangan, jam, tanggal):
        self.id = id
        self.id_pebisnis = id_pebisnis
        self.id_lapangan = id_lapangan
        self.jam = jam
        self.tanggal = tanggal

    def __repr__(self):
        return '<Lapangan %r>' % self.id

