# --------------------------------------------------------------------------
# Copyright (c) Lien Tam Buddhist Temple. All rights reserved.
# Licensed under the MIT License. 
# 
# Bachelor's Thesis - Helsinki Metropolia University of Applied Sciences
# Author: Duy Le-Dinh 
# Supervisor: Sami Sainio
# --------------------------------------------------------------------------

from flask import Response
from flask_restful import Resource
from database.models import CollectModel
from libs.strings import gettext


MESSAGE_NOT_FOUND = 'Collect not found, please contact administrators'

class Collect(Resource):
  """ All API logics of '/collect' endpoint."""

  def get(self, name):
    """ GET method """

    collect = CollectModel.find_by_name(name)
    if collect: 
      return Response(collect, mimetype="application/json", status=200)

    return {'message': gettext("collect_not_found")}

  def post(self, name):
    """ POST method """

    name = 'Test'
    if CollectModel.find_by_name(name):
      return {'message': "A store with name '{}' already exists.".format(name)}, 400

    collect = CollectModel(name)  
    try:
      collect.save()
    except:
      return {"message": "An error occurred creating the collect."}, 500

    return collect.to_json(), 201

    def delete(self, name):
      """ DELETE method """

      collect = CollectModel.find_by_name(name)
      if collect:
        try:
          collect.delete()
        except:
          return {"message": "An error occurred deleting the collect."}, 500
        return {'message': gettext("collect_not_found")}
      return {'message': gettext("collect_not_found")}

class CollectList(Resource):
  """ All API logics of '/collect' endpoint."""

  def get(self):
    """ GET method """

    collect = CollectModel.find_all()
    return Response(collect, mimetype="application/json", status=200)

