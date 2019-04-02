import json, logging, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime
from password_strength import PasswordPolicy
from ..lapangan import *
from . import *

bp_jadwal = Blueprint('jadwal', __name__)
api = Api(bp_jadwal)
       
class JadwalResources(Resource):

    def __init__(self):
        pass

    def get(self, jadwal_endpoint = None):
        if jadwal_endpoint is not None:
            qry = Jadwal.query.get(jadwal_endpoint)
            return {'status' : 'Success', 'data' : marshal(qry, Jadwal.response_field)}, 200, {'Content_type' : 'application/json'}
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 50)
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Jadwal.query

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Jadwal.response_field))
            
            return {'status' : 'Success', 'data' : rows}, 200, {'Content_type' : 'application/json'} 
    
    @jwt_required
    def delete(self, jadwal_endpoint):
        qry = Jadwal.query.get(jadwal_endpoint)
        db.session.delete(qry)
        db.session.commit()    
        return {'status' : 'Success', 'message' : 'Schedule Deleted'}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, jadwal_endpoint):        
        qry = Jadwal.query.get(jadwal_endpoint)
        marshal_jadwal = marshal(qry, Jadwal.response_field)

        parser = reqparse.RequestParser()
        parser.add_argument('id_lapangan', location = 'json')
        parser.add_argument('jam', location = 'json')
        parser.add_argument('tanggal', location = 'json')
        args = parser.parse_args()

        qry_lapangan = Lapangan.query.get(args['id_lapangan'])
        if args['id_lapangan'] is not None:
            qry.id_lapangan = args['id_lapangan']
            qry.id_pebisnis = qry_lapangan.id_pebisnis
        if args['jam'] is not None:
            qry.jam = args['jam']
        if args['tanggal'] is not None:
            qry.tanggal = args['tanggal']

        db.session.commit()
        marshal_jadwal = marshal(qry, Jadwal.response_field)
        return {'status' : 'Success Change', 'data' : marshal_jadwal}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_lapangan', location = 'json', required = True)
        parser.add_argument('jam', location = 'json', required = True)
        parser.add_argument('tanggal', location = 'json', required = True)
        args = parser.parse_args()

        qry_lapangan = Lapangan.query.get(args['id_lapangan'])  
        jadwal = Jadwal(None, qry_lapangan.id_pebisnis, args['id_lapangan'], args['jam'], args['tanggal'])
        db.session.add(jadwal)
        db.session.commit()

        return {'status' : 'Success', 'data' : marshal(jadwal, Jadwal.response_field)}, 200, {'Content_type' : 'application/json'}

api.add_resource(JadwalResources, '', '/<jadwal_endpoint>')
