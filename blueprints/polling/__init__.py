import random, logging
from blueprints import db
from flask_restful import fields


class Polling(db.Model):
    __tablename__ = "polling"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False) #nama user yang memberikan polling
    sport = db.Column(db.String(255), nullable=False) #lapangan sport apa yang dipunya
    lokasi = db.Column(db.String(255), nullable=False)    
    jumlah_polling = db.Column(db.String(55), nullable=False)

    response_field = {
        'id' : fields.Integer,
        'name' : fields.String,
        'sport' : fields.String,
        'lokasi' : fields.String,
        'jumlah_polling' : fields.Integer,
    }
  
    def __init__(self, name, sport, lokasi, jumlah_polling):
        self.name = name
        self.sport = sport
        self.lokasi = lokasi
        self.jumlah_polling = jumlah_polling
       
    def __repr__(self): #initiate table model
        return '<Polling %r>' % self.id 
  