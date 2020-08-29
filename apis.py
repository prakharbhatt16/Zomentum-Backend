from flask import *
from flask_restful import *
from collections import defaultdict

class Booking(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['database']
        self.session = kwargs['session']

    def get(self):
        """
        Arguments:
            if get all:
                'ticketId' : <str : 0 = all>
                'year' : <int>
                'month' : <int>
                'day' : <int>
                'hour' : <int>
            else:
                'ticketId' : <str : != 0>
        """
        obj = dict(request.args)
        
        try:
            if obj['ticketId'] == '0':
                obj['timing'] = obj
                results, status = self.db.getTickets(obj)
            else:
                results, status = self.db.getTicket(obj)
            if status is False:
                raise results
            return results, 200
        except Exception as e:
            print("Error occured in Booking Get", e)
            return {'status':e}, 500

    def post(self):
        """
        # Create ticket
        Request format:
        {
            "user" : <str> {Name of the user}
            "phone" : <10 digit integer string> {Phone number of the user}
            "timing" : {
                    'year' : <int>
                    'month' : <int>
                    'day' : <int>
                    'hour' : <int>
                }
        }
        """
        obj = request.get_json(force=True)

        try:
            results, status = self.db.createTicket(obj)
            if status is False:
                raise results
            return results, 200
        except Exception as e:
            print("Error occured in Booking post", e)
            return {'status':e}, 500
    
    def put(self):
        """
        # Create ticket
        Request format:
        {
            if update:
                "ticketId" : <str ObjectId>,
                'timing' : {
                        'year' : <int>
                        'month' : <int>
                        'day' : <int>
                        'hour' : <int>
                    }
            else create:
                "user" : <str> {Name of the user}
                "phone" : <10 digit integer string> {Phone number of the user}
                "timing" : {
                        'year' : <int>
                        'month' : <int>
                        'day' : <int>
                        'hour' : <int>
                    }
        }
        """
        obj = request.get_json(force=True)

        try:
            if 'ticketId' in obj:
                results, status = self.db.updateTicket(obj)
            else:
                results, status = self.db.createTicket(obj)
            if status is False:
                raise results
            return results, 200
        except Exception as e:
            print("Error occured in Booking Put", e)
            return {'status':e}, 500

    def delete(self):
        """
        # Delete ticket
        Request format:
        {
            "ticketId" : <str ObjectId> {}
        }
        """
        obj = request.get_json(force=True)
        
        try:
            results, status = self.db.deleteTicket(obj)
            if status is False:
                raise results
            return results, 200
        except Exception as e:
            print("Error occured in Booking delete", e)
            return {'status':e}, 500