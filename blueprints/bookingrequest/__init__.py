from blueprints import db
from flask_restful import fields

class BookingRequest(db.Model):

    __tablename__ = 'booking request'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer)
    sport = db.Column(db.String(50))
    player = db.Column(db.Integer)
    time = db.Column(db.String(50))
    location = db.Column(db.Text)
    compound = db.Column(db.Text)
    vicinity = db.Column(db.Text)
    status = db.Column(db.String(50))
    url_image = db.Column(db.String(1000))
    pemain_saat_ini = db.Column(db.Integer)

    response_field = {
        'id': fields.Integer,
        'id_user': fields.Integer,
        'sport': fields.String,
        'player': fields.Integer,
        'time' : fields.String,
        'location' : fields.String,
        'compound' : fields.String,
        'vicinity' : fields.String,
        'status' : fields.String,
        'url_image' : fields.String,
        'pemain_saat_ini': fields.Integer,
    }

    def __init__(self, id, id_user, sport, player, time, location, compound, vicinity, status,url_image, pemain_saat_ini):
        self.id = id
        self.id_user = id_user
        self.sport = sport
        self.player = player
        self.time = time
        self.location = location
        self.compound = compound
        self.vicinity = vicinity
        self.status = status
        self.url_image = url_image
        self.pemain_saat_ini = pemain_saat_ini

    def __repr__(self):
        return '<Booking Request %r>' % self.id

