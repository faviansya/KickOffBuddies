import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from ..pemain import *
from ..bookingrequest import *
from . import *
from ..accepted_booking import *


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
        elif playerlist_endpoint == "mylist":
            qry = PlayerList.query.filter(PlayerList.pemain_id.like(jwtclaim['id'])).all()

            rows = []
            bookings = []
            for row in qry :
                qry_booking = BookingRequest.query.get(marshal(row, PlayerList.response_field)['booking_id'])
                rows.append(marshal(row, PlayerList.response_field))
                bookings.append(marshal(qry_booking, BookingRequest.response_field))

            return {'status':'success', 'data': rows, "booking":bookings}, 200, {'Content-Type': 'application/json'}
        
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
                    marshal_pemain["ListId"] = rows[i]["id"]
                    marshal_pemain["isThisMyself"] = 'no'
                    if jwtclaim['id'] == marshal_pemain['id']:
                        marshal_pemain["isThisMyself"] = 'yes'                    
                    player.append(marshal_pemain)
                except:
                    player.append({"user_type":"empty","isThisMyself":"no"})

            if rows is not None:
                return {'status':'success', 'data': rows, "pemain":player}, 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT FOUND','m':'Not found'}, 404, {'Content-Type':'application/json'}
    
    @jwt_required
    def delete(self, playerlist_endpoint):
        jwtclaim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('booking_id', location = 'json', type=int, required=True)
        args = parser.parse_args()

        qry = PlayerList.query.get(playerlist_endpoint)

        db.session.delete(qry)
        db.session.commit()

        qry_booking = BookingRequest.query.get(args['booking_id'])
        pemain_now = marshal(qry_booking, BookingRequest.response_field)["pemain_saat_ini"]
        if pemain_now <= 1:
            db.session.delete(qry_booking)
            db.session.commit()
        else:
            qry_booking.pemain_saat_ini = pemain_now -1
            db.session.commit()


        return {'status' : "success", 'message' : "success"}, 200, {'Content_type' : 'application/json'}

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
        pemain_now = marshal(qry_booking, BookingRequest.response_field)["pemain_saat_ini"]
        if(pemain_now < 1):
            pemain_now = 1
        else:
            pemain_now = pemain_now + 1
        qry_booking.pemain_saat_ini = pemain_now
        qry = PlayerList.query.filter(PlayerList.booking_id.like(args['booking_id'])).all()
        
        for row in qry:
            if(jwtclaim['id'] == marshal(row, PlayerList.response_field)['pemain_id']):
                return {'status' : 'failed', "message":"Player Already Exist"},401,{'Content_type' : 'application/json'}

        playerlist = PlayerList(None, args['booking_id'], jwtclaim['id'], jwtclaim['name'],jwtclaim['url_image'], get_player, pemain_now)
        
        db.session.add(playerlist)
        db.session.commit()

        qry = PlayerList.query.filter(PlayerList.booking_id.like(args['booking_id'])).all()
        pemain_now = marshal(qry_booking, BookingRequest.response_field)["pemain_saat_ini"]
        pemain_sisa = marshal(qry_booking, BookingRequest.response_field)["player"]
        marshal_booking = marshal(qry_booking, BookingRequest.response_field)
        getID = marshal(qry, PlayerList.response_field)
        rows = []
        counter = 0
        if(pemain_now >= pemain_sisa):
            for data in qry:
                data_marshal = marshal(data, PlayerList.response_field)
                counter +=1
                for i in getID:
                    if counter == 1:
                        inputToAcceptedBooking= AcceptedBooking(i["pemain_id"],data_marshal["pemain_name"],data_marshal["pemain_image"],marshal_booking["location"],marshal_booking["sport"],marshal_booking["url_image"],pemain_now,1)
                        db.session.add(inputToAcceptedBooking)
                        db.session.commit()
                        rows.append(data_marshal)
                    else:
                        inputToAcceptedBooking= AcceptedBooking(i["pemain_id"],data_marshal["pemain_name"],data_marshal["pemain_image"],marshal_booking["location"],marshal_booking["sport"],marshal_booking["url_image"],pemain_now,0)
                        db.session.add(inputToAcceptedBooking)
                        db.session.commit()
                        rows.append(data_marshal)

        
        return {"len":pemain_now,"lensisa":pemain_sisa, "Len Now":len(marshal(qry, PlayerList.response_field)),'status' : 'Success','data' : marshal(qry_booking, BookingRequest.response_field),"a":rows}, 200, {'Content_type' : 'application/json'}

api.add_resource(PlayerListResources, '', '/<playerlist_endpoint>')
