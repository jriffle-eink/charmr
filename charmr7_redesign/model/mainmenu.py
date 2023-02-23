from .basemenu import BaseMenu
import charmr_module as cm

'''
Responsible for monitoring the state of the main menu/launching any main-menu related applications (main menu settings, slideshows, or sketch)
'''
class MainMenu(BaseMenu):
    def __init__(self, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):

        super().__init__(locations=None, check_file=check_file, uncheck_file=uncheck_file)

        #self.menu_items = self.menu_build()

        # if there is a slideshow being worked with, it is stored here
        self.slideshow = None

        # the class responsible for monitoring main menu settings
        self.settings = MainSettings()

        # the class responsible for monitoring sketch NOTE: might be unnecessary since sketch is built into demos and doesn't require much
        # external code
        self.sketch = Sketch()

        # build the menu locations
        self.locations = self.menu_build('main', '_mainmenu')

    
    ''' 
    Launches the sketch app
    '''
    def launch_sketch_app(self):
        os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt") 

    '''
    Changes the slideshow number to the number placed in argument NOTE: remove hardcoding, allow for N number of arguments to select up to 
    N number of slideshows
    '''
    def change_slideshow(self, arg):

        #s_Check = directory + 'check_bar.pgm'; s_Uncheck = directory + 'uncheck_bar.pgm'    

        if int(arg) == 1: self.slideshow = Slideshow(cm.slideshow1)
        if int(arg) == 2: self.slideshow = Slideshow(cm.slideshow2)
        if int(arg) == 3: self.slideshow = Slideshow(cm.slideshow3)
        
    #     #CHECK(menu.sshw, int(arg)-1, None, s_Check, s_Uncheck)

    '''
    Changes the slideshow number to the number placed in argument NOTE: remove hardcoding, allow for N number of arguments to select up to 
    N number of slideshows

    RETURNS
    The selected argument (either an instance of Sketch() or an instance of Slideshow(cm_slideshow))
    '''
    def app_selector(self, arg):
        slideshow_number = 1
        app_List = [cm.app1, cm.app2, cm.app3, cm.app4, cm.app5]
        for i in range(arg):
            if   app_List[i].form == 'slideshow': 
                if    i+1 == arg:

                        # #starts the slideshow thread?
                        # auto_slideshow = threading.Thread(target=slideshow_run, args=(self))

                        # auto_slideshow.run()

                        # sets up the selected slideshown and initiates automatic slide progression

                    # changes slideshow to selected argument
                    self.change_slideshow(arg)
                        
                    # returns slideshow
                    return self.slideshow

                else: slideshow_number += 1

            elif app_List[i].form == 'sketch': 
                if    i+1 == arg: 

                    return self.sketch

