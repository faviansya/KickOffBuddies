
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
app.register_blueprint(bp_auth, url_prefix='/api/login')

from blueprints.pemain.resources import bp_pemain
from blueprints.pebisnis.resources import bp_pebisnis
from blueprints.bookingrequest.resources import bp_bookingrequest
from blueprints.player_list.resources import bp_playerlist
from blueprints.polling.resources import bp_polling
from blueprints.accepted_booking.resources import bp_acceptedbooking
from blueprints.jadwal.resources import bp_jadwal
from blueprints.googleHandler.resources import bp_googlehandler
from blueprints.lapangan.resources import bp_lapangan
from blueprints.chatBookingRoom.resources import bp_chatbookingroom
from blueprints.chatPlayerList.resources import bp_chatplayerlist
from blueprints.chatList.resources import bp_chatlist
from blueprints.notification.resources import bp_notification


app.register_blueprint(bp_pemain, url_prefix='/api/pemain')
app.register_blueprint(bp_bookingrequest, url_prefix='/api/booking')
app.register_blueprint(bp_pebisnis, url_prefix='/api/pebisnis')
app.register_blueprint(bp_playerlist, url_prefix='/api/playerlist')
app.register_blueprint(bp_polling, url_prefix='/api/polling')
app.register_blueprint(bp_acceptedbooking, url_prefix='/api/acceptbooking')
app.register_blueprint(bp_jadwal, url_prefix='/api/jadwal')
app.register_blueprint(bp_googlehandler, url_prefix='/api/google')
app.register_blueprint(bp_lapangan, url_prefix='/api/lapangan')
app.register_blueprint(bp_chatbookingroom, url_prefix='/api/chatroom')
app.register_blueprint(bp_chatplayerlist, url_prefix='/api/chatplayerlist')
app.register_blueprint(bp_chatlist, url_prefix='/api/chat')
app.register_blueprint(bp_notification, url_prefix='/api/notification')

db.create_all()