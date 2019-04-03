import random, logging
from blueprints import db
from flask_restful import fields


class ChatList(db.Model):
    __tablename__ = "chatlist"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    message = db.Column(db.String(500))
    time = db.Column(db.String(500))

    response_field = {
        'id' : fields.Integer,
        'room_id' : fields.Integer,
        'user_id' : fields.Integer,
        'message' : fields.String,
        'time' : fields.String,
    }
  
    def __init__(self, room_id, user_id,message,time):
        self.room_id = room_id
        self.user_id = user_id
        self.message = message
        self.time = time

    def __repr__(self): #initiate table model
        return '<ChatList %r>' % self.id 
  