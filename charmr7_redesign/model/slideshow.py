import threading
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
        if slideshow_num == 1: self.cm_slideshow = cm.slideshow1
        if slideshow_num == 2: self.cm_slideshow = cm.slideshow2
        if slideshow_num == 3: self.cm_slideshow = cm.slideshow3

        # the length of the slideshow (number of slides)
        self.length = len(self.cm_slideshow.file)

        # to be implemented - pause management
        #self.pause_menu = PauseMenu()

    '''
    Calculates the necessary slide timeout based on the waveform of the current slide.
    
    RETURNS
    The slide timeout value (int)
    '''
    def slide_timer(self): # This needs to be made into a json as well
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '2': time_Added = 1024
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '3': time_Added = 377
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '4': time_Added = 518
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '5': time_Added = 1518
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '6': time_Added = 377
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '7': time_Added = 729

        return int(self.cm_slideshow.time[self.cur_slide])+time_Added
            
            

