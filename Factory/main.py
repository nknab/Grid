#!/usr/bin/env python3

'''
File: main.py
Project: AIX 2019 Robotics Final Challenge
File Created: Friday, 24th May 2019 6:35:52 AM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: The main provides an interface to the user to select which program 
       to be run.
-----
Last Modified: Thursday, 18th July 2019 11:35:20 AM
Modified By: nknab
-----
Copyright ©2019 nknab
'''

import os
import subprocess


from carrier import *
from delivery import *
from production import *

from PIL import Image
from time import sleep

from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.display import Display

# Setting my font type and size.
os.system('setfont Lat15-TerminusBold14')

# Declaring and instantiating the various classes.
btn = Button()
lcd = Display()
sound = Sound()


# What should be executed when the LEFT button is pressed.
def left(state):
    if state:
        sound.beep()
        lcd.clear()
        logo = Image.open('/home/robot/Grid/bmps/printing.bmp')
        lcd.image.paste(logo, (0, 0))
        lcd.update()
        prin = printer.Printer()
        prin.run()


# What should be executed when the UP button is pressed.
def up(state):
    if state:
        sound.beep()
        lcd.clear()
        logo = Image.open('/home/robot/Grid/bmps/carrier.bmp')
        lcd.image.paste(logo, (0, 0))
        lcd.update()
        carr = carrier.Carrier()
        carr.run()


# What should be executed when the RIGHT button is pressed.
def right(state):
    if state:
        sound.beep()
        lcd.clear()
        logo = Image.open('/home/robot/Grid/bmps/roller.bmp')
        lcd.image.paste(logo, (0, 0))
        lcd.update()
        roll = roller.Roller()
        roll.run()


# What should be executed when the DOWN button is pressed.
def down(state):
    if state:
        sound.beep()
        lcd.clear()
        logo = Image.open('/home/robot/Grid/bmps/cutter.bmp')
        lcd.image.paste(logo, (0, 0))
        lcd.update()
        cut = cutter.Cutter()
        cut.run()


# What should be executed when the ENTER button is pressed.
def enter(state):
    if state:
        sound.beep()
        lcd.clear()
        logo = Image.open('/home/robot/Grid/bmps/delivery.bmp')
        lcd.image.paste(logo, (0, 0))
        lcd.update()
        deliv = delivery.Delivery()
        deliv.run()


# Assigning the various on button functions to their preprogrammed class.
btn.on_left = left
btn.on_up = up
btn.on_right = right
btn.on_down = down
btn.on_enter = enter

# Making sure mosquitto is running on the brick.
subprocess.call(
    'echo maker| sudo -S systemctl restart mosquitto', shell=True)

# Displaying the various programs on the screen with their corresponding buttons.
print ('Select Program\n')
print ('Left Btn: Printer')
print ('Up Btn: Carrier')
print ('Right Btn: Roller')
print ('Down Btn: Cutter')
print ('Enter Btn: Delivery')


# Waiting for a command from the user.
while True:
    btn.process()
    sleep(0.01)
