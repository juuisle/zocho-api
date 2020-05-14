# --------------------------------------------------------------------------
# Copyright (c) Lien Tam Buddhist Temple. All rights reserved.
# Licensed under the MIT License. 
# 
# Bachelor's Thesis - Helsinki Metropolia University of Applied Sciences
# Author: Duy Le-Dinh 
# Supervisor: Sami Sainio
# --------------------------------------------------------------------------

from mongoengine import *
from datetime import datetime


class UserModel(Document):
  """ Schema of Users """

  objects = QuerySetManager()
  meta = {'collection': 'user'}

  user_name = StringField(required=True, unique=True)
  password = StringField(required=True)
  email = StringField(unique=True)
  roles = ListField(StringField(default='user'))

  #name = db.StringField()
  active = BooleanField(required=True, default=True)
  time_created = DateTimeField(default=datetime.utcnow())

  @classmethod
  def find_all(cls): 
    return cls.objects()

  @classmethod
  def find_by_username(cls, name):
    try:
      user = cls.objects.get(user_name=name)
    except Exception:
      return None

    return user

  @classmethod
  def find_by_email(cls, email):
    try:
      user = cls.objects.get(email=email)
    except Exception:
      return None

    return user


class PaymentModel(Document):
  """ Schemas for payments that user create. """
  
  objects = QuerySetManager()

  meta = {'collection': 'payment'}
  
  description = StringField()
  amount = DecimalField()
  buyer = StringField()
  invoice_url = StringField()
  invoice_code = StringField()
  note = StringField()
  currency = StringField(default='EUR')
  last_changed = DateTimeField(default=datetime.utcnow())
  time_created = DateTimeField(default=datetime.utcnow())
  collect_name = StringField(required=True)

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


class CollectModel(Document):
  """ Schemas for collect that user create. 
  In this application, 'Collect' mean a set/category of payments. 
  """
  
  objects = QuerySetManager()


  meta = {'collection': 'collect'}

  name = StringField(required=True, unique=True)
  active = BooleanField(required=True, default=True)
  last_changed = DateTimeField(default=datetime.utcnow())
  time_created = DateTimeField(default=datetime.utcnow())

  @classmethod
  def find_all(cls): 
    return cls.objects()

  @classmethod
  def find_by_name(cls, name):
    collect = cls.objects(name=name)
    if not collect:
      return None

    return collect





  
