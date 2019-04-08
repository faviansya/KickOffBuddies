import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_chatbookingroom = Blueprint('chatbookingroom', __name__)
api = Api(bp_chatbookingroom)

class ChatBookingRoomResources(Resource): 

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        jwtclaim = get_jwt_claims()
        qry = ChatBookingRoom.query.filter(ChatBookingRoom.user_id.like(jwtclaim["id"]))
        rows = []
        for row in qry:
            rows.append(marshal(row, ChatBookingRoom.response_field))
        return {"status": "200 OK", "message": "All ChatBookingRoom posted is on display", "data": rows}, 200, {'Content-Type': 'application/json'}   

    @jwt_required 
    def delete(self, id):
        qry_del = ChatBookingRoom.query.get(id)
        if qry_del is not None: 
            db.session.delete(qry_del)
            db.session.commit()
            return {"code": 200, "message": "OK, ChatBookingRoom has been removed", "data": 'User with id = %d has been deleted' % id}, 200, {'Content-Type': 'application/json'}
        return {"code": 404, "message": "Failed to edit. Wrong username or password"}, 404, {'Content-Type': 'application/json'}
        
    def patch(self):
        return 'Not yet implemented', 501

    def options(self,id=None):
        return {},200

api.add_resource(ChatBookingRoomResources, '', '/<int:id>')

