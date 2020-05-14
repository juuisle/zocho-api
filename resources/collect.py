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

from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, fresh_jwt_required

from database.models import CollectModel, PaymentModel
from libs.strings import gettext


class Collect(Resource):
  """ '/collect' endpoint.
  The name of the function is the HTTP methods. 
  """
  
  @fresh_jwt_required
  def get(self, name):
    """ Return collection of payments """

    payments = PaymentModel.find_by_collect_name(name)
    if payments is None: 
      return {'message': gettext("error_collect_not_found")}, 404

    return Response(payments.to_json(), mimetype="application/json", status=200)
  
  @fresh_jwt_required
  def post(self, name):
    """ Create new Collect and save to MongoDB """

    if CollectModel.find_by_name(name):
      return {'message': gettext("error_collect_exists").format(name)}, 400

    collect = CollectModel(name=name)  
    try:
      collect.save()
    except:
      return {"message": gettext("error_collect_creating")}, 500

    return Response(collect.to_json(), mimetype="application/json", status=201)
  
  @fresh_jwt_required
  def put(self, name):
    """ Update Collect's name """

    new_name = request.get_json()["new_name"]

    if CollectModel.find_by_name(new_name) == True:
      return {"message": gettext("error_collect_exists").format(new_name)}, 400

    collect = CollectModel.find_by_name(name)
    if collect is None:
      return {'message': gettext("error_collect_not_found")}, 404

    try:
      collect.update(name=new_name)
      PaymentModel.find_by_collect_name(name).update(collect_name=new_name)
    except:
      return {"message": gettext("error_collect_updating")}, 500

    return {'message': gettext("collect_updated")}, 200
  
  @jwt_required
  def delete(self, name):
    """ Delete the entire Collect """

    collect = CollectModel.find_by_name(name)
    if collect is None:
      return {'message': gettext("error_collect_not_found")}

    try:
      collect.delete()
      PaymentModel.find_by_collect_name(name).delete()
    except:
      return {"message": gettext("error_collect_deleting")}, 500

    return {'message': gettext("collect_deleted")}, 200


class CollectList(Resource):
  """ '/collects' endpoint.
  The name of the function is the HTTP methods. 
  """
  
  @fresh_jwt_required
  def get(self):
    """ Return the list of saved collects """

    collect = CollectModel.find_all()
    return Response(collect.to_json(), mimetype="application/json", status=200)

