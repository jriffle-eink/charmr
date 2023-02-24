import threading
import sys 
sys.path.append('cmodule')

import charmr_module as cm

class Slideshow():

    def __init__(self, arg):
        self.cur_slide = 0

        """
        Changes the slideshow number to the number placed in argument
        """    
        if arg == 1: self.cm_slideshow = cm.slideshow1
        if arg == 2: self.cm_slideshow = cm.slideshow2
        if arg == 3: self.cm_slideshow = cm.slideshow3

        self.length = len(self.cm_slideshow.file)

        #self.pause_menu = PauseMenu()


    # def setup(self, arg):
    #     #def CHANGE_SLIDESHOW(arg):

    #     # s_Check = self.directory + 'check_bar.pgm'; s_Uncheck = self.directory + 'uncheck_bar.pgm'    


        
    #     # CHECK(menu.sshw, int(arg)-1, None, s_Check, s_Uncheck)

    #     self.slideshow_progression()

    def slide_timer(self): # This needs to be made into a json as well
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '2': time_Added = 1024
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '3': time_Added = 377
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '4': time_Added = 518
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '5': time_Added = 1518
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '6': time_Added = 377
        if str(self.cm_slideshow.wfm[self.cur_slide]) == '7': time_Added = 729

        return int(self.cm_slideshow.time[self.cur_slide])+time_Added
            
            

