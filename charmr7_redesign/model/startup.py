from basemenu import BaseMenu
from mainsettingsmenu import MainSettingsMenu
import charmr_module as cm
from view import Display
from model.slideshow import Slideshow
import os

class Startup():
    
    def __init__(self):
        
        self.view = Display()

        self.view.display_startup()
        
    def clear(self):
        
        self.view.clear('best')
        
