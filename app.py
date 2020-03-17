# --------------------------------------------------------------------------
# Copyright (c) Lien Tam Buddhist Temple. All rights reserved.
# Licensed under the MIT License. 
# 
# Bachelor's Thesis - Helsinki Metropolia University of Applied Sciences
# Author: Duy Le-Dinh 
# Supervisor: Sami Sainio
# --------------------------------------------------------------------------

import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db 
from resources.collect import Collect, CollectList
from resources.payment import Payment, PaymentList
from resources.user import UserManagement, UserLogin, UserLogout, TokenRefresh
from blacklist import BLACKLIST

from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv(".env", verbose=True)
# Load config from setting.py
app.config.from_object("setting.DevelopmentConfig")  
api = Api(app)

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

api.add_resource(Collect, '/collect/<string:name>')
api.add_resource(CollectList, '/collects')
api.add_resource(Payment, '/payment/<string:query>')
api.add_resource(PaymentList, '/payments')
api.add_resource(UserManagement, '/user')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

@app.route('/')
def home():
  return os.environ.get("TEST")


db.init_app(app)
app.run(port=5000, debug=True)
