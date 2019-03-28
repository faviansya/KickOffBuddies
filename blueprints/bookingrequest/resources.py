import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *

bp_bookingrequest = Blueprint('booking request', __name__)
api = Api(bp_bookingrequest)
       
class BookingRequestResources(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, request_endpoint = None):
        jwtclaim = get_jwt_claims()
        if request_endpoint == None :
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 50)
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = BookingRequest.query

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, BookingRequest.response_field))

            return {'status':'success', 'data':rows}, 200, {'Content_type' : 'application/json'}
        else :
            qry = BookingRequest.query.get(request_endpoint)
            data = marshal(qry, BookingRequest.response_field)              
            if qry is not None:
                return {'status':'success', 'data': data}, 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT FOUND','message':'Booking request not found'}, 404, {'Content-Type':'application/json'}
    
    @jwt_required
    def delete(self, request_endpoint):
        jwtclaim = get_jwt_claims()
        qry = BookingRequest.query.get(request_endpoint)
        
        db.session.delete(qry)
        db.session.commit()

        return {'status' : 'Success', 'message' : 'Booking Request Cancelled'}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, request_endpoint):
        jwtclaim = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('sport', location = 'json', required=True)
        parser.add_argument('player', location = 'json', type=int, required=True)
        parser.add_argument('time', location = 'json', required=True)
        parser.add_argument('location', location = 'json', required=True)

        args = parser.parse_args()

        qry = BookingRequest.query.get(request_endpoint)
        marshal_request = marshal(qry, BookingRequest.response_field)

        qry.sport= args['sport']
        qry.player= args['player']
        qry.time= args['time']
        qry.location= args['location']

        db.session.commit()
        qry = BookingRequest.query.get(request_endpoint)
        marshal_request = marshal(qry, BookingRequest.response_field)

        return {'status' : 'Success Change', 'data' : marshal_request}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def post(self):
        jwtclaim = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('sport', location = 'json', required=True)
        parser.add_argument('player', location = 'json', type=int, required=True)
        parser.add_argument('time', location = 'json', required=True)
        parser.add_argument('location', location = 'json', required=True)

        args = parser.parse_args()

        booking_request = BookingRequest(None, jwtclaim['id'], args['sport'], args['player'], args['time'], args['location'], 'waiting for players')
        db.session.add(booking_request)
        db.session.commit()

        return {'status' : 'Success','data' : marshal(booking_request, BookingRequest.response_field)}, 200, {'Content_type' : 'application/json'}

class MyBookingResources(Resource):
    @jwt_required
    def get(self):
        jwtclaim = get_jwt_claims()
        parser = reqparse.RequestParser()

        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 50)

        args = parser.parse_args()

        offside = (args['p'] * args['rp']) - args['rp']
        qry = BookingRequest.query.filter_by(id_user=jwtclaim['id'])
        rows = []
        for row in qry.limit(args['rp']).offset(offside).all():
            rows.append(marshal(row, BookingRequest.response_field))
        return {'status':'success', 'data':rows}, 200, {'Content_type' : 'application/json'}

api.add_resource(BookingRequestResources, '', '/<request_endpoint>')
api.add_resource(MyBookingResources, '/mybooking')
