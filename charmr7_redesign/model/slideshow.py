import threading
from pausesettingsmenu import PauseSettingsMenu
import sys 
sys.path.append('cmodule')

import charmr_module as cm


'''
Responsible for monitoring the state of the slideshow

PARAMETERS
slideshow_num: int (which charmr module slideshow info should be used)
'''
class Slideshow():

    def __init__(self, slideshow_num):

        # the current slide of the slideshow
        self.cur_slide = 0

        """
        Changes the slideshow number to the number placed in argument.
        """    

        '''
        The charmr module slideshow is stored here for easy access to the slideshow information (waveform, rotation values, etc.)
        '''
        self.change_slideshow(slideshow_num)

        # the length of the slideshow (number of slides)
        self.length = len(self.cm_slideshow.file)

        # to be implemented - pause management
        self.pause_menu = PauseSettingsMenu(self)

        self.app_dict={

        }
        
    def change_slideshow(self, slideshow_num):
        if slideshow_num == 1: self.cm_slideshow = cm.slideshow1
        if slideshow_num == 2: self.cm_slideshow = cm.slideshow2
        if slideshow_num == 3: self.cm_slideshow = cm.slideshow3


    '''
    Calculates the necessary slide timeout based on the waveform of the current slide.
    
    RETURNS
    The slide timeout value (int)
    '''
    def slide_timer(self): # This needs to be made into a json as well
        time_Added = 0

        if str(self.cm_slideshow.wfm[self.cur_slide]) == '2': time_Added = 1024
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '3': time_Added = 377
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '4': time_Added = 518
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '5': time_Added = 1518
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '6': time_Added = 377
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '7': time_Added = 729

        return int(self.cm_slideshow.time[self.cur_slide]) + time_Added

    def display_pause(self):
        self.view.display_pause(self)             

    '''

    '''
    def process_settings_input(self, user_input, display):
        self.pause_menu.process_input(user_input, display)

    def process_settings_output(self, output):

        if output != None:
            if output[1] == 'change_slideshow': self.change_slideshow(output[1])

            elif output[1] == 'slide': self.cur_slide = output[1]

            else: self.replace_data(output[0], output[1], 'slideshow')

    def replace_data(self, data_Type, replacement, image):
        """
        Replaces image info in the charmrmodule file.
        data_Type: Type of info to be replaced ('rot', 'wfm', 'disp', etc)
        replacement: The info's replacement value
        image: The image whose info is being replaced (slideshow1, banner, etc)
        """
        with open("charmr_module.py", "r") as f: # Replace value in file
            lines = f.readlines()
        for number1, line in enumerate(lines):
            if image == 'slideshow': # Special case because slideshow data are arrays

                if line.find(str(self.cm_slideshow.name) + "." + data_Type) == 0:
                    data = line[len(str(self.cm_slideshow.name) + "." + data_Type) + 1:]
                    data = data.replace('"', '').replace('\'', '')
                    data = data.strip('[').replace(']', "").split(', ')
                    data[len(data) - 1] = data[len(data) - 1].strip("\n")
                    data[self.cur_slide] = replacement
            else:
                if line.find(image + "." + data_Type) == 0:
                    data = line[len(str(image) + "." + data_Type) + 1:]
                    data = replacement
        with open("charmr_module.py", "w") as f:
            for line in lines:
                if image == 'slideshow':
                    if line.find(str(self.cm_slideshow.name) + "." + data_Type) == -1: f.write(line) # If the string is not in the data line, returns value -1
                    else: f.write(str(self.cm_slideshow.name) + "." + data_Type + "=" + str(data) + "\n")
                else:
                    if line.find(image + "." + data_Type + "=") == -1: f.write(line)
                    else: f.write(image + "." + data_Type + "=" + str(data) + "\n")       
        self.reload()

    def reload(self):
        import charmr_module as cm
        reload(cm)