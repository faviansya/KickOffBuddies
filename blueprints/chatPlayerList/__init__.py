import random, logging
from blueprints import db
from flask_restful import fields


class ChatPlayerList(db.Model):
    __tablename__ = "chatplayerlist"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    response_field = {
        'id' : fields.Integer,
        'room_id' : fields.Integer,
        'user_id' : fields.Integer,

    }
  
    def __init__(self, room_id, user_id):
        self.room_id = room_id
        self.user_id = user_id

    def __repr__(self): #initiate table model
        return '<ChatPlayerList %r>' % self.id 
  