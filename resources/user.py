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
from database.models import UserModel
from libs.strings import gettext


class UserManagement(Resource):
  """ '/user' endpoint.
  The name of the function is the HTTP methods. 
  This application is for internal use. Therefore, all users will be
  created and managed my administrator
  """

  def get(self):
    pass

  def post(self):
    """ Create new user """

    user_data = request.get_json()

    if UserModel.find_by_username(user_data["user_name"]):
      return {"message": gettext("error_user_exists")}, 400
    
    if UserModel.find_by_email(user_data["email"]):
      return {"message": gettext("error_user_exists")}, 400
    
    user = UserModel(**user_data)
    try:
      user.save()
    except:
      return {"message": gettext("error_user_creating")}, 500
    
    return Response(user.to_json(), mimetype="application/json", status=200)

  def delete(self):
    """ Delete user """
    
    user_name = request.get_json()["user_name"]

    user = UserModel.find_by_username(user_name)
    if user is None: 
      return {"message": gettext("error_user_not_found")}, 404
    
    try: 
      user.delete()
    except:
      return {"message": gettext("error_user_deleting")}, 500
  
    return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
  """ '/userlogin' endpoint.
  The name of the function is the HTTP methods. 
  """

  def post(self):
    pass

class UserLogout(Resource):
  """ '/userlogin' endpoint.
  The name of the function is the HTTP methods. 
  """

  def post(self):
    pass

class TokenRefresh(Resource):
  pass