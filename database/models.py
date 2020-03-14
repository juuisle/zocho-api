# --------------------------------------------------------------------------
# Copyright (c) Lien Tam Buddhist Temple. All rights reserved.
# Licensed under the MIT License. 
# 
# Bachelor's Thesis - Helsinki Metropolia University of Applied Sciences
# Author: Duy Le-Dinh 
# Supervisor: Sami Sainio
# --------------------------------------------------------------------------

from db import db
from bson import ObjectId
from datetime import datetime

class PaymentModel(db.EmbeddedDocument):
  """ Schemas for payments that user create. """

  description = db.StringField()
  amount = db.DecimalField()
  currency = db.StringField(default='EUR')
  last_changed = db.DateTimeField(default=datetime.utcnow())
  time_created = db.DateTimeField(default=datetime.utcnow())


class CollectModel(db.Document):
  """ Schemas for collect that user create. 
  In this application, 'Collect' mean a set/category of payments. 
  """

  meta = {'collection': 'collect'}

  name = db.StringField(required=True, unique=True)
  active = db.BooleanField(required=True, default=True)
  last_changed = db.DateTimeField(default=datetime.utcnow())
  time_created = db.DateTimeField(default=datetime.utcnow())
  payments = db.EmbeddedDocumentListField(PaymentModel)

  @classmethod
  def find_all(cls): 
    return cls.objects()

  @classmethod
  def find_by_name(cls, name):
    collect = cls.objects(name=name)
    if collect != '[]':
      return collect
    return False





  
