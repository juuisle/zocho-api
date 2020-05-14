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

from database.models import PlantCategoryModel, PlantModel
from libs.strings import gettext


class Plant(Resource):

  @fresh_jwt_required
  def get(self, query):
    """ Return the requested plant """
    
    plant_id = query
    plant = PlantModel.find_by_id(plant_id)
    if plant is None:
      return {'message': gettext("error_plant_not_found")}, 404

    return Response(plant.to_json(), mimetype="application/json", status=200)
  
  @fresh_jwt_required
  def post(self, query):
    category_name = query
    plant_data = request.get_json()
    category = PlantCategoryModel.find_by_name(category_name)
    if category is None:
      return {'message': gettext("error_plant_category_not_found")}, 404

    try:
      plant = PlantModel(
        category=category_name,
        **plant_data
      )
      plant.save()
    except:
      return {"message": gettext("error_plant_updating")}, 500
      
    return Response(plant.to_json(), mimetype="application/json", status=201)

  def put(self, name):
    pass
  
  @jwt_required
  def delete(self, query):
    plant_id = query
    plant = PlantModel.find_by_id(plant_id)
    if plant is None:
      return {'message': gettext("error_plant_not_found")}, 404

    try:
      plant.delete()
    except:
      return {"message": gettext("error_plant_deleting")}, 500

    return {'message': gettext("plant_deleted")}, 200

class PlantList(Resource):
  def get(self):
    """ Get all plants that users have """

    plant_list = PlantModel.find_all()
    return Response(plant_list.to_json(), mimetype="application/json", status=200)