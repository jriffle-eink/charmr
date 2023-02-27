from basemenu import BaseMenu

from pausesettingsmenu import PauseSettingsMenu

import charmr_module as cm

''' 
Controls the internal state of the pause menu.
'''
class Pause():
    def __init__(self, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):

        self.pause_settings = PauseSettingsMenu()

        #self.sketch = launch_pause_sketch()

    '''
    Sends user input to the settings field to process
    '''
    def process_settings_input(self, user_input):
        pass
