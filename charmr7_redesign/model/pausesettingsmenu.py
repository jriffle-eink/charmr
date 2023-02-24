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

        self.go_to_slide_touch_dict={
            ['change slideshow', '1']: [[760,490],  [860,610]],
            ['change slideshow', '2']: [[876,490],  [976,610]],
            ['change slideshow', '3']: [[992,490], [1092,610]],

            ['slide', '7']: [[440,940],  [627,1080]],
            ['slide', '8']: [[627,940],  [813,1080]],
            ['slide', '9']: [[813,940],  [1000,1080]],
            ['slide', '4']: [[440,1080], [627,1220]],
            ['slide', '5']: [[627,1080], [813,1220]],
            ['slide', '6']: [[813,1080], [1000,1220]],
            ['slide', '1']: [[440,1220], [627,1360]],
            ['slide', '2']: [[627,1220], [813,1360]],
            ['slide', '3']: [[813,1220], [1000,1360]],
            ['slide', '0']: [[627,1360], [813,1500]],
        }

        self.wfm_touch_dict={
            ['wfm', '0']: [[300,900],    [510,1100]],
            ['wfm', '1']: [[510,900],    [720,1100]],
            ['wfm', '2']: [[720,900],    [930,1100]],
            ['wfm', '3']: [[930,900],   [1140,1100]],
            ['wfm', '4']: [[300,1100],   [510,1300]],
            ['wfm', '5']: [[510,1100],   [720,1300]],
            ['wfm', '6']: [[720,1100],   [930,1300]],
            ['wfm', '7']: [[930,1100],  [1140,1300]],
        }

        self.rot_touch_dict={
            ['rot', '0']: [[470,900],    [670,1100]],
            ['rot', '1']: [[770,900],    [970,1100]],
            ['rot', '2']: [[470,1200],   [670,1400]],
            ['rot', '3']: [[770,1200],   [970,1400]],
        }

        self.disp_flsh_touch_dict={
            ['disp', 'full']: [[300,900],    [510,1100]],
            ['disp', 'part']: [[510,900],    [720,1100]],
            ['flsh', 'none']: [[720,900],    [930,1100]],
            ['flsh', 'full']: [[930,900],   [1140,1100]],
            ['flsh', 'best']: [[300,1100],   [510,1300]],
            ['flsh', 'strd']: [[510,1100],   [720,1300]],
            ['flsh', 'fast']: [[720,1100],   [930,1300]],
            ['auto', auto_Opp]: [[930,1100],  [1140,1300]],
        }

    def process_input(self, user_input):
        cmd = self.menu_touch(user_input)

        
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
    
    #while True:        

        # s_Check = directory + "check_bar.pgm"; s_Uncheck = directory + "uncheck_bar.pgm"
        # BUTTONS(menu.sshw, "no display", s_Check, s_Uncheck)

        # img = Image.open(directory + "blank_gotoslide.pgm")
        # I1 = ImageDraw.Draw(img)
        # myFont = ImageFont.truetype(r"/mnt/mmc/images/charmr/TrueTypeFonts/Serif_DejaVu.ttf", 80)
        # I1.text((10, 10), slide, font=myFont, fill=0)
        
        # img.save(directory + "tmp_gotoslide.pgm")
        # LOAD_AREA(directory + 'tmp_gotoslide.pgm', 1, (758, 743))        
        # DISPLAY(wfm_Disp.text, 'part')
        
        # for cmd in self.go_to_slide_touch_dict:
        #     if utils.touch_zone(user_input, touch_dict[cmd]):
        #         return cmd

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

    def F_wfm(self, slideshow, user_input):
    # w_Check = directory + "check_bar.pgm"; w_Uncheck = directory + "uncheck_bar.pgm"

    # LOAD(directory + "menu_wfm.pgm")
    # WINDOW_HEADER('Waveform menu')
    
    # if device.sect == 'psettings':
    #     while True:
    #         data = GET_DATA('wfm', 'slideshow')
    #         CHECK(menu.wfms, int(data), 'display', w_Check, w_Uncheck)
           
    #         GET_INPUT()
            if touch:
                if   TOUCH_ZONE([[300,900],    [510,1100]]): CHECK(menu.wfms, 0, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 0, 'slideshow');
                elif TOUCH_ZONE([[510,900],    [720,1100]]): CHECK(menu.wfms, 1, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 1, 'slideshow');
                elif TOUCH_ZONE([[720,900],    [930,1100]]): CHECK(menu.wfms, 2, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 2, 'slideshow');
                elif TOUCH_ZONE([[930,900],   [1140,1100]]): CHECK(menu.wfms, 3, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 3, 'slideshow'); 
                elif TOUCH_ZONE([[300,1100],   [510,1300]]): CHECK(menu.wfms, 4, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 4, 'slideshow');
                elif TOUCH_ZONE([[510,1100],   [720,1300]]): CHECK(menu.wfms, 5, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 5, 'slideshow');
                elif TOUCH_ZONE([[720,1100],   [930,1300]]): CHECK(menu.wfms, 6, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 6, 'slideshow');
                elif TOUCH_ZONE([[930,1100],  [1140,1300]]): CHECK(menu.wfms, 7, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 7, 'slideshow');  


        
