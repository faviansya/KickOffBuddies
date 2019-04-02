import random, logging
from blueprints import db
from flask_restful import fields


class GoogleHandler(db.Model):
    __tablename__ = "googlehandler"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    url_image = db.Column(db.String(1000))

    response_field = {
        'id' : fields.Integer,
        'username' : fields.Integer,
        'name' : fields.String,
        'url_image' : fields.String,

    }
  
    def __init__(self, username, name, url_image):
        self.username = username
        self.name = name
        self.url_image = url_image

    def __repr__(self): #initiate table model
        return '<GoogleHandler %r>' % self.id 
  