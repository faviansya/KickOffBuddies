import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims
from ..chatBookingRoom import *
from ..pemain import *
bp_chatplayerlist = Blueprint('chatplayerlist', __name__)
api = Api(bp_chatplayerlist)

class ChatPlayerListResources(Resource): 

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        jwtclaim = get_jwt_claims()
        qry_ListmyselfRoom = ChatPlayerList.query.filter(ChatPlayerList.user_id.like(jwtclaim["id"])).all()
        marshal_ListmyselfRoom = marshal(qry_ListmyselfRoom, ChatPlayerList.response_field)
        
        myRooms = []
        for myChatRooms in marshal_ListmyselfRoom:
            qry_playerList = ChatPlayerList.query.filter(ChatPlayerList.room_id.like(myChatRooms["room_id"])).all()
            marshal_playerList = marshal(qry_playerList, ChatPlayerList.response_field)
            player = []
            
            for booking in marshal_playerList:
                player.append(booking)

            player_info = []
            for player_detail in player:
                qry_details = Pemain.query.get(player_detail["user_id"])
                marshal_player_detail= marshal(qry_details, Pemain.response_field)
                player_info.append(marshal_player_detail)
            
            
            qry_sport_info = ChatBookingRoom.query.get(myChatRooms["room_id"])
            marshal_qry_sport_info = marshal(qry_sport_info, ChatBookingRoom.response_field)
            myChatRooms["location"] = marshal_qry_sport_info["lokasi"]
            myChatRooms["waktu"] = marshal_qry_sport_info["waktu"]
            myChatRooms["olahraga"] = marshal_qry_sport_info["olahraga"]
            
            myChatRooms["player"] = player_info
            myRooms.append(myChatRooms)


        return {"status": "200 OK", "message": "All ChatPlayerList posted is on display", "data": myRooms}, 200, {'Content-Type': 'application/json'}   

    @jwt_required
    def delete(self, id):
        qry_del = ChatPlayerList.query.get(id)
        if qry_del is not None: 
            db.session.delete(qry_del)
            db.session.commit()
            return {"code": 200, "message": "OK, ChatPlayerList has been removed", "data": 'User with id = %d has been deleted' % id}, 200, {'Content-Type': 'application/json'}
        return {"code": 404, "message": "Failed to edit. Wrong username or password"}, 404, {'Content-Type': 'application/json'}
        
    def patch(self):
        return 'Not yet implemented', 501

    def options(self,id=None):
        return {},200

api.add_resource(ChatPlayerListResources, '', '/<int:id>')

