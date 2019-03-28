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
    status = db.Column(db.String(50))
    
    response_field = {
        'id': fields.Integer,
        'id_user': fields.Integer,
        'sport': fields.String,
        'player': fields.Integer,
        'time' : fields.String,
        'location' : fields.String,
        'status' : fields.String,
    }

    def __init__(self, id, id_user, sport, player, time, location, status):
        self.id = id
        self.id_user = id_user
        self.sport = sport
        self.player = player
        self.time = time
        self.location = location
        self.status = status

    def __repr__(self):
        return '<Booking Request %r>' % self.id
