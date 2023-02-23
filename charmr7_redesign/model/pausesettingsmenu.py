from basemenu import BaseMenu
import charmr_module as cm

class PauseSettingsMenu(BaseMenu):
    def __init__(self, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):

        super().__init__(locations=None, check_file=check_file, uncheck_file=uncheck_file)

        self.slide_jump_menu = SlideJumpMenu()
        self.wfm_menu = WfmMenu()

        self.locations = self.menu_build('menu', '_psettings',
                              ['Go to slide', 
                               'Waveform', 
                               'Rotation', 
                               'Disp/Flsh',
                               'Main menu']
                               ) 

        # used mainly for view purposes to know what items to display
        self.items = ['Go to slide', 'Waveform', 'Rotation', 'Disp/Flsh', 'Main menu']

        self.touch_dict={
            'change slideshow 1': [[760,490],  [860,610]],
            'change slideshow 2': [[876,490],  [976,610]],
            'change slideshow 3': [[992,490], [1092,610]],

            '7': [[440,940],  [627,1080]],
            '8': [[627,940],  [813,1080]],
            '9': [[813,940],  [1000,1080]],
            '4': [[440,1080], [627,1220]],
            '5': [[627,1080], [813,1220]],
            '6': [[813,1080], [1000,1220]],
            '1': [[440,1220], [627,1360]],
            '2': [[627,1220], [813,1360]],
            '3': [[813,1220], [1000,1360]],
            '0': [[627,1360], [813,1500]],

            'back': [[440,1360], [627,1500]],
            'enter': [[813,1360], [1000,1500]],
            'lighting': [[760,1710],   [990,1920]],
            'sketch': [[1000,1760], [1215,1920]],
            'back': [[970,340],    [1110,460]],
            'exit': [[1110,340],   [1240,460]],
            'exit': [[1240,1760], [1440,1920]],
            }

    '''
    Returns user to main menu
    '''
    def go_to_main(self):
        return 'main'

    def go_to_slide(self, slideshow, user_input):
        #def F_gotoslide():
    
    # # ----- LOADING CONTENT ------------    should be in view!!!!
    # LOAD(directory + 'menu_gotoslide.pgm', 1)  
    # WINDOW_HEADER('Go-to-slide menu')  
    # GET_SLIDE((849, 617))
        slide = ""   
    
    # while True:        

        # s_Check = directory + "check_bar.pgm"; s_Uncheck = directory + "uncheck_bar.pgm"
        # BUTTONS(menu.sshw, "no display", s_Check, s_Uncheck)

        # img = Image.open(directory + "blank_gotoslide.pgm")
        # I1 = ImageDraw.Draw(img)
        # myFont = ImageFont.truetype(r"/mnt/mmc/images/charmr/TrueTypeFonts/Serif_DejaVu.ttf", 80)
        # I1.text((10, 10), slide, font=myFont, fill=0)
        
        # img.save(directory + "tmp_gotoslide.pgm")
        # LOAD_AREA(directory + 'tmp_gotoslide.pgm', 1, (758, 743))        
        # DISPLAY(wfm_Disp.text, 'part')
        
                    #         if utils.touch_zone(user_input, touch_dict['slider']):
                    #     self.load_slider(user_input)
                    # elif utils.touch_zone(user_input, touch_dict['brightness_button']): 
                    #     self.load_brightness()
                    # elif utils.touch_zone(user_input, touch_dict['temperature_button']):
                    #     self.load_temperature()          
                    # elif utils.touch_zone(user_input, touch_dict['settings_button']): 
                    #     self.load_settings()

        # GET_INPUT()
        # if touch:

        #     utils.touch_zone(user_input, touch_dict[])
        #     if   TOUCH_ZONE([760,490],  [860,610]):   CHECK(menu.sshw, 0, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(1); GET_SLIDE((849, 617))
        #     elif TOUCH_ZONE([876,490],  [976,610]):   CHECK(menu.sshw, 1, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(2); GET_SLIDE((849, 617))
        #     elif TOUCH_ZONE([992,490], [1092,610]):   CHECK(menu.sshw, 2, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(3); GET_SLIDE((849, 617))

        #     elif TOUCH_ZONE([440,940],  [627,1080]):  slide = slide + '7'
        #     elif TOUCH_ZONE([627,940],  [813,1080]):  slide = slide + '8'
        #     elif TOUCH_ZONE([813,940],  [1000,1080]): slide = slide + '9'
        #     elif TOUCH_ZONE([440,1080], [627,1220]):  slide = slide + '4' 
        #     elif TOUCH_ZONE([627,1080], [813,1220]):  slide = slide + '5'  
        #     elif TOUCH_ZONE([813,1080], [1000,1220]): slide = slide + '6' 
        #     elif TOUCH_ZONE([440,1220], [627,1360]):  slide = slide + '1'
        #     elif TOUCH_ZONE([627,1220], [813,1360]):  slide = slide + '2' 
        #     elif TOUCH_ZONE([813,1220], [1000,1360]): slide = slide + '3'
        #     elif TOUCH_ZONE([627,1360], [813,1500]):  slide = slide + '0'
        #     elif TOUCH_ZONE([440,1360], [627,1500]):  # BACK
        #         slide = slide[:-1]
        #         if len(slide) == 0: slide = ""
        #     elif TOUCH_ZONE([813,1360], [1000,1500]): # ENTER
        #         if int(slide) >= len(slideshow.file):
        #             print(int(slide))
        #             print(len(slideshow.file))
        #             slide = len(slideshow.file)
        #         F_slideshow(menu.sshw.check + 1, int(slide) - 2); F_main()
        #     elif TOUCH_ZONE([760,1710],   [990,1920]): F_lighting()
        #     elif TOUCH_ZONE([1000,1760], [1215,1920]): pass#SKETCH("screen") 
        #     elif TOUCH_ZONE([970,340],    [1110,460]): return 'back'  
        #     elif TOUCH_ZONE([1110,340],   [1240,460]): return 'exit' 
        #     elif TOUCH_ZONE([1240,1760], [1440,1920]): return 'exit' #settings
            
        #     else: 
        #         return
        #         #continue

