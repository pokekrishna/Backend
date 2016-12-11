# morse-code-availability.py
import falcon
import json
import mysql.connector


class AvailabilityResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status

        # Query DB
        cnx = mysql.connector.connect(user='alphahc_user', password='bhCLEsjEHwhXb3Jc',
                                      host='hashcustoms-prod-db.cfnhgrdrfrvh.us-west-2.rds.amazonaws.com',
                                      database='alphahashcustoms')
        cursor = cnx.cursor()
        query = ("select customer.booking_slot from customer where booking_confirmed=1  ")
        cursor.execute(query)
        row = cursor.fetchone()

        already_booked = []
        while row is not None:
            already_booked.append(row[0])
            row = cursor.fetchone()
        cursor.close()
        cnx.close()


        complete_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
        available_list = list(set(complete_list).symmetric_difference(already_booked))

        availability_dict = {"availabe": available_list}
        print json.dumps(availability_dict)

        resp.body = (json.dumps(availability_dict))

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
availability = AvailabilityResource()

app.add_route('/morse-code-availability', availability)
