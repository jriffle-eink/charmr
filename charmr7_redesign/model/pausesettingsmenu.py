from basemenu import BaseMenu
import charmr_module as cm
import utils as utils

class PauseSettingsMenu(BaseMenu):
    def __init__(self, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):


        self.locations = self.menu_build('menu', '_psettings',
                              ['Go to slide', 
                               'Waveform', 
                               'Rotation', 
                               'Disp/Flsh',
                               'Main menu']
                               ) 

        self.check_file = check_file
        self.uncheck_file = uncheck_file

        super(PauseSettingsMenu, self).__init__(self.locations, check_file, uncheck_file)#locations, check_file, uncheck_file)

        #self.cur_cmd = None


        # used mainly for view purposes to know what items to display
        self.items = ['Go to slide', 'Waveform', 'Rotation', 'Disp/Flsh', 'Main menu']

        # these stay the same for all submenus, but are pause setting menu specific!
        self.general_touch_dict={
            'exit': [[.7743*cm.wsize,.1781*cm.hsize], [.8590*cm.wsize,.2417*cm.hsize]],
            'back': [[.6736*cm.wsize,.1771*cm.hsize], [.7708*cm.wsize,.2396*cm.hsize]],
        }

        self.go_to_slide_touch_dict={
            tuple(['change slideshow', '1']): [[760,490],  [860,610]],
            tuple(['change slideshow', '2']): [[876,490],  [976,610]],
            tuple(['change slideshow', '3']): [[992,490], [1092,610]],

            tuple(['slide', '7']): [[440,940],  [627,1080]],
            tuple(['slide', '8']): [[627,940],  [813,1080]],
            tuple(['slide', '9']): [[813,940],  [1000,1080]],
            tuple(['slide', '4']): [[440,1080], [627,1220]],
            tuple(['slide', '5']): [[627,1080], [813,1220]],
            tuple(['slide', '6']): [[813,1080], [1000,1220]],
            tuple(['slide', '1']): [[440,1220], [627,1360]],
            tuple(['slide', '2']): [[627,1220], [813,1360]],
            tuple(['slide', '3']): [[813,1220], [1000,1360]],
            tuple(['slide', '0']): [[627,1360], [813,1500]],
            tuple(['BACK', '-1']): [[440,1360], [627,1500]],
            tuple(['ENTER', '0']): [[813,1360], [1000,1500]],
        }

        self.wfm_touch_dict={
            tuple(['wfm', '0']): [[300,900],    [510,1100]],
            tuple(['wfm', '1']): [[510,900],    [720,1100]],
            tuple(['wfm', '2']): [[720,900],    [930,1100]],
            tuple(['wfm', '3']): [[930,900],   [1140,1100]],
            tuple(['wfm', '4']): [[300,1100],   [510,1300]],
            tuple(['wfm', '5']): [[510,1100],   [720,1300]],
            tuple(['wfm', '6']): [[720,1100],   [930,1300]],
            tuple(['wfm', '7']): [[930,1100],  [1140,1300]],
        }

        self.rot_touch_dict={
            tuple(['rot', '0']): [[470,900],    [670,1100]],
            tuple(['rot', '1']): [[770,900],    [970,1100]],
            tuple(['rot', '2']): [[470,1200],   [670,1400]],
            tuple(['rot', '3']): [[770,1200],   [970,1400]],
        }

        self.disp_flsh_touch_dict={
            tuple(['disp', 'full']): [[300,900],    [510,1100]],
            tuple(['disp', 'part']): [[510,900],    [720,1100]],
            tuple(['flsh', 'none']): [[720,900],    [930,1100]],
            tuple(['flsh', 'full']): [[930,900],   [1140,1100]],
            tuple(['flsh', 'best']): [[300,1100],   [510,1300]],
            tuple(['flsh', 'strd']): [[510,1100],   [720,1300]],
            tuple(['flsh', 'fast']): [[720,1100],   [930,1300]],
            tuple(['auto', 'auto_Opp']): [[930,1100],  [1140,1300]],
        }

    def process_input(self, user_input, display):

        if self.cur_check != 0:

            if utils.touch_zone(user_input, self.general_touch_dict['exit']):
                self.cur_check = 0
                return 'pause'

            elif utils.touch_zone(user_input, self.general_touch_dict['back']):
                self.cur_check = 0
                display.display_psettings()

            else: 
                return self.run_app(user_input, display)
        else:
            self.cur_check = self.menu_touch(user_input)

            display.change_checkmarked_option()

            # use this to display the submenu (waveform, rotation, etc.)
            display.display_psetting_submenu()

    def run_app(self, user_input, display):
        if self.cur_check == 1:
            self.go_to_slide(user_input, display)
        elif self.cur_check == 2:
            self.wfm(user_input, display)
        elif self.cur_check == 3:
            self.rotation(user_input, display)
        elif self.cur_check == 4:
            self.dispflsh(user_input, display)
        elif self.cur_check == 5:
            self.go_to_main()
        
    '''
    Returns user to main menu
    '''
    def go_to_main(self):
        # reset current command
        self.cur_check = 0
        return 'main'

    def go_to_slide(self, user_input, display):
        for elem in self.go_to_slide_touch_dict:

            if utils.touch_zone(user_input, self.go_to_slide_touch_dict[elem]):

                display.go_to_slide_display()

                return elem

    def wfm(self, user_input, display):
        for elem in self.wfm_touch_dict:

            if utils.touch_zone(user_input, self.wfm_touch_dict[elem]):

                display.wfm_display()

                return elem

    def rotation(self, user_input, display):
        for elem in self.rot_touch_dict:

            if utils.touch_zone(user_input, self.rot_touch_dict[elem]):

                display.rotation_display()

                return elem

    def dispflsh(self, user_input, display):
        for elem in self.disp_flsh_touch_dict:

            if utils.touch_zone(user_input, self.disp_flsh_touch_dict[elem]):
          
                display.dispflsh_display()

                return elem
