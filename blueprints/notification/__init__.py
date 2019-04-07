import random, logging
from blueprints import db
from flask_restful import fields


class Notification(db.Model):
    __tableuser_id__ = "notification"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    notification = db.Column(db.String(1000))
    read_status = db.Column(db.String(10))

    response_field = {
        'id' : fields.Integer,
        'user_id' : fields.String,
        'notification' : fields.String,
        'read_status' : fields.String,

    }
  
    def __init__(self, user_id, notification,read_status):
        self.user_id = user_id
        self.notification = notification
        self.read_status = read_status

    def __repr__(self): #initiate table model
        return '<Notification %r>' % self.id 
  