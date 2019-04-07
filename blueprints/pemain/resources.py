import json
import logging
import hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime
from password_strength import PasswordPolicy

from . import *

bp_pemain = Blueprint('pemain', __name__)
api = Api(bp_pemain)

from ..calendar import calendar
import queue
import threading
import time

class PemainResources(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, pemain_endpoint=None):
        jwtclaim = get_jwt_claims()
        if pemain_endpoint is not None:
            if pemain_endpoint == "me":
                qry = Pemain.query.get(jwtclaim['id'])
                return {'status': 'Success', 'data': marshal(qry, Pemain.response_field)}, 200, {'Content_type': 'application/json'}
            else:
                parser = reqparse.RequestParser()
                qry = Pemain.query.get(pemain_endpoint)
                if(qry is None):
                    return {'status': 'Success', 'data': []}, 200, {'Content_type': 'application/json'}
                return {'status': 'Success', 'data': marshal(qry, Pemain.response_field)}, 200, {'Content_type': 'application/json'}
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=50)
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Pemain.query

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Pemain.response_field))

            return {'status': 'Success', 'data': rows}, 200, {'Content_type': 'application/json'}

    @jwt_required
    def delete(self):
        qry = Pemain.query.get(get_jwt_claims()['id'])
        db.session.delete(qry)
        db.session.commit()

        return {'status': 'Success', 'message': 'See You Again In Another Time'}, 200, {'Content_type': 'application/json'}

    @jwt_required
    def put(self):
        policy = PasswordPolicy.from_names(
            length=6,
            uppercase=1,
            numbers=1,
            special=1,
        )
        jwtclaim = get_jwt_claims()
        google = 1
        qry = Pemain.query.get(jwtclaim['id'])
        marshal_pemain = marshal(qry, Pemain.response_field)

        parser = reqparse.RequestParser()
        parser.add_argument('password', location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('phone_no', location='json')
        parser.add_argument('address', location='json')
        parser.add_argument('favourite_sport', location='json')
        parser.add_argument('url_image', location='json')
        args = parser.parse_args()

        if args['password'] is not None:
            validation = policy.test(args['password'])
            if validation == []:
                password = hashlib.md5(args['password'].encode()).hexdigest()
                qry.password = password
                if args['name'] is not None:
                    qry.name = args['name']
                if args['email'] is not None:
                    if ("@google" in args['email']):
                        qry.is_google = google
                    qry.email = args['email']
                if args['phone_no'] is not None:
                    qry.phone_no = args['phone_no']
                if args['address'] is not None:
                    qry.address = args['address']
                if args['favourite_sport'] is not None:
                    qry.favourite_sport = args['favourite_sport']
                if args['url_image'] is not None:
                    qry.url_image = args['url_image']
                db.session.commit()
                marshal_pemain = marshal(qry, Pemain.response_field)
                return {'status': 'Success Change', 'data': marshal_pemain}, 200, {'Content_type': 'application/json'}
            return {'status': 'Password Invalid'}, 400, {'Content_type': 'application/json'}
        else:
            if args['name'] is not None:
                qry.name = args['name']
            if args['email'] is not None:
                qry.email = args['email']
            if args['phone_no'] is not None:
                qry.phone_no = args['phone_no']
            if args['address'] is not None:
                qry.address = args['address']
            if args['favourite_sport'] is not None:
                qry.favourite_sport = args['favourite_sport']
            if args['url_image'] is not None:
                qry.url_image = args['url_image']
            db.session.commit()
            marshal_pemain = marshal(qry, Pemain.response_field)
            return {'status': 'Success Change', 'data': marshal_pemain}, 200, {'Content_type': 'application/json'}

    def post(self):
        policy = PasswordPolicy.from_names(
            length=6,
            uppercase=1,
            numbers=1,
            special=1,
        )
        google = 0
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone_no', location='json')
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('favourite_sport', location='json', required=True)
        parser.add_argument('url_image', location='json', required=True)
        args = parser.parse_args()

        # pemain = Pemain(args['username'],password,args['name'],args['email'],args['phone_no'],args['address'],args['favourite_sport'],"pemain",str(datetime.datetime.now()),args['url_image'])
        validation = policy.test(args['password'])

        if("@gmail" in args["email"]):
            events = threading.Event()
            myCalendar = calendar.Calendar(events,args["email"])
            t1 = threading.Thread(target = myCalendar.flags)
            t2 = threading.Thread(target = myCalendar.setCalendar)
            t1.start()
            t2.start()
            print ("T2",t2)
            google = 1

        if validation == []:
            password = hashlib.md5(args['password'].encode()).hexdigest()

            pemain = Pemain(args['username'], password, args['name'], args['email'], args['phone_no'], args['address'],
                            args['favourite_sport'], "pemain", str(datetime.datetime.now()), args['url_image'], google)
            db.session.add(pemain)
            db.session.commit()

            return {'status': 'Success', 'data': marshal(pemain, Pemain.response_field)}, 200, {'Content_type': 'application/json'}
        return {'status': 'Password Invalid'}, 400, {'Content_type': 'application/json'}


api.add_resource(PemainResources, '', '/<pemain_endpoint>')
