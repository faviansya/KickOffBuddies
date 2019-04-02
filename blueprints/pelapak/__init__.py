import random, logging
from blueprints import db
from flask_restful import fields


class SportVenue(db.Model):
    __tablename__ = "SportVenue"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    urlimage = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.String(255), nullable=False)
    jumlah_pemberi_rating = db.Column(db.Integer)

    response_field = {
        'id' : fields.Integer,
        'name' : fields.String,
        'address' : fields.String,
        'urlimage' : fields.String,
        'rating': fields.String,
        'jumlah_pemberi_rating': fields.String,
    }
  
    def __init__(self, name, address, urlimage, rating, jumlah_pemberi_rating):
        self.name = name
        self.address = address
        self.urlimage = urlimage
        self.rating = rating   
        self.jumlah_pemberi_rating = jumlah_pemberi_rating        
       
    def __repr__(self): #initiate table model
        return '<SportVenue %r>' % self.id 
  