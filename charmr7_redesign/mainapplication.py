import charmr_module as cm
import os
import sys
import signal
import time
import math
import subprocess
import numpy as np
import datetime
import threading
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

class DemoModel():
    
#current menu field (pause/flash/main etc.)
#game
#sketch
#slideshow

    def __init__():

        self.bght_temp_menu = BrightnessTemperatureMenu()

        self.main_menu = MainMenu()
        
        self.sketch = Sketch()

        self.wfm_transition_dict = {'dictionary of waveform transitions'}

        self.current_application = 'main'

    # # what menu/element is currently displayed, so the view knows what to display
    # self.current_element

    # #low-level system monitoring
    # self.device_monitoring = None

    # def update_slider(user_input: list):
    #     self.bght_temp_menu.brightness_temperature_slider(user_input)

