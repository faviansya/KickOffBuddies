import random, logging
from blueprints import db
from flask_restful import fields


class AcceptedBooking(db.Model):
    __tablename__ = "acceptedBooking"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pemain_id = db.Column(db.Integer)
    pemain_name = db.Column(db.String(500))
    pemain_url_image = db.Column(db.String(500))
    booking_location = db.Column(db.String(500))
    sport = db.Column(db.String(500))
    sport_image = db.Column(db.String(500))
    player_amount = db.Column(db.Integer)
    marker = db.Column(db.Integer)

    response_field = {
        'id' : fields.Integer,
        'pemain_id' : fields.Integer,
        'pemain_name' : fields.String,
        'pemain_url_image' : fields.String,
        'booking_location' : fields.String,
        'sport' : fields.String,
        'sport_image' : fields.String,
        'player_amount' : fields.Integer,
        'marker' : fields.Integer,

    }
  
    def __init__(self, pemain_id, pemain_name, pemain_url_image, booking_location,sport,sport_image,player_amount,marker):
        self.pemain_id = pemain_id
        self.pemain_name = pemain_name
        self.pemain_url_image = pemain_url_image
        self.booking_location = booking_location
        self.sport = sport
        self.sport_image = sport_image
        self.player_amount = player_amount
        self.marker = marker

    def __repr__(self): #initiate table model
        return '<AcceptedBooking %r>' % self.id 
  