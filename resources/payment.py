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


class Payment(Resource):
  """ '/payment' endpoint.
  The name of the function is the HTTP methods. 
  """
  @fresh_jwt_required
  def get(self, query):
    """ Return the requested payment """
    
    payment_id = query
    payment = PaymentModel.find_by_id(payment_id)
    if payment is None:
      return {'message': gettext("error_payment_not_found")}, 404

    return Response(payment.to_json(), mimetype="application/json", status=200)
  
  @fresh_jwt_required
  def post(self, query):
    """ Add payment to collect """

    collect_name = query
    payment_data = request.get_json()
    collect = CollectModel.find_by_name(collect_name)
    if collect is None:
      return {'message': gettext("error_collect_not_found")}, 404

    try:
      payment = PaymentModel(
        collect_name=collect_name,
        **payment_data
      )
      payment.save()
    except:
      return {"message": gettext("error_payment_updating")}, 500
      
    return Response(payment.to_json(), mimetype="application/json", status=201)

  def put(self, name):
    """ Update payment's data """
  pass
  
  @jwt_required
  def delete(self, query):
    """ Delete the entire payment """

    payment_id = query
    payment = PaymentModel.find_by_id(payment_id)
    if payment is None:
      return {'message': gettext("error_payment_not_found")}, 404

    try:
      payment.delete()
    except:
      return {"message": gettext("error_payment_deleting")}, 500

    return {'message': gettext("payment_deleted")}, 200

class PaymentList(Resource):
  """ '/payments' endpoint.
  The name of the function is the HTTP methods. 
  """

  def get(self):
    """ Get all payments that users have """

    payment_list = PaymentModel.find_all()
    return Response(payment_list.to_json(), mimetype="application/json", status=200)

