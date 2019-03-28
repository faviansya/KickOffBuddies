
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from time import strftime
import json, logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fatma:12345678@kickofbuddies.c26kug0ctusy.ap-southeast-1.rds.amazonaws.com:3306/kickofbuddies'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['JWT_SECRET_KEY'] = 'SFsieaaBsLEpecP675r243faM8oSB2hV'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

api = Api(app, catch_all_404s = True)

@app.after_request
def after_request(response):
    if request.method == 'GET':
        app.logger.warning("REQUEST LOG\t%s%s", json.dumps({'request' : request.args.to_dict(), 'response' : json.loads(response.data.decode('utf-8'))}), request.method)
    else:    
        app.logger.warning("REQUEST LOG\t%s%s", json.dumps({'request' : request.get_json(), 'response' : json.loads(response.data.decode('utf-8'))}), request.method)
    return response

jwt = JWTManager(app)
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity


from blueprints.auth import bp_auth
from blueprints.pemain.resources import bp_pemain
from blueprints.pebisnis.resources import bp_pebisnis
from blueprints.bookingrequest.resources import bp_bookingrequest

app.register_blueprint(bp_auth, url_prefix='/api/login')
app.register_blueprint(bp_pemain, url_prefix='/api/pemain')
app.register_blueprint(bp_bookingrequest, url_prefix='/api/booking')
app.register_blueprint(bp_pebisnis, url_prefix='/api/pebisnis')

db.create_all()