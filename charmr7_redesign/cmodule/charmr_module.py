class IMAGE:
    def __init__(self, name, img, file, path, time, wfm, rot, disp, flsh, auto, size):
        self.name = name
        self.img = img
        self.file = file
        self.path = path
        self.time = time
        self.wfm = wfm
        self.rot = rot
        self.disp = disp
        self.flsh = flsh  
        self.auto = auto
        self.size = size 
		
class LAYOUT:
    def __init__(self, header, clock, banner, frontpage, footer, menu, exitbutton, returnbutton):
         self.header = header
         self.clock = clock
         self.banner = banner
         self.frontpage = frontpage
         self.footer = footer
         self.menu = menu
         self.exitbutton = exitbutton
         self.returnbuttn = returnbutton

class GAME:
    def __init__(self, name, hscr):
        self.name = name
        self.hscr = hscr
		
class APP:
	def __init__(self, name, form):
		self.name = name
		self.form = form
	
startup = IMAGE("startup", "", "", "", None, "", "", 0, "None", "None" , "")
banner = IMAGE("banner", "", "", "", None, "", "", 0, "None", "None" , "")
main = IMAGE("main", "", "", "", None, "", "", 0, "None", "None", "")
slideshow1 = IMAGE("slideshow1", [], [], "", [], [], [], [], [], [], [],)
slideshow2 = IMAGE("slideshow2", [], [], "", [], [], [], [], [], [], [],)
slideshow3 = IMAGE("slideshow3", [], [], "", [], [], [], [], [], [], [],)
check = IMAGE("check", "", "", "", "", '4', 1, "None", "None", "None" , "")
uncheck = IMAGE("uncheck", "", "", "", "", '4', 1, "None", "None" , "None", "")

area = LAYOUT(([],[]),([],[]),([],[]),([],[]),([],[]),([],[]),([],[]),([],[]))

snake = GAME("", 0)

app1 = APP("", "")
app2 = APP("", "")
app3 = APP("", "")
app4 = APP("", "")
app5 = APP("", "")

snake.name=''
snake.hscr=0
draw_App='colorpenCS_draw'
sketch_App='colorpenCS_sketch'

wsize=1440
hsize=1920
touch=1
aurora=1
startup.name='startup'
startup.file='/mnt/mmc/images/charmr/1440x1920/startup.pgm'
startup.path='/'
startup.time=None
startup.wfm=4
startup.rot=1
startup.size=(1920, 1440)
banner.name='banner'
banner.file='/mnt/mmc/images/charmr/1440x1920/banner.pgm'
banner.path='/'
banner.time=None
banner.wfm=5
banner.rot=1
banner.size=(220, 1440)
app1.name='Book covers'
app1.form='slideshow'
app2.name='Magazines'
app2.form='slideshow'
app3.name='Photo album'
app3.form='slideshow'
app4.name='Sketch pad'
app4.form='sketch'
app5.name='Snake'
app5.form='other'
slideshow1.name='slideshow1'
slideshow1.file=['dimg-cover01.pgm', 'dimg-cover02.pgm', 'dimg-cover02p1.pgm', 'dimg-cover02p2.pgm', 'dimg-cover03.pgm', 'dimg-cover04.pgm', 'dimg-cover05.pgm', 'dimg-cover06.pgm', 'dimg-cover07.pgm', 'dimg-cover08.pgm', 'dimg-cover09.pgm', 'dimg-cover10.pgm', 'dimg-cover11.pgm', 'dimg-cover12.pgm', 'dimg-cover13.pgm']
slideshow1.path='/mnt/mmc/images/images_jake/books/'
slideshow1.time=[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
slideshow1.wfm=[5, 5, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
slideshow1.rot=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
slideshow1.size=[]
slideshow1.disp=['full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full']
slideshow1.flsh=['none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none']
slideshow1.auto=['yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes']
slideshow1.styl='swipe'
slideshow2.name='slideshow2'
slideshow2.file=['dimg-mcover01.pgm', 'dimg-mcover02.pgm', 'dimg-mcover03.pgm', 'dimg-mcover04.pgm', 'dimg-mcover05.pgm', 'dimg-mcover06.pgm', 'dimg-mcover07.pgm', 'dimg-mcover08.pgm', 'dimg-mcover09.pgm', 'dimg-mcover10.pgm', 'dimg-mcover11.pgm', 'dimg-mcover12.pgm']
slideshow2.path='/mnt/mmc/images/images_jake/magazines/'
slideshow2.time=[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
slideshow2.wfm=[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
slideshow2.rot=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
slideshow2.size=[]
slideshow2.disp=['full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full']
slideshow2.flsh=['none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none']
slideshow2.auto=['yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes']
slideshow2.styl='swipe'
slideshow3.name='slideshow3'
slideshow3.file=['dimg-01_Pencils_8in.pgm', 'dimg-02_ButterflyGirlBlue_8in.pgm', 'dimg-03_girlportrait_8in.pgm', 'dimg-04_lovebirds_8in.pgm', 'dimg-06_13P_Animal01_8in.pgm', 'dimg-07_Butterfly_8in.pgm', 'dimg-08_iStock-cooldog_8in.pgm', 'dimg-09_iStock-flowers_8in.pgm', 'dimg-10_italy_8in.pgm', 'dimg-11_Buttons_8in.pgm', 'dimg-12_tiger_8in.pgm', 'dimg-13_FlashofTwoWorlds_8in.pgm', 'dimg-14_burger_portrait_8in.pgm']
slideshow3.path='/mnt/mmc/images/images_jake/photos/'
slideshow3.time=[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
slideshow3.wfm=[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
slideshow3.rot=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
slideshow3.size=[]
slideshow3.disp=['full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full', 'full']
slideshow3.flsh=['none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none']
slideshow3.auto=['yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes']
slideshow3.styl='center-out'
check.file='/mnt/mmc/images/charmr/1440x1920/check.pgm'
check.size=(72, 72)
check.wfm=4
check.rot=1
uncheck.file='/mnt/mmc/images/charmr/1440x1920/uncheck.pgm'
uncheck.size=(72, 72)
uncheck.wfm=4
uncheck.rot=1
area.header=([0,0],[1440,80])
area.clock=([1179,0],[1150,0])
area.banner=([0,80],[1440,300])
area.frontpage=([0,300],[1440,1716])
area.footer=([0,1716],[1440,1920])
area.menu=([220,360],[1220,1560])
area.exitbutton=([1110,330],[1240,470])
area.returnbutton=([970,330],[1110,470])
