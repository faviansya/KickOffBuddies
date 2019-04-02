import json, logging, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime
from password_strength import PasswordPolicy
from ..pebisnis import *
from . import *

bp_lapangan = Blueprint('lapangan', __name__)
api = Api(bp_lapangan)
       
class LapanganResources(Resource):

    def __init__(self):
        pass

    def get(self, lapangan_endpoint = None):
        if lapangan_endpoint is not None:
            qry = Lapangan.query.get(lapangan_endpoint)
            return {'status' : 'Success', 'data' : marshal(qry, Lapangan.response_field)}, 200, {'Content_type' : 'application/json'}
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 50)
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Lapangan.query

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Lapangan.response_field))
            
            return {'status' : 'Success', 'data' : rows}, 200, {'Content_type' : 'application/json'} 
    
    @jwt_required
    def delete(self, lapangan_endpoint):
        qry = Lapangan.query.get(lapangan_endpoint)
        if qry.id_pebisnis == get_jwt_claims()['id'] :
            db.session.delete(qry)
            db.session.commit()    
            return {'status' : 'Success', 'message' : 'Field Deleted'}, 200, {'Content_type' : 'application/json'}
        return {'status' : 'Failed', 'message' : 'Unauthorized User'}, 400, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, lapangan_endpoint):        
        qry = Lapangan.query.get(lapangan_endpoint)
        marshal_lapangan = marshal(qry, Lapangan.response_field)

        parser = reqparse.RequestParser()
        parser.add_argument('jenis_lapangan', location = 'json')
        parser.add_argument('url_image', location = 'json')
        args = parser.parse_args()

        if args['jenis_lapangan'] is not None:
            qry.jenis_lapangan = args['jenis_lapangan']
        if args['url_image'] is not None:
            qry.url_image = args['url_image']
        db.session.commit()
        marshal_lapangan = marshal(qry, Lapangan.response_field)
        return {'status' : 'Success Change', 'data' : marshal_lapangan}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def post(self):
        jwtclaim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('jenis_lapangan', location = 'json', required = True)
        parser.add_argument('url_image', location = 'json', required = True)
        args = parser.parse_args()

        lapangan = Lapangan(None, jwtclaim['id'], args['jenis_lapangan'], args['url_image'], 0, 0)
        db.session.add(lapangan)
        db.session.commit()

        return {'status' : 'Success', 'data' : marshal(lapangan, Lapangan.response_field)}, 200, {'Content_type' : 'application/json'}

class LapanganSelfResources(Resource):
    @jwt_required
    def get(self, lapangan_endpoint = None):
        jwtclaim = get_jwt_claims()
        if lapangan_endpoint is not None:
            qry = Lapangan.query.get(lapangan_endpoint)
            if qry.id_pebisnis == jwtclaim['id']:
                return {'status' : 'Success', 'data' : marshal(qry, Lapangan.response_field)}, 200, {'Content_type' : 'application/json'}
            return {'status' : 'Failed', 'message' : 'Unauthorized User'}, 400, {'Content_type' : 'application/json'}
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 50)
            args = parser.parse_args()
            offside = (args['p'] * args['rp']) - args['rp']
            qry = Lapangan.query
            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                if row.id_pebisnis == jwtclaim['id']:
                    rows.append(marshal(row, Lapangan.response_field))        
            return {'status' : 'Success', 'data' : rows}, 200, {'Content_type' : 'application/json'} 


api.add_resource(LapanganResources, '', '/<lapangan_endpoint>')
api.add_resource(LapanganSelfResources, '', '/posted','/posted/<lapangan_endpoint>')
