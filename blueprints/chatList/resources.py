import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims
from ..chatBookingRoom import *
from ..pemain import *

import datetime

bp_chatlist = Blueprint('chatlist', __name__)
api = Api(bp_chatlist)

class ChatListResources(Resource): 

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        jwtclaim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('Room_id', location='args')
        args = parser.parse_args()

        qry = ChatList.query.filter(ChatList.room_id.like(args["Room_id"])).all()
        marshal_qry = marshal(qry, ChatList.response_field)
        rows = []
        for row in marshal_qry:
            qry_pemain = Pemain.query.get(row["user_id"])
            marshal_pemain = marshal(qry_pemain, Pemain.response_field)

            row["name_user"] = marshal_pemain["name"]
            row["url_image"] = marshal_pemain["url_image"]
            rows.append(row)

        return {"status": "200 OK", "message": "All ChatList posted is on display", "data": rows}, 200, {'Content-Type': 'application/json'}   

    @jwt_required 
    def delete(self, id):
        qry_del = ChatList.query.get(id)
        if qry_del is not None: 
            db.session.delete(qry_del)
            db.session.commit()
            return {"code": 200, "message": "OK, ChatList has been removed", "data": 'User with id = %d has been deleted' % id}, 200, {'Content-Type': 'application/json'}
        return {"code": 404, "message": "Failed to edit. Wrong username or password"}, 404, {'Content-Type': 'application/json'}

    @jwt_required 
    def post(self): #for pemain to add polling
        jwtclaim = get_jwt_claims()
  
        parser = reqparse.RequestParser()
        parser.add_argument('room_id', location='args')
        parser.add_argument('message', location='args')
        args = parser.parse_args() 

        add_message = ChatList(args['room_id'], jwtclaim['id'], args['message'],str(datetime.datetime.now()))
        db.session.add(add_message) #insert the input data into the database
        db.session.commit() 
        return {"message": "Message has been Sent", "data":marshal(add_message, ChatList.response_field)}, 200, {'Content-Type': 'application/json'}   


    def patch(self):
        return 'Not yet implemented', 501

api.add_resource(ChatListResources, '', '/<int:id>')

