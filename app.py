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
from db import db 
from resources.collect import Collect, CollectList
from resources.payment import Payment, PaymentList

from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv(".env", verbose=True)

app.config['MONGODB_SETTINGS'] = {
  'host': os.environ.get("DATABASE_URL")
}

api = Api(app)

api.add_resource(Collect, '/collect/<string:name>')
api.add_resource(CollectList, '/collects')
api.add_resource(Payment, '/payment/<string:id>')
api.add_resource(PaymentList, '/payments')



if __name__ == '__main__':
  db.init_app(app)
  app.run(port=5000, debug=True)
