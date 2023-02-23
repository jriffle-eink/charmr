from .basemenu import BaseMenu
import charmr_module as cm


class MainMenu(BaseMenu):
    def __init__(self, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):

        locations = self.menu_build("main", '_mainmenu')

        super().__init__(locations=locations, check_file=check_file, uncheck_file=uncheck_file)

        #self.menu_items = self.menu_build()

        self.slideshow = None

        self.settings = Main_Settings()

        self.sketch = Sketch()

        self.menu_build('main', '_mainmenu')


    # def menu_build(self):
    #     items = []

    #     if cm.app1.name != "": items.append(cm.app1.name)
    #     if cm.app2.name != "": items.append(cm.app2.name)
    #     if cm.app3.name != "": items.append(cm.app3.name)
    #     if cm.app4.name != "": items.append(cm.app4.name)
    #     if cm.app5.name != "": items.append(cm.app5.name)

    #     return items

    
    def launch_sketch_app(self):
        os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt") 

    def change_slideshow(arg):
        """
        Changes the slideshow number to the number placed in argument
        """    
        #s_Check = directory + 'check_bar.pgm'; s_Uncheck = directory + 'uncheck_bar.pgm'    

        if int(arg) == 1: self.slideshow = Slideshow(cm.slideshow1)
        if int(arg) == 2: self.slideshow = Slideshow(cm.slideshow2)
        if int(arg) == 3: self.slideshow = Slideshow(cm.slideshow3)
        
    #     #CHECK(menu.sshw, int(arg)-1, None, s_Check, s_Uncheck)

    def app_selector(arg):
        slideshow_number = 1
        app_List = [cm.app1, cm.app2, cm.app3, cm.app4, cm.app5]
        for i in range(arg):
            if   app_List[i].form == 'slideshow': 
                if    i+1 == arg:

                        # #starts the slideshow thread?
                        # auto_slideshow = threading.Thread(target=slideshow_run, args=(self))

                        # auto_slideshow.run()

                        # sets up the selected slideshown and initiates automatic slide progression
                    self.change_slideshow(arg)
                        
                    

                    return self.slideshow

                else: slideshow_number += 1

            elif app_List[i].form == 'sketch': 
                if    i+1 == arg: 

                    return self.sketch

