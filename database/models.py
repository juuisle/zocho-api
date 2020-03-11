# --------------------------------------------------------------------------
# Copyright (c) Lien Tam Buddhist Temple. All rights reserved.
# Licensed under the MIT License. 
# 
# Bachelor's Thesis - Helsinki Metropolia University of Applied Sciences
# Author: Duy Le-Dinh 
# Supervisor: Sami Sainio
# --------------------------------------------------------------------------

from db import db

class PaymentModel(db.EmbeddedDocument):
  """ Schemas for payments that user create. """

  name = db.StringField(required=True, unique=True)
  amount = db.IntField()

class CollectModel(db.Document):
  """ Schemas for collect that user create. 
  In this application, 'Collect' mean a set/category of payments. 
  """

  meta = {'collection': 'collect'}

  name = db.StringField(required=True, unique=True)
  payments = db.ListField(db.EmbeddedDocumentField(PaymentModel))

  @classmethod
  def find_all(cls): 
    return cls.objects().to_json()

  @classmethod
  def find_by_name(cls, name):
    collect = cls.objects(name=name).to_json()
    if collect != '[]':
      return collect
    return False





  
