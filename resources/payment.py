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


class Payment(Resource):
  """ All API logics of '/collect' endpoint."""

  def get(self, id):
    """ GET method """

    payment = PaymentModel.find_by_id(id)
    if payment: 
      return Response(payment.to_json(), mimetype="application/json", status=200)

    return {'message': gettext("collect_not_found")}

  def post(self, name):
    """ POST method """

    payment_json = request.get_json()
    collect = CollectModel.find_by_name(name)
    if collect:
      try:
        payment = PaymentModel(
          collect_name=name,
          description=payment_json["description"],
          amount=payment_json["amount"]
        )
        payment.save()
      except Exception as ex:
        print(ex)
        return {"message": "An error occurred updating the collect."}, 500
      return Response(payment.to_json(), mimetype="application/json", status=201)
    return {'message': gettext("collect_not_found")}
  

  def put(self, name):
    """ PUT method """

  pass

  def delete(self, id):
    """ DELETE method """

    payment = PaymentModel.find_by_id(id)
    if payment:
      try:
        payment.delete()
      except Exception as ex:
        print(ex)
        return {"message": "An error occurred deleting the collect."}, 500
      return {'message': gettext("collect_deleted")}
    return {'message': gettext("collect_not_found")}

class PaymentList(Resource):
  """ All API logics of '/collect' endpoint."""

  def get(self):
    """ GET method """

    payment_list = PaymentModel.find_all()
    return Response(payment_list.to_json(), mimetype="application/json", status=200)

