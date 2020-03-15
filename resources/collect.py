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
from database.models import CollectModel, PaymentModel
from libs.strings import gettext


class Collect(Resource):
  """ All API logics of '/collect' endpoint."""

  def get(self, name):
    """ GET method
    Return: collection of payments
    """

    collect = PaymentModel.find_by_collect_name(name)
    if collect: 
      return Response(collect.to_json(), mimetype="application/json", status=200)

    return {'message': gettext("collect_not_found")}

  def post(self, name):
    """ POST method """

    if CollectModel.find_by_name(name):
      return {'message': "A store with name '{}' already exists.".format(name)}, 400

    #payments = [PaymentModel(description='test', amount=40)]
    collect = CollectModel(name=name)  
    try:
      collect.save()
    except Exception as ex:
      print(ex)
      return {"message": "An error occurred creating the collect."}, 500

    return Response(collect.to_json(), mimetype="application/json", status=201)
  

  def put(self, name):
    """ PUT method """

    req = request.get_json()
    collect = CollectModel.find_by_name(name)
    if collect and CollectModel.find_by_name(req["new_name"]) == False:
      try:
        collect.update(name=req["new_name"])
        payments = PaymentModel.find_by_collect_name(name)

        for payment in payments:
          payments.update(collect_name=req["new_name"])

      except Exception as ex:
        print(ex)
        return {"message": "An error occurred updating the collect."}, 500
      return {'message': gettext("collect_updated")}
    return {'message': gettext("error_occured")}

  def delete(self, name):
    """ DELETE method """

    collect = CollectModel.find_by_name(name)
    if collect:
      try:
        collect.delete()
      except Exception as ex:
        print(ex)
        return {"message": "An error occurred deleting the collect."}, 500
      return {'message': gettext("collect_deleted")}
    return {'message': gettext("collect_not_found")}

class CollectList(Resource):
  """ All API logics of '/collect' endpoint."""

  def get(self):
    """ GET method """

    collect = CollectModel.find_all()
    return Response(collect.to_json(), mimetype="application/json", status=200)

