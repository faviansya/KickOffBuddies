import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from ..pemain import *
from ..bookingrequest import *
from . import *

bp_playerlist = Blueprint('playerlist', __name__)
api = Api(bp_playerlist)
       
class PlayerListResources(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, playerlist_endpoint = None):
        jwtclaim = get_jwt_claims()
        if playerlist_endpoint == None :
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 50)
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = PlayerList.query

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, PlayerList.response_field))

            return {'status':'success', 'data':rows}, 200, {'Content_type' : 'application/json'}

        else :

            qry = PlayerList.query.filter_by(booking_id=playerlist_endpoint)
            
            rows = []
            player = []
            for row in qry :
                rows.append(marshal(row, PlayerList.response_field))
            qry_booking = BookingRequest.query.get(rows[0]['booking_id'])
            get_player = marshal(qry_booking, BookingRequest.response_field)["player"]

            for i in range(int(get_player)):
                try:
                    qry_pemain = Pemain.query.get(rows[i]["pemain_id"])
                    marshal_pemain = marshal(qry_pemain, Pemain.response_field)
                    player.append(marshal_pemain)
                except:
                    player.append({"user_type":"empty"})

            if rows is not None:
                return {'status':'success', 'data': rows, "pemain":player}, 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT FOUND','m':'Not found'}, 404, {'Content-Type':'application/json'}
    
    @jwt_required
    def delete(self, playerlist_endpoint):
        jwtclaim = get_jwt_claims()
        qry = PlayerList.query.get(playerlist_endpoint)
        
        db.session.delete(qry)
        db.session.commit()

        return {'status' : 'Success', 'message' : 'Cancelled'}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, playerlist_endpoint):
        jwtclaim = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('booking_id', location = 'json', type=int, required=True)
        args = parser.parse_args()

        qry = PlayerList.query.get(playerlist_endpoint)
        marshal_request = marshal(qry, PlayerList.response_field)

        qry.booking_id= args['booking_id']

        db.session.commit()
        qry = PlayerList.query.get(playerlist_endpoint)
        marshal_playerlist = marshal(qry, PlayerList.response_field)

        return {'status' : 'Success Change', 'data' : marshal_playerlist}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def post(self):
        jwtclaim = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('booking_id', location = 'json', type=int, required=True)
        args = parser.parse_args()

        qry_booking = BookingRequest.query.get(args['booking_id'])
        get_player = marshal(qry_booking, BookingRequest.response_field)["player"]

        qry = PlayerList.query.filter(PlayerList.booking_id.like(args['booking_id'])).all()

        for row in qry :
            if(jwtclaim['id'] == marshal(row, PlayerList.response_field)['pemain_id']):
                return {'status' : 'failed', "message":"Player Already Exist"},401,{'Content_type' : 'application/json'}
            
        playerlist = PlayerList(None, args['booking_id'], jwtclaim['id'], jwtclaim['name'], get_player)
        db.session.add(playerlist)
        db.session.commit()

        return {'status' : 'Success','data' : marshal(qry, PlayerList.response_field)}, 200, {'Content_type' : 'application/json'}

api.add_resource(PlayerListResources, '', '/<playerlist_endpoint>')
