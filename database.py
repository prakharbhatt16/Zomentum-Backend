import pymongo
import json
from pymongo.write_concern import WriteConcern
# from pymodm import * #MongoModel, fields
import pymodm
from pymodm import EmbeddedMongoModel, MongoModel, fields, ReferenceField
from bson.objectid import ObjectId
from bson import SON
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

import re
import time
import secrets

from pymodm.connection import connect

import logger
from functools import wraps
from datetime import date, datetime, timedelta

log = logger.Logger('logs/dblogs.json')

class Ticket(MongoModel):
    ticketId = fields.CharField(primary_key=True)
    userName = fields.CharField()
    phoneNumber = fields.CharField(max_length=10, min_length=10)
    timing = fields.DateTimeField()
    timestamp = fields.IntegerField()

def classToDict(obj, default=None):
    """
    Wraps class into a dict, assigning 'default' value to fields not existing in the obj
    """
    final = {}
    refClass = obj.__class__
    refItems = vars(refClass)
    for key in refItems:
        if key[0] == '_' or key in ['DoesNotExist', 'MultipleObjectsReturned', 'objects']:
            continue
        if key in obj:
            final[key] = getattr(obj, key)
            if type(type(final[key])) == pymodm.base.models.MongoModelMetaclass:
                final[key] = classToDict(final[key])
        else:
            final[key] = default
    return final

def getTimeSlot(timing):
    # Round off timing to nearest hour
    t = datetime(
        int(timing['year']), 
        int(timing['month']), int(timing['day']), int(timing['hour']))
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour) + timedelta(hours=t.minute//30))

def manage_error(returns=1):
    def wrapper(func):
        @wraps(func)
        def function_wrapper(*args, **kwarg):
            try:
                result = func(*args, **kwarg)
                return result
            except Exception as e:
                log.error(func.__name__, None, None, e)
                if returns == 1:
                    return None
                elif returns == 2:
                    return None, False
        return function_wrapper
    return wrapper

class Database:
    def __init__(self, url="mongodb://localhost:27017/zomentum"):
        try:
            connect(url, alias="default")
        except Exception as e:
            print("Connection with MongoDB Failed!")
            print(e)
        return

    @manage_error()
    def initFresh(self):
        print("Initializing Database a fresh")
        connect("mongodb://localhost:27017/zomentum", alias="default")
        print("Done!")

    @manage_error()
    def createTicket(self, data):
        # Verify there are < 200 tickets in the slot!
        tickets, status = self.getTickets(data)
        if status is False or len(tickets) >= 20:
            return {"status":"Too much tickets! >20"}, False
        ticket = Ticket(
            ticketId = str(ObjectId()),
            userName = data['user'],
            phoneNumber = data['phone'],
            timing = getTimeSlot(data['timing']),
            timestamp = time.time()
        )
        ticket.save()
        return classToDict(ticket), True

    @manage_error(returns=2)
    def getUser(self, data):
        ticket = Ticket.objects.get({'_id': data['ticketId']})
        if ticket == None:
            return None, False
        return {'user':ticket.userName, 'phone':ticket.phoneNumber}, True

    @manage_error(returns=2)
    def getAllTickets(self):
        ticket = Ticket.objects.all()
        if ticket == None:
            return None, False
        return [classToDict(i) for i in ticket], True

    @manage_error(returns=2)
    def getTicket(self, data):
        ticket = Ticket.objects.get({'_id': data['ticketId']})
        if ticket == None:
            return None, False
        return classToDict(ticket), True

    @manage_error(returns=2)
    def updateTicket(self, data):
        ticket = Ticket.objects.get({'_id': data['ticketId']})
        if ticket is None:
            return None, False
        ticket.timing = getTimeSlot(data['timing'])
        ticket.save()
        return classToDict(ticket), True

    @manage_error(returns=2)
    def getTickets(self, data):
        timing = getTimeSlot(data['timing'])
        tickets = [i.ticketId for i in Ticket.objects.raw({'timing':timing})]
        return tickets, True

    @manage_error(returns=2)
    def deleteTicket(self, data):
        ticket = Ticket.objects.get({'_id' : data['ticketId']})
        if ticket is None:
            return None, False
        ticket.delete()
        return {"status":"Done"}, True
        
        # return tickets

    

