import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *

bp_basket = Blueprint('basket', __name__)
api = Api(bp_basket)
       
class BasketResources(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, basket_endpoint = None):
        jwtclaim = get_jwt_claims()
        if basket_endpoint == None :
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 50)
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Basket.query

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Basket.response_field))

            return {'status':'success', 'data':rows}, 200, {'Content_type' : 'application/json'}
        else :
            qry = Basket.query.filter_by(booking_id=basket_endpoint)
            rows = []
            for row in qry :
                rows.append(marshal(row, Basket.response_field))              
            if rows is not None:
                return {'status':'success', 'data': rows}, 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT FOUND','message':'Not found'}, 404, {'Content-Type':'application/json'}
    
    @jwt_required
    def delete(self, basket_endpoint):
        jwtclaim = get_jwt_claims()
        qry = Basket.query.get(basket_endpoint)
        
        db.session.delete(qry)
        db.session.commit()

        return {'status' : 'Success', 'message' : 'Cancelled'}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, basket_endpoint):
        jwtclaim = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('booking_id', location = 'json', type=int, required=True)
        parser.add_argument('pebisnis_id', location = 'json', type=int, required=True)
        parser.add_argument('pebisnis_name', location = 'json', required=True)

        args = parser.parse_args()

        qry = Basket.query.get(basket_endpoint)
        marshal_request = marshal(qry, Basket.response_field)

        qry.booking_id= args['booking_id']
        qry.pebisnis_id= args['pebisnis_id']
        qry.pebisnis_name= args['pebisnis_name']

        db.session.commit()
        qry = Basket.query.get(basket_endpoint)
        marshal_basket = marshal(qry, Basket.response_field)

        return {'status' : 'Success Change', 'data' : marshal_basket}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def post(self):
        jwtclaim = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('booking_id', location = 'json', type=int, required=True)
        parser.add_argument('pebisnis_id', location = 'json', type=int, required=True)
        parser.add_argument('pebisnis_name', location = 'json', required=True)

        args = parser.parse_args()

        basket = Basket(None, args['booking_id'], jwtclaim['id'], args['pebisnis_id'], jwtclaim['name'], args['pebisnis_name'])
        db.session.add(basket)
        db.session.commit()

        return {'status' : 'Success','data' : marshal(basket, Basket.response_field)}, 200, {'Content_type' : 'application/json'}

api.add_resource(BasketResources, '', '/<basket_endpoint>')
