from flask import Flask,request,jsonify
from flask_restplus import fields,Api,Resource
from flask_pymongo import PyMongo

import datetime, uuid
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict
import json
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_raw_jwt
    )
from flask_bcrypt import Bcrypt

LOG = logging.getLogger(__name__)
app=Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://localhost:27017/college'
mongo= PyMongo(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# JWT_COOKIE_CSRF_PROTECT = False
# app.config['JWT_COOKIE_CSRF_PROTECT'] = False



jwt = JWTManager(app)
flask_bcrypt = Bcrypt(app)
CORS(app)
api = Api(app)


LOG_FILENAME = "college.log"
FORMAT = '%(levelname)7s%(name)10s%(filename)15s:%(lineno)4d -%(funcName)8s \
    %(asctime)s, %(msecs)s, %(message)s'


LOG.setLevel(logging.INFO)
logging.basicConfig(
   filename = LOG_FILENAME,
   filemode = 'a',
   level = logging.INFO,
   format = FORMAT,
   datefmt = '%H:%M:%S')

filehandler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=1024, backupCount=3)

LOG.addHandler(filehandler)


class Auth:
    
    login = api.model('login',{
            'username':fields.String(required = True),
            'password':fields.String(required = True),            
        })

    auth_response = api.model('auth_response',{
            'msg':fields.String,
            'access_token':fields.String,  
            'refresh_token':fields.String, 
            'username':fields.String,
            'role':fields.String,
            '_id':fields.String,
            'login': fields.Boolean
        })


    @classmethod
    def get_user(cls, email):
        """add new user"""
        user = mongo.db.users.find_one({"email":email})
        return user

    @classmethod
    def authorise(cls, data):
        """add new user"""
        user = cls.get_user(data['username'])
        if user != None:
            _id = user['_id']     
            role = user['role']
            password = user['password']
            print(role)
            if flask_bcrypt.check_password_hash(password, data["password"]):
                resp = {'msg': "login success", "_id":_id, "role":role, "login":True }
                return resp, role
            else:
                resp = {'msg': "username/password does not match", 'login':False}
                return resp, None
        else:
            resp = {'msg': "username/password does not match", 'login':False}
            return resp, None
            

    @classmethod
    def create_token(cls, _id, role, fresh = True):
        "create access and refresh token for user"
        access_token = create_access_token({ \
                                        "_id":_id, "role":role}, fresh=datetime. \
                                        datetime.utcnow(), expires_delta \
                                        =datetime.timedelta(minutes=120))
        if fresh == True:
            refresh_token = create_refresh_token({ \
                                "_id":_id, "role":role}, \
                                expires_delta=datetime.\
                                timedelta(minutes=180))
        else:
            refresh_token = None
        return {"access_token":access_token, "refresh_token":refresh_token}
        
@api.route('/login')
class Login(Resource):
    """ Create session for user """
    @classmethod
    @api.expect(Auth.login)
    def post(cls):
        """  Authorize users given by username and password  """
        data, role = Auth.authorise(request.json)
        if data['login'] == True:
            resp = Auth.create_token(data['_id'], role)
            resp.update(data)
            access_token = resp['access_token']
            refresh_token = resp['refresh_token']
            resp = jsonify(resp)
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            LOG.info('Logged in by %s', str(data['_id']+" as "+ data['role']))
            return resp
        else:
            resp ={}
            resp.update(data)
            return resp  

@api.route('/refresh')
class Refresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def put(cls):
        """ To refresh the current user access token """
        current_user = get_jwt_identity()
        resp = Auth.create_token(current_user['_id'],current_user['role'], fresh = False)
        access_token = resp['access_token']
        resp = jsonify(resp)
        LOG.info('Access Token refreshed for %s', str(data['_id']))
        return jsonify({'access_token': access_token})

@api.route('/logout')
class Logout(Resource):
    @classmethod
    @jwt_required
    def delete(cls):
        """To close session of the current user""" 
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        resp = jsonify({"msg": "Successfully logged out"})
        unset_jwt_cookies(resp)
        LOG.info('Logged out by %s', str(data['_id']+" as "+ data['role']))
        return resp
