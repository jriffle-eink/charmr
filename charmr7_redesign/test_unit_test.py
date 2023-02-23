import unittest
import sys
import utils as utils
from model.brightnesstemperaturemenu import *
from model.basemenu import *
from model.slideshow import *
from utils import clock
from cmodule import charmr_module as cm



#TESTS FOR UTIL CLASS

class Test_Class(unittest.TestCase):
    
    def test_clock(self):
        time = utils.clock()

        self.assertEqual(time, 0)


class Test_BrightnessTemp(unittest.TestCase):

    def test_brightness_temperature_slider(self):

        bght_temp_menu = BrightnessTemperatureMenu()

        # validating initial state
        self.assertEqual("bght", bght_temp_menu.cur_type)
        self.assertEqual(None, bght_temp_menu.current_brightness)
        self.assertEqual(None, bght_temp_menu.current_temperature)
        self.assertEqual(0, bght_temp_menu.cur_check)

        # changing brightness works, temp unaffected
        touch_location1 = [960, 1800]
        bght_temp_menu.brightness_temperature_slider(touch_location1)

        self.assertEqual(0, bght_temp_menu.cur_check)
        self.assertEqual(0, bght_temp_menu.current_brightness)

        self.assertEqual(None, bght_temp_menu.current_temperature)

        touch_location2 = [570, 1731]
        bght_temp_menu.brightness_temperature_slider(touch_location2)

        self.assertEqual(8, bght_temp_menu.cur_check)
        self.assertEqual(80, bght_temp_menu.current_brightness)

        self.assertEqual(None, bght_temp_menu.current_temperature)

        # can't change to invalid type
        bght_temp_menu.select_type("INVALID")
        self.assertEqual("bght", bght_temp_menu.cur_type)

        # can change to valid type
        bght_temp_menu.select_type("temp")
        self.assertEqual("temp", bght_temp_menu.cur_type)

        # changing temp works, brightness unaffected
        touch_location3 = [620, 1750]
        bght_temp_menu.brightness_temperature_slider(touch_location3)

        self.assertEqual(7, bght_temp_menu.cur_check)
        self.assertEqual(70, bght_temp_menu.current_temperature)

        self.assertEqual(80, bght_temp_menu.current_brightness)

        # invalid location has no impact
        touch_location4 = [477, 1730]
        bght_temp_menu.brightness_temperature_slider(touch_location4)

        self.assertEqual(7, bght_temp_menu.cur_check)
        self.assertEqual(70, bght_temp_menu.current_temperature)

        self.assertEqual(80, bght_temp_menu.current_brightness)

class Test_Slideshow(unittest.TestCase):

    def test_init(self):

        sshw = Slideshow(1)

        # validating initial state
        self.assertEqual(0, sshw.cur_slide)
        #self.assertEqual(cm.slideshow1, sshw.cm_slideshow)
        self.assertEqual(15, sshw.length)


class Test_Controller(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()