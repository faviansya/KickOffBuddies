import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *

bp_pemain = Blueprint('pemain', __name__)
api = Api(bp_pemain)
       
class PemainResources(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, pemain_endpoint = None):
        jwtclaim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 50)
        args = parser.parse_args()

        offside = (args['p'] * args['rp']) - args['rp']
        qry = Pemain.query

        rows = []
        for row in qry.limit(args['rp']).offset(offside).all():
            rows.append(marshal(row, Pemain.response_field))

        return rows, 200, {'Content_type' : 'application/json'}
    
    @jwt_required
    def delete(self):
        qry = Pemain.query.get(jwtclaim['id'])
        
        db.session.delete(qry)
        db.session.commit()

        return {'status' : 'Success', 'message' : 'See You Again In Another Time'}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self):
        jwtclaim = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('password', location = 'json',default=marshal_pemain['password'])
        args = parser.parse_args()

        qry = Pemain.query.get(jwtclaim['id'])
        marshal_pemain = marshal(qry, Pemain.response_field)

        qry.password = args['password']
        db.session.commit()

        return {'status' : 'Success Change', 'Your ID' : marshal_pemain}, 200, {'Content_type' : 'application/json'}

    def post(sef):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        args = parser.parse_args()

        pemain = Pemain(args['username'], args['password'])
        db.session.add(pemain)
        db.session.commit()

        return {'status' : 'Success', 'Your Account' : marshal(pemain, Pemain.response_field)}, 200, {'Content_type' : 'application/json'}

api.add_resource(PemainResources, '', '/<pemain_endpoint>')
