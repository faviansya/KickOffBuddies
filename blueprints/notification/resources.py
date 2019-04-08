import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims
from sqlalchemy import desc

bp_notification = Blueprint('notification', __name__)
api = Api(bp_notification)

class NotificationResources(Resource): 

    def __init__(self):
        pass
        
    @jwt_required 
    def get(self):
        jwtclaim = get_jwt_claims()
        qry = Notification.query.filter(Notification.user_id.like(jwtclaim["id"])).order_by(desc(Notification.id)).all()
        # qry = Notification.query.order_by(desc(Pemain.created_time)).all()

        marshal_notificaiton = marshal(qry, Notification.response_field)
        
        return {'status' : 'Success', 'data' : marshal_notificaiton}, 200, {'Content_type' : 'application/json'}
    def options(self,id=None):
        return {},200


api.add_resource(NotificationResources, '', '/<int:id>')

