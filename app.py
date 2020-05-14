# -------------------------------------------------------------------------------------------------
# Zocho-Ten Smart Ecosystem
#
# The MIT License (MIT)
# Copyright © 2020 Juuis Le
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
# and associated documentation files (the “Software”), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software 
# is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies 
# or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# -------------------------------------------------------------------------------------------------

import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from flask_mongoengine import MongoEngine
from resources.collect import Collect, CollectList
from resources.payment import Payment, PaymentList
from resources.plant import Plant, PlantList
from resources.plant_category import PlantCategory, PlantCategoryList
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

db = MongoEngine(app)
# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

api.add_resource(Collect, '/collect/<string:name>')
api.add_resource(CollectList, '/collects')
api.add_resource(Payment, '/payment/<string:query>')
api.add_resource(PaymentList, '/payments')

api.add_resource(Plant, '/plant/<string:query>')
api.add_resource(PlantList, '/plants')
api.add_resource(PlantCategory, '/plantcategory/<string:name>')
api.add_resource(PlantCategoryList, '/plantcategories')
api.add_resource(UserManagement, '/user')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

@app.route('/')
def home():
  return os.environ.get("TEST")

if __name__ == '__main__':
 # db.init_app(app)
  app.run(port=5000, debug=True)
