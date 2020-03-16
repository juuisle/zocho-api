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
from blacklist import BLACKLIST
from libs.strings import gettext

from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)


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
    
    user_data = request.get_json()

    user = UserModel.find_by_username(user_data["user_name"])
    if user is None: 
      user = UserModel.find_by_email(user_data["email"])
      if user is None: 
        return {"message": gettext("error_user_not_found")}, 404
    
    try: 
      user.delete()
    except:
      return {"message": gettext("error_user_deleting")}, 500
  
    return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
  """ '/login' endpoint.
  The name of the function is the HTTP methods. 
  """

  def post(self):
    user_data = request.get_json()
    user = UserModel.find_by_username(user_data["user_name"])
    
    if user and safe_str_cmp(user.password, user_data["password"]):
      access_token = create_access_token(user.user_name, fresh=True)
      refresh_token = create_refresh_token(user.user_name)
      return (
          { "access_token": access_token, 
            "refresh_token": refresh_token
          }, 200,
      )
    return {"message": gettext("error_user_invalid_credentials")}, 401



class UserLogout(Resource):
  """ '/userlogin' endpoint.
  The name of the function is the HTTP methods. 
  """
  @jwt_required
  def post(self):
      jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
      user_name = get_jwt_identity()
      BLACKLIST.add(jti)
      return {"message": gettext("user_logged_out").format(user_name)}, 200


class TokenRefresh(Resource):
  pass