# NOTE implementing main and pause settings independently for now, then will abstract out commonalities here

# class Settings_Menu():
#     def __init__():
#         self.slide_jump_menu = SlideJumpMenu()
#         self.wfm_menu = WfmMenu()


#     # go back to main menu
#     def go_to_main(self):
#         pass
    
    




#     #-----------------------------------------------------------------------------------------------
#     #------ CHANGE SLIDE NUMBER --------------------------------------------------------------------
#     #----------------------------------------------------------------------------------------------- 
            
#     def F_gotoslide():
#         # ----- LOADING CONTENT ------------
#         LOAD(directory + 'menu_gotoslide.pgm')  
#         WINDOW_HEADER('Go-to-slide menu')  
#         GET_SLIDE((849, 617))
#         slide = ""   
        
#         while True:        
#             img = Image.open(directory + "blank_gotoslide.pgm")
#             I1 = ImageDraw.Draw(img)
#             myFont = ImageFont.truetype(r"/mnt/mmc/images/charmr/TrueTypeFonts/Serif_DejaVu.ttf", 80)
#             I1.text((10, 10), slide, font=myFont, fill=0)
            
#             img.save(directory + "tmp_gotoslide.pgm")
#             LOAD_AREA(directory + 'tmp_gotoslide.pgm', (758, 743))  
            
#             s_Check = directory + "check_bar.pgm"; s_Uncheck = directory + "uncheck_bar.pgm"
#             BUTTONS(menu.sshw, "display", s_Check, s_Uncheck)
            
#             GET_INPUT()
#             if touch:
#                 if   TOUCH_ZONE([[760,490],  [860,610]]):   CHECK(menu.sshw, 0, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(1); GET_SLIDE((849, 617))
#                 elif TOUCH_ZONE([[876,490],  [976,610]]):   CHECK(menu.sshw, 1, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(2); GET_SLIDE((849, 617))
#                 elif TOUCH_ZONE([[992,490], [1092,610]]):   CHECK(menu.sshw, 2, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(3); GET_SLIDE((849, 617))

#                 elif TOUCH_ZONE([[440,940],  [627,1080]]):  slide = slide + '7'
#                 elif TOUCH_ZONE([[627,940],  [813,1080]]):  slide = slide + '8'
#                 elif TOUCH_ZONE([[813,940],  [1000,1080]]): slide = slide + '9'
#                 elif TOUCH_ZONE([[440,1080], [627,1220]]):  slide = slide + '4' 
#                 elif TOUCH_ZONE([[627,1080], [813,1220]]):  slide = slide + '5'  
#                 elif TOUCH_ZONE([[813,1080], [1000,1220]]): slide = slide + '6' 
#                 elif TOUCH_ZONE([[440,1220], [627,1360]]):  slide = slide + '1'
#                 elif TOUCH_ZONE([[627,1220], [813,1360]]):  slide = slide + '2' 
#                 elif TOUCH_ZONE([[813,1220], [1000,1360]]): slide = slide + '3'
#                 elif TOUCH_ZONE([[627,1360], [813,1500]]):  slide = slide + '0'
#                 elif TOUCH_ZONE([[440,1360], [627,1500]]):  # BACK
#                     slide = slide[:-1]
#                     if len(slide) == 0: slide = ""
#                 elif TOUCH_ZONE([[813,1360], [1000,1500]]): # ENTER
#                     if int(slide) >= len(slideshow.file):
#                         slide = len(slideshow.file)
#                     F_slideshow(menu.sshw.check + 1, int(slide) - 2); F_main()
#                 elif TOUCH_ZONE(TOUCH_DICT['slider']): 
#                     if   device.slide == 'bght': F_brightness()
#                     elif device.slide == 'temp': F_temperature()
#                 elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
#                 elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE() 
#                 elif TOUCH_ZONE(TOUCH_DICT['sketch_button']): F_sketch()
#                 elif TOUCH_ZONE(TOUCH_DICT['back_button']): return 'back'  
#                 elif TOUCH_ZONE(TOUCH_DICT['exit_button']): return 'exit' # exit button 
#                 elif TOUCH_ZONE(TOUCH_DICT['settings_button']): return 'exit' # settings button
                
#                 else: continue

#         #-----------------------------------------------------------------------------------------------
#     #------ WAVEFORM MENU --------------------------------------------------------------------------
#     #-----------------------------------------------------------------------------------------------  
            
#     def F_wfm():
#         w_Check = directory + "check_bar.pgm"; w_Uncheck = directory + "uncheck_bar.pgm"

#         LOAD(directory + "menu_wfm.pgm")
#         WINDOW_HEADER('Waveform menu')
        
#         if device.sect == 'psettings':
#             while True:
#                 data = GET_DATA('wfm', 'slideshow')
#                 CHECK(menu.wfms, int(data), 'display', w_Check, w_Uncheck)
            
