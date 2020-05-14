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


class PlantCategory(Resource):

  @fresh_jwt_required
  def get(self, name):
    plant = PlantCategoryModel.find_by_name(name)
    if plant is None: 
      return {'message': gettext("error_plant_category_not_found")}, 404

    return Response(plant.to_json(), mimetype="application/json", status=200)
  
  @fresh_jwt_required
  def post(self, name):
    if PlantCategoryModel.find_by_name(name):
      return {'message': gettext("error_plant_category_exists").format(name)}, 400

    PlantCategory = PlantCategoryModel(name=name)  
    try:
      PlantCategory.save()
    except:
      return {"message": gettext("error_plant_category_creating")}, 500

    return Response(PlantCategory.to_json(), mimetype="application/json", status=201)
  
  @fresh_jwt_required
  def put(self, name):
    new_name = request.get_json()["new_name"]

    if PlantCategoryModel.find_by_name(new_name) == True:
      return {"message": gettext("error_plant_category_exists").format(new_name)}, 400

    PlantCategory = PlantCategoryModel.find_by_name(name)
    if PlantCategory is None:
      return {'message': gettext("error_plant_category_not_found")}, 404

    try:
      PlantCategory.update(name=new_name)
      PlantModel.find_by_PlantCategory_name(name).update(PlantCategory_name=new_name)
    except:
      return {"message": gettext("erro_plant_category_updating")}, 500

    return {'message': gettext("plant_category_updated")}, 200
  
  @jwt_required
  def delete(self, name):

    PlantCategory = PlantCategoryModel.find_by_name(name)
    if PlantCategory is None:
      return {'message': gettext("error_plant_category_not_found")}

    try:
      PlantCategory.delete()
      PlantModel.find_by_PlantCategory_name(name).delete()
    except:
      return {"message": gettext("error_plant_category_deleting")}, 500

    return {'message': gettext("plant_category_deleted")}, 200


class PlantCategoryList(Resource):

  @fresh_jwt_required
  def get(self):

    PlantCategory = PlantCategoryModel.find_all()
    return Response(PlantCategory.to_json(), mimetype="application/json", status=200)

