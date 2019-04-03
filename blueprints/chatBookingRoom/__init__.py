import random, logging
from blueprints import db
from flask_restful import fields


class ChatBookingRoom(db.Model):
    __tablename__ = "chatbookingroom"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    lokasi = db.Column(db.String(255))    
    waktu = db.Column(db.String(500))
    olahraga = db.Column(db.String(255))    

    response_field = {
        'id' : fields.Integer,
        'booking_id' : fields.Integer,
        'user_id' : fields.Integer,
        'lokasi' : fields.String,
        'waktu' : fields.String,
        'olahraga' : fields.String,

    }
  
    def __init__(self, booking_id, user_id, lokasi, waktu,olahraga):
        self.booking_id = booking_id
        self.user_id = user_id
        self.lokasi = lokasi
        self.waktu = waktu
        self.olahraga = olahraga

    def __repr__(self): #initiate table model
        return '<ChatBookingRoom %r>' % self.id 
  