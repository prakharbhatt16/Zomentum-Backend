import os
import random
import string
from flask import *
from flask_restful import *
from flask_sessionstore import Session
import json

import database
import apis
import logger

from datetime import datetime

from apscheduler.scheduler import Scheduler

app = Flask(__name__, template_folder='frontend/template', static_folder='frontend/static')
app.config.update(
    DATABASE='Zomentum'
)
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)

global db
db = database.Database("mongodb://localhost:27017/zomentum")

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.urandom(32)

#######################################################################################################################
################################################### Utility Functions #################################################
#######################################################################################################################


def manage_error(func):
    @wraps(func)
    def function_wrapper(*args, **kwarg):
        try:
            result = func(*args, **kwarg)
            return result
        except Exception as e:
            print("Error in %s" % request.path, e)
            log.error(request.path, request, session, e)
            return render_template("/errors/500.html")
    return function_wrapper

cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()

@cron.interval_schedule(hours=8)
def expireTickets():
    global db
    alltickets = db.getAllTickets()
    now = datetime.now()
    for ticket in alltickets:
        if (now - ticket['timestamp']) / 3600 >= 8:
            db.deleteTicket(ticket)


#######################################################################################################################
##################################################### RESTFUL APIS ####################################################
#######################################################################################################################

api = Api(app)
apiv1_uri = '/api/v1/'

api.add_resource(apis.Booking, apiv1_uri + 'booking',
                 resource_class_kwargs={'database': db, 'session': session})

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
