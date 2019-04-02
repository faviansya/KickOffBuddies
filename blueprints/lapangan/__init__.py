from blueprints import db
from flask_restful import fields

class Lapangan(db.Model):

    __tablename__ = 'lapangan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pebisnis = db.Column(db.Integer)
    jenis_lapangan = db.Column(db.String(100))
    url_image = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    jumlah_user_rating = db.Column(db.Integer)

    response_field = {
        'id': fields.Integer,
        'id_pebisnis': fields.Integer,
        'jenis_lapangan': fields.String,
        'url_image' : fields.String,
        'rating': fields.Integer,
        'jumlah_user_rating': fields.Integer,
    }

    def __init__(self, id, id_pebisnis, jenis_lapangan, url_image, rating, jumlah_user_rating):
        self.id = id
        self.id_pebisnis = id_pebisnis
        self.jenis_lapangan = jenis_lapangan
        self.url_image = url_image
        self.rating = rating
        self.jumlah_user_rating = jumlah_user_rating

    def __repr__(self):
        return '<Lapangan %r>' % self.id

