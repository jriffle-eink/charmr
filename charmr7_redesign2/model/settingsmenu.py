from basemenu import BaseMenu
import charmr_module as cm
import utils as utils

class SettingsMenu(BaseMenu):

    def __init__(self, view, locations, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):

        super(SettingsMenu, self).__init__(view, locations, check_file, uncheck_file)


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

    def retrieve_output(self, user_input, touch_dict, app_type):
        for elem in touch_dict:

            if utils.touch_zone(user_input, touch_dict[elem]):

                self.view.settings_app_display(app_type)

                return elem