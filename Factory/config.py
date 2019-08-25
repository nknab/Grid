'''
File: config.py
Project: AIX 2019 Robotics Final Challenge
File Created: Thursday, 18th July 2019 11:28:45 AM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: This is a configuration file for the entire system. All motors' and
       sensors' ports are set here as well as mqtt topics and other relevant 
       data.
-----
Last Modified: Thursday, 18th July 2019 11:35:09 AM
Modified By: nknab
-----
Copyright ©2019 nknab
'''

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4

Printer = {
    'X_AXIS_MOTOR': OUTPUT_A,
    'Y_AXIS_MOTOR': OUTPUT_B,
    'Z_AXIS_MOTOR': OUTPUT_C,
    'GRABBER_MOTOR': OUTPUT_D,

    'X_AXIS_TS': INPUT_3,
    'Y_AXIS_TS': INPUT_4,

    'X_AXIS_LENGTH': 22.5,
    'Y_AXIS_LENGTH': 24,

    'X_AXIS_GEAR_RADIUS': 1,
    'Y_AXIS_GEAR_RADIUS': 1,
    'LIFT_GEAR_RADIUS': 1,
    'GRABBER_GEAR_RADIUS': 1,

    'Z_AXIS_DROP_LIFT_DISTANCE': 10,
    'MAX_OPEN_GRABBER_DISTANCE': 12.8,
    'PRINTING_Z_DISTANCE': 3.85,

    'ORDER_TOPIC': 'production/order',
    'RP_ROLL_TOPIC': 'roll-paper/roll',
    'RP_READY_TOPIC': 'roll-paper/ready',
    'RP_ORDER_TOPIC': 'roll-paper/order',
    'STATUS_TOPIC': 'production/status',
    'EMERGENCY_STOP_TOPIC': 'production/stop',
    'SERVER': 'grid.local',

    'STAMP_POSITION': [[15, 0], [15, 7.8], [15, 16.6], [15, 23.6]],

    'PRINT_POSITION': [[0, 20], [3.1, 20], [6.2, 20],
                       [0, 15], [3.1, 15], [6.2, 15],
                       [0, 11], [3.1, 11], [6.2, 11]],
    'SPEED': -50

}

Roller = {
    'ROLLER_MOTOR': 'in1:i2c3:M2',
    'FEEDER_MOTOR': 'in1:i2c3:M1',
    'CUT_ROLLER_MOTOR': OUTPUT_A,

    'CS_ONE': INPUT_3,
    'CS_TWO': INPUT_2,
    'CS_THREE': INPUT_4,

    'ORDER_TOPIC': 'production/order',
    'RP_RESET_TOPIC': 'roll-paper/reset',
    'RP_ROLL_TOPIC': 'roll-paper/roll',
    'RP_READY_TOPIC': 'roll-paper/ready',
    'RP_COLOUR_TOPIC': 'roll-paper/colour',
    'DELIVERY_TOPIC': 'production/delivery',
    'CARRIER_TOPIC': 'carrier/control',
    'EMERGENCY_STOP_TOPIC': 'production/stop',
    'CUTTER_TOPIC': 'production/cut',
    'RP_ORDER_TOPIC': 'roll-paper/order',
    'SERVER': 'grid.local',

    'STANDARD_LENGTH': 11.2,
    'CUTTER_DISTANCE': 23,

    'FEEDER_GEAR_RADIUS': 1,
    'CUTTER_GEAR_RADIUS': 1,

    'SPEED': 50
}

Cutter = {
    'FIRST_LIFT_MOTOR': OUTPUT_A,
    'CUTTER_MOTOR': OUTPUT_B,
    'SECOND_LIFT_MOTOR': OUTPUT_C,
    'DISPENSER_MOTOR': OUTPUT_D,

    'CS': INPUT_4,
    'CUTTER_TS': INPUT_3,
    'LIFT_TS': INPUT_2,

    'CUTTER_DISTANCE': 13.5,
    'CUTTER_GEAR_RADIUS': 1,

    'RP_COLOUR_TOPIC': 'roll-paper/colour',
    'CUTTER_TOPIC': 'production/cut',
    'SERVER': 'grid.local',

    'SPEED': 50
}

Carrier = {
    'PRODUCTION_TS': INPUT_4,
    'DELIVERY_TS': INPUT_1,
    'MOTOR': OUTPUT_A,

    'SERVER': 'grid.local',
    'CARRIER_TOPIC': 'carrier/control',

    'SPEED': 50
}

Delivery = {

    'SERVER': 'grid.local',

    'CARRIER_TOPIC': 'carrier/control',
    'STATUS_TOPIC': 'production/status',
    'DELIVERY_TOPIC': 'production/delivery',

    'SPEED': 100
}

MQTT = {
    'PORT': 1883,
    'KEEPALIVE': 60
}
