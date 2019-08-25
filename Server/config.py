'''
File: config.py
Project: Grid Server
File Created: Saturday, 20th July 2019 11:17:34 PM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: This is a configuration file for the server. The Mqtt topic and 
       Database credentials are set here.
-----
Last Modified: Sunday, 21st July 2019 7:06:08 AM
Modified By: nknab
-----
Copyright ©2019 nknab
'''


MQTT = {
    'PORT': 1883,
    'KEEPALIVE': 60,
    'TOPIC': 'production/status'
}

Database = {
    "HOST": "localhost",
    "USER": "root",
    "PASSWORD": "",
    "DATABASE": "grid"
}
