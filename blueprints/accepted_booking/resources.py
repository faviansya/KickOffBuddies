import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_acceptedbooking = Blueprint('acceptedbooking', __name__)
api = Api(bp_acceptedbooking)

class AcceptedBookingResources(Resource): 

    def __init__(self):
        pass

    @jwt_required
    def get(self,acceptlist_endpoint=None): 
        jwtclaim = get_jwt_claims()
        if(acceptlist_endpoint == None):
            return {"status": "200 OK", "message": "All History posted", "data": "masok"}, 200, {'Content-Type': 'application/json'}   
        else:
            qry = AcceptedBooking.query
            rows = []
            for row in qry.filter(AcceptedBooking.pemain_id.like(acceptlist_endpoint)).all():
                rows.append(marshal(row, AcceptedBooking.response_field))
            return {"status": "200 OK", "message": "All History posted", "data": rows}, 200, {'Content-Type': 'application/json'}   

    # @jwt_required      
    # def post(self): #for pemain to add polling       
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('sport', location='json')
    #     parser.add_argument('lokasi', location='json')
    #     parser.add_argument('jumlah_polling', location='json')
    #     args = parser.parse_args() 
    #     name = get_jwt_claims()['name'] 

    #     if get_jwt_claims()['user_type']  == 'pemain':
    #         add_polling = AcceptedBooking(name, args['sport'], args['lokasi'], args['jumlah_polling'])
    #         db.session.add(add_polling) #insert the input data into the database
    #         db.session.commit() 
    #     return {"code": 200, "message": "OK, polling has been successfully posted", "data":marshal(add_polling, AcceptedBooking.response_field)}, 200, {'Content-Type': 'application/json'}   
        
    def patch(self):
        return 'Not yet implemented', 501

    def options(self,acceptlist_endpoint=None):
        return {},200

api.add_resource(AcceptedBookingResources, '', '/<acceptlist_endpoint>')

