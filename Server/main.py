'''
File: main.py
Project: Grid Server
File Created: Saturday, 20th July 2019 9:48:26 PM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: The main allows information to be sent to the server for processing,=.
-----
Last Modified: Sunday, 21st July 2019 7:06:26 AM
Modified By: nknab
-----
Copyright ©2019 nknab
'''

import json
import logging

from database import *
from mqtt import subscriber
from config import MQTT as MQTT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Declaring and instantiating my database class.
db = database.Database()


while True:
    data = None
    logger.info('Waiting For Order Status Update')
    # Subscribing and waiting for the data.
    sub = subscriber.Subscriber("localhost")
    try:
        data = json.loads(sub.subscribe(MQTT['TOPIC']))
        logger.info('Update: %s', data)

    except:
        logger.error('In Valid Message')

    # Cross checking if the data received is valid.
    if data != None and data["Status"] in ["Production", "In Delivery", "Done"]:
        logger.info('Updating Order Status...')
        status = "1"
        if data["Status"] == "Production":
            status = "2"
        elif data["Status"] == "In Delivery":
            status = "3"
        elif data["Status"] == "Done":
            status = "4"

        # Updating the database with the correct status
        db.update(str(data["OrderID"]), status)
        logger.info('Order Status Update Finished \n')
    else:
        logger.error('In Valid Status \n')
