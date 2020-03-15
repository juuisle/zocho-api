# --------------------------------------------------------------------------
# Copyright (c) Lien Tam Buddhist Temple. All rights reserved.
# Licensed under the MIT License. 
# 
# Bachelor's Thesis - Helsinki Metropolia University of Applied Sciences
# Author: Duy Le-Dinh 
# Supervisor: Sami Sainio
# --------------------------------------------------------------------------

from db import db
from datetime import datetime

class PaymentModel(db.Document):
  """ Schemas for payments that user create. """

  meta = {'collection': 'payment'}
  
  description = db.StringField()
  amount = db.DecimalField()
  buyer = db.StringField()
  invoice_url = db.StringField()
  invoice_code = db.StringField()
  note = db.StringField()
  currency = db.StringField(default='EUR')
  last_changed = db.DateTimeField(default=datetime.utcnow())
  time_created = db.DateTimeField(default=datetime.utcnow())
  collect_name = db.StringField(required=True)

  @classmethod
  def find_all(cls): 
    return cls.objects()
  
  @classmethod
  def find_by_collect_name(cls, collect_name):
    payments = cls.objects(collect_name=collect_name)
    if not payments:
      return None

    return payments
  
  @classmethod
  def find_by_id(cls, id):
    payment = cls.objects(id=id)
    if not payment:
      return None

    return payment


class CollectModel(db.Document):
  """ Schemas for collect that user create. 
  In this application, 'Collect' mean a set/category of payments. 
  """

  meta = {'collection': 'collect'}

  name = db.StringField(required=True, unique=True)
  active = db.BooleanField(required=True, default=True)
  last_changed = db.DateTimeField(default=datetime.utcnow())
  time_created = db.DateTimeField(default=datetime.utcnow())

  @classmethod
  def find_all(cls): 
    return cls.objects()

  @classmethod
  def find_by_name(cls, name):
    collect = cls.objects(name=name)
    if not collect:
      return None

    return collect





  