#                 GET_INPUT()
#                 if touch:
#                     if   TOUCH_ZONE([[300,900],    [510,1100]]): CHECK(menu.wfms, 0, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 0, 'slideshow');
#                     elif TOUCH_ZONE([[510,900],    [720,1100]]): CHECK(menu.wfms, 1, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 1, 'slideshow');
#                     elif TOUCH_ZONE([[720,900],    [930,1100]]): CHECK(menu.wfms, 2, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 2, 'slideshow');
#                     elif TOUCH_ZONE([[930,900],   [1140,1100]]): CHECK(menu.wfms, 3, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 3, 'slideshow'); 
#                     elif TOUCH_ZONE([[300,1100],   [510,1300]]): CHECK(menu.wfms, 4, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 4, 'slideshow');
#                     elif TOUCH_ZONE([[510,1100],   [720,1300]]): CHECK(menu.wfms, 5, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 5, 'slideshow');
#                     elif TOUCH_ZONE([[720,1100],   [930,1300]]): CHECK(menu.wfms, 6, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 6, 'slideshow');
#                     elif TOUCH_ZONE([[930,1100],  [1140,1300]]): CHECK(menu.wfms, 7, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 7, 'slideshow');  
#                     if   TOUCH_ZONE(TOUCH_DICT['slider']): 
#                         if   device.slide == 'bght': F_brightness()
#                         elif device.slide == 'temp': F_temperature()
#                     elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
#                     elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE() 
#                     elif TOUCH_ZONE(TOUCH_DICT['sketch_button']): F_sketch() 
#                     elif TOUCH_ZONE(TOUCH_DICT['back_button']): return 'back'  
#                     elif TOUCH_ZONE(TOUCH_DICT['exit_button']): return 'exit' 
#                     elif TOUCH_ZONE(TOUCH_DICT['settings_button']): return 'exit'
#                     else: continue
            
#         elif device.sect == 'main':
#             image = 'banner'
#             while True:          
#                 if   image == 'banner':  LOAD(directory + 'menu_wfm_banner.pgm')
#                 elif image == 'main':    LOAD(directory + 'menu_wfm_main.pgm')
#                 elif image == 'startup': LOAD(directory + 'menu_wfm_startup.pgm')
#                 elif image == 'check':   LOAD(directory + 'menu_wfm_checkicons.pgm')           
#                 data = GET_DATA('wfm', image) # Get data first, so screens pop up around the same time
#                 CHECK(menu.wfmm, int(data), 'display', w_Check, w_Uncheck)

#                 GET_INPUT()
#                 if touch:
#                     if   TOUCH_ZONE([[300,1040],   [510,1240]]): CHECK(menu.wfmm, 0, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 0, image);
#                     elif TOUCH_ZONE([[510,1040],   [720,1240]]): CHECK(menu.wfmm, 1, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 1, image);
#                     elif TOUCH_ZONE([[720,1040],   [930,1240]]): CHECK(menu.wfmm, 2, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 2, image);
#                     elif TOUCH_ZONE([[930,1040],  [1140,1240]]): CHECK(menu.wfmm, 3, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 3, image);
#                     elif TOUCH_ZONE([[300,1240],   [510,1440]]): CHECK(menu.wfmm, 4, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 4, image); 
#                     elif TOUCH_ZONE([[510,1240],   [720,1440]]): CHECK(menu.wfmm, 5, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 5, image);
#                     elif TOUCH_ZONE([[720,1240],   [930,1440]]): CHECK(menu.wfmm, 6, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 6, image);
#                     elif TOUCH_ZONE([[930,1240],  [1140,1440]]): CHECK(menu.wfmm, 7, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 7, image);
#                     elif TOUCH_ZONE([[220,500],     [470,650]]): image = 'banner'
#                     elif TOUCH_ZONE([[470,500],     [720,650]]): image = 'main'
#                     elif TOUCH_ZONE([[720,500],     [970,650]]): image = 'startup'
#                     elif TOUCH_ZONE([[970,500],    [1220,650]]): image = 'check'  
#                     if   TOUCH_ZONE(TOUCH_DICT['slider']): 
#                         if   device.slide == 'bght': F_brightness()
#                         elif device.slide == 'temp': F_temperature()
#                     elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
#                     elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE() 
#                     elif TOUCH_ZONE(TOUCH_DICT['sketch_button']): F_sketch() 
#                     elif TOUCH_ZONE(TOUCH_DICT['back_button']): return 'back'  
#                     elif TOUCH_ZONE(TOUCH_DICT['exit_button']): return 'exit' 
#                     elif TOUCH_ZONE(TOUCH_DICT['settings_button']): return 'exit'
#                     else: continue     