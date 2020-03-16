# --------------------------------------------------------------------------
# Copyright (c) Lien Tam Buddhist Temple. All rights reserved.
# Licensed under the MIT License. 
# 
# Bachelor's Thesis - Helsinki Metropolia University of Applied Sciences
# Author: Duy Le-Dinh 
# Supervisor: Sami Sainio
# --------------------------------------------------------------------------

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

