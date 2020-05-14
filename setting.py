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


class Config():
  DEBUG = False
  TESTING = False
  JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
  JWT_BLACKLIST_ENABLED = True
  JWT_BLACKLIST_TOKEN_CHECKS = [
      "access",
      "refresh",
  ]  


class ProductionConfig(Config):
  MONGODB_SETTINGS = {
    'host': os.environ.get("DATABASE_URL")
  }


class DevelopmentConfig(Config):
  DEBUG = True
  MONGODB_SETTINGS = {
    'db': 'payment-db',
    'host': os.environ.get("DATABASE_URL"),
    'connect': False
  }




class TestingConfig(Config):
  TESTING = True