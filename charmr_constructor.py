import os
import configparser
import fnmatch
import matlab.engine
import tkinter as tk
import tkinter.ttk as ttk
from scipy import ndimage
from tkinter import Entry, Label, Button, filedialog as fd
from matplotlib import pyplot as plt
from skimage.io import imread

#-----------------------------------------------------------------------------------------------
# Defining styles and parameters
#-----------------------------------------------------------------------------------------------

root = tk.Tk()
root.title("Charmr constructor")
root.geometry("1100x400")

global N; N = tk.IntVar(value = 0)
global N1; N1 = tk.IntVar(value = 0) # Number of slides in the slideshows
global N2; N2 = tk.IntVar(value = 0)
global N3; N3 = tk.IntVar(value = 0)
global sketch_App; sketch_App = ''
global startup, banner, main, slideshow1, slideshow2, slideshow3
global check, uncheck

style = ttk.Style()
style.configure('Image.TButton', foreground="black", padding=[5, 5, 5, 5], font="Calibri 11 bold")
style.configure('Rotate.TButton', foreground="black", padding=[5, 5, 5, 5], font="Calibri 11")
style.configure('Write.TButton', foreground="red", padding=[5, 5, 5, 5], font="Calibri 12 bold")
style.configure('Entry.TEntry', font="Calibri 10")

class IMAGE: # Each image is part of a class with all characteristics
    def __init__(self, name, img, file, path, time, wfm, rot, disp, flsh, auto, size, styl):
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
        self.styl = styl
        
    def __name__(self): return f'.name=\'{self.name}\'\n'
    def __file__(self): return f'.file=\'{self.file}\'\n'
    def __sfle__(self): return f'.file={self.file}\n'
    def __path__(self): return f'.path=\'{self.path}/\'\n'
    def __time__(self): return f'.time={self.time}\n'    
    def __wfm__(self):  return f'.wfm={self.wfm}\n'
    def __rot__(self):  return f'.rot={self.rot}\n'
    def __disp__(self): return f'.disp={self.disp}\n'
    def __flsh__(self): return f'.flsh={self.flsh}\n'
    def __auto__(self): return f'.auto={self.auto}\n'
    def __size__(self): return f'.size={self.size}\n'
    def __styl__(self): return f'.styl=\'{self.styl}\'\n'       
    
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
    
class APP: # Each image is part of a class with all characteristics
    def __init__(self, name, form, bttn):
        self.name = name
        self.form = form
        self.bttn = bttn
    
    def __name__(self): return f'.name=\'{self.name}\'\n'
    def __form__(self): return f'.form=\'{self.form}\'\n'
    
startup = IMAGE("startup", "", "", "", None, "", 1, 0, "None", "None" , "", "")
banner = IMAGE("banner", "", "", "", None, "", 1, 0, "None", "None" , "", "")
main = IMAGE("main", "", "", "", None, "", 1, 0, "None", "None", "", "")
slideshow1 = IMAGE("slideshow1", [], [], "", [], [], [], [], [], [], [], "")
slideshow2 = IMAGE("slideshow2", [], [], "", [], [], [], [], [], [], [], "")
slideshow3 = IMAGE("slideshow3", [], [], "", [], [], [], [], [], [], [], "")
slideshow4 = IMAGE("slideshow2", [], [], "", [], [], [], [], [], [], [], "")
slideshow5 = IMAGE("slideshow3", [], [], "", [], [], [], [], [], [], [], "")
check = IMAGE("check", "", "", "", "", 4, 1, 0, "None", "None" , "", "")
uncheck = IMAGE("uncheck", "", "", "", "", 4, 1, 0, "None" , "None", "", "")

area = LAYOUT(([],[]),([],[]),([],[]),([],[]),([],[]),([],[]),([],[]),([],[]))

app1 = APP("", 0, None); app2 = APP("", 0, None); app3 = APP("", 0, None); app4 = APP("", 0, None); app5 = APP("", 0, None)

global slideshow_List; slideshow_List = [slideshow1, slideshow2, slideshow3, slideshow4, slideshow5]
global app_List; app_List = [app1, app2, app3, app4, app5]

#-----------------------------------------------------------------------------------------------
# Universal tools
#-----------------------------------------------------------------------------------------------

def choose_File(file):
    file = fd.askopenfilename(title="Choose your file")
    
def choose_Slide(slide): # Open file search, user selects pgm
    slide.file = fd.askopenfilename(title="Choose your image")
    slide.rot = 1
    slide.img = imread(slide.file)    
    slide.size = slide.img.shape; 
    plt.imshow(slide.img, cmap = 'gray')
    plt.show()
    
def rotate(slide, N = None): # Function rotates any image. Optional arument is for slideshow slide number N
    if N == None:
        slide.img = ndimage.rotate(slide.img, -90)
        slide.rot += 1
        if slide.rot == 4: slide.rot = 0
        plt.imshow(slide.img, cmap = 'gray')
        plt.show(slide.img)     
        
    elif N != None:
        slide.img[N.get()] = ndimage.rotate(slide.img[N.get()], -90)
        slide.rot[N.get()] += 1
        if slide.rot[N.get()] == 4: slide.rot[N.get()] = 0
        plt.imshow(slide.img[N.get()], cmap = 'gray')
        plt.show(slide.img[N.get()].any())   

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CONTROLLER-SPECIFIC DETAILS ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

module_Name = tk.StringVar()
module_Name.set("charmr_module")

ttk.module_NameLabel = Label(root, text = "Module file name")
ttk.module_NameLabel.grid(row=1, column=1, padx=5, pady=5)
module_NameEntryBox = Entry(root, textvariable = module_Name) #---------------- MODULE FILE NAME
module_NameEntryBox.grid(row=2, column=1, padx=5, pady=5)

touch = tk.IntVar()
aurora = tk.IntVar()

# Loading current.config details 
config_Path = r"C:\Users\jriffle\.spyder-py3\current.config"               
config = configparser.ConfigParser()
# For python to read, must have a section header
# Try to read the current.config file. If error, create a section header in current.config.
try: config.read(config_Path)
except: 
    with open(config_Path, 'r') as fc:
        first_Line = fc.readline()
        fc.seek(0, 0)
        current_Data = fc.read() 
        fc.close()
        with open(config_Path, 'w') as fc:
            fc.write("[SECTION1]\n")
            fc.write(current_Data) 
        fc.close()
        config.read_file(open(config_Path))          

# Finding screen size from current.config
VSIZE = tk.IntVar(); HSIZE = tk.IntVar()
VSIZE.set(config.get('SECTION1', 'VSIZE'))
HSIZE.set(config.get('SECTION1', 'HSIZE'))

ttk.touch_ScreenLabel = Label(root, text = "Touch screen")
ttk.touch_ScreenLabel.grid(row=1, column=2, padx=5, pady=5)
app1_Form1 = tk.Checkbutton(root, variable=touch, onvalue=1, offvalue=0)
app1_Form1.grid(row=2, column=2, padx=5, pady=5) 

ttk.AuroraLabel = Label(root, text = "Aurora")
ttk.AuroraLabel.grid(row=1, column=3, padx=5, pady=5)
app1_Form1 = tk.Checkbutton(root, variable=aurora, onvalue=1, offvalue=0)
app1_Form1.grid(row=2, column=3, padx=5, pady=5) 

#-----------------------------------------------------------------------------------------------
# Choose the directory for the startup screen and main menu files
#-----------------------------------------------------------------------------------------------

ttk.ImageLabel = Label(root, text = "Image select", font = "Calibri 12")
ttk.ImageLabel.grid(row=3, column=1, padx=5, pady=5)    
ttk.Button( #---------------------------------------- CHOOSE STARTUP
    root, text="Startup screen select", style='Image.TButton', width = 25,
    command=lambda: [choose_Slide(startup)]
    ).grid(row=4, column=1, padx=5, pady=5)
ttk.Button( #---------------------------------------- CHOOSE BANNER
    root,  text="Banner select", style='Image.TButton', width = 25,
    command=lambda: [choose_Slide(banner)]
    ).grid(row=5, column=1, padx=5, pady=5)

ttk.startupLabel = Label(root, text = "Waveform mode", font = "Calibri 12")
ttk.startupLabel.grid(row=3, column=2, padx=5, pady=5)
startup.wfm = Entry(root) #---------------- STARTUP WAVEFORM
startup.wfm.grid(row=4, column=2, padx=5, pady=5)
banner.wfm = Entry(root) #------------ BANNER WAVEFORM
banner.wfm.grid(row=5, column=2, padx=5, pady=5)

ttk.Button( #---------------------------------------- STARTUP ROTATION
    root, text="Rotate 90\N{DEGREE SIGN}", style='Rotate.TButton',
    command=lambda: [rotate(startup)]
    ).grid(row=4, column=3, padx=5, pady=5)   
ttk.Button( #---------------------------------------- BANNER ROTATION
    root, text="Rotate 90\N{DEGREE SIGN}", style='Rotate.TButton',
    command=lambda: [rotate(banner)]
    ).grid(row=5, column=3, padx=5, pady=5)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SKETCH APP SELECTION :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Button(
    root, text="Choose apps", padx=10, pady=5, font="calibri 12 bold", width = 20,
    command=lambda: [choose_Apps()]
    ).grid(row=8, column=1, padx=5, pady=5)

def choose_Apps():
    win = tk.Toplevel(root)  
    
    app_Name1 = tk.StringVar()
    app_Name2 = tk.StringVar()
    app_Name3 = tk.StringVar()
    app_Name4 = tk.StringVar()
    app_Name5 = tk.StringVar()
    
    app_Form1 = tk.IntVar()
    app_Form2 = tk.IntVar()
    app_Form3 = tk.IntVar()
    app_Form4 = tk.IntVar()
    app_Form5 = tk.IntVar()

    app1 = Entry(win) #--------------- APPLICATION 1
    ttk.app1Label = Label(win, text = "Appication 1", font = "Calibri 12")
    ttk.app1Label.grid(row=1, column=1, padx=5, pady=5)
    app1.grid(row=2, column=1, padx=5, pady=5) 
    
    app2 = Entry(win) #--------------- APPLICATION 2
    ttk.app2Label = Label(win, text = "Appication 2", font = "Calibri 12")
    ttk.app2Label.grid(row=3, column=1, padx=5, pady=5)
    app2.grid(row=4, column=1, padx=5, pady=5) 
    
    app3 = Entry(win) #--------------- APPLICATION 3
    ttk.app3Label = Label(win, text = "Appication 3", font = "Calibri 12")
    ttk.app3Label.grid(row=5, column=1, padx=5, pady=5)
    app3.grid(row=6, column=1, padx=5, pady=5) 
    
    app4 = Entry(win) #--------------- APPLICATION 4
    ttk.app4Label = Label(win, text = "Appication 4", font = "Calibri 12")
    ttk.app4Label.grid(row=7, column=1, padx=5, pady=5)
    app4.grid(row=8, column=1, padx=5, pady=5) 
    
    app5 = Entry(win) #--------------- APPLICATION 5
    ttk.app5Label = Label(win, text = "Appication 5", font = "Calibri 12")
    ttk.app5Label.grid(row=9, column=1, padx=5, pady=5)
    app5.grid(row=10, column=1, padx=5, pady=5) 
    
    app1_Form1 = tk.Checkbutton(win, text='Slideshow', variable=app_Form1, onvalue=1, offvalue=0)
    app1_Form1.grid(row=2, column=2, padx=5, pady=5)    
    app1_Form1 = tk.Checkbutton(win, text='Sketch', variable=app_Form1, onvalue=2, offvalue=0)
    app1_Form1.grid(row=2, column=3, padx=5, pady=5)   
    
    app2_Form2 = tk.Checkbutton(win, text='Slideshow', variable=app_Form2, onvalue=1, offvalue=0)
    app2_Form2.grid(row=4, column=2, padx=5, pady=5)    
    app2_Form2 = tk.Checkbutton(win, text='Sketch', variable=app_Form2, onvalue=2, offvalue=0)
    app2_Form2.grid(row=4, column=3, padx=5, pady=5) 
    
    app3_Form3 = tk.Checkbutton(win, text='Slideshow', variable=app_Form3, onvalue=1, offvalue=0)
    app3_Form3.grid(row=6, column=2, padx=5, pady=5)    
    app3_Form3 = tk.Checkbutton(win, text='Sketch', variable=app_Form3, onvalue=2, offvalue=0)
    app3_Form3.grid(row=6, column=3, padx=5, pady=5) 
    
    app4_Form4 = tk.Checkbutton(win, text='Slideshow', variable=app_Form4, onvalue=1, offvalue=0)
    app4_Form4.grid(row=8, column=2, padx=5, pady=5)    
    app4_Form4 = tk.Checkbutton(win, text='Sketch', variable=app_Form4, onvalue=2, offvalue=0)
    app4_Form4.grid(row=8, column=3, padx=5, pady=5) 
        
    app5_Form5 = tk.Checkbutton(win, text='Slideshow', variable=app_Form5, onvalue=1, offvalue=0)
    app5_Form5.grid(row=10, column=2, padx=5, pady=5)    
    app5_Form5 = tk.Checkbutton(win, text='Sketch', variable=app_Form5, onvalue=2, offvalue=0)
    app5_Form5.grid(row=10, column=3, padx=5, pady=5) 
    
    Button(
        win, text="Done", padx=10, pady=5, font="calibri 12 bold", width = 10,
        command=lambda: [SAVE_APPS()]
        ).grid(row=11, column=3, padx=5, pady=5)
    
    def SAVE_APPS():
        app_List[0].name = app1.get()
        app_List[1].name = app2.get()
        app_List[2].name = app3.get()
        app_List[3].name = app4.get()
        app_List[4].name = app5.get()

        app_List[0].form = app_Form1.get()
        app_List[1].form = app_Form2.get()
        app_List[2].form = app_Form3.get()
        app_List[3].form = app_Form4.get()
        app_List[4].form = app_Form5.get() 
        
        for i in range(len(app_List)):
            if app_List[i].form == 0: app_List[i].form = "other" 
            if app_List[i].form == 1: app_List[i].form = "slideshow"
            if app_List[i].form == 2: app_List[i].form = "sketch"   
        
        j=0
        for i in range(len(app_List)): # Iterates through all applications
            if app_List[i].form == 'slideshow':
                app_List[i].bttn = j # Numbers the button for the slideshow app
                if i == 0: # If the first application is a slideshow...
                    Button( # Create a button for it
                        root, text=app_List[0].name, padx=10, pady=5, font="calibri 12 bold", width = 20,
                        command=lambda: [SLIDE_WINDOW(slideshow_List[app_List[0].bttn], app_List[0].bttn+1)] 
                        ).grid(row=9, column=(app_List[0].bttn+1), padx=5, pady=5)
                        # Button action is a command to bring to slideshow edit window
                        # Places button in the first column, all others are placed in next available
                if i == 1:
                    Button(
                        root, text=app_List[1].name, padx=10, pady=5, font="calibri 12 bold", width = 20,
                        command=lambda: [SLIDE_WINDOW(slideshow_List[app_List[1].bttn], app_List[1].bttn+1)]
                        ).grid(row=9, column=(app_List[1].bttn+1), padx=5, pady=5)
                if i == 2:
                    Button(
                        root, text=app_List[2].name, padx=10, pady=5, font="calibri 12 bold", width = 20,
                        command=lambda: [SLIDE_WINDOW(slideshow_List[app_List[2].bttn], app_List[2].bttn+1)]
                        ).grid(row=9, column=(app_List[2].bttn+1), padx=5, pady=5)
                if i == 3:
                    Button(
                        root, text=app_List[3].name, padx=10, pady=5, font="calibri 12 bold", width = 20,
                        command=lambda: [SLIDE_WINDOW(slideshow_List[app_List[3].bttn], app_List[3].bttn+1)]
                        ).grid(row=9, column=(app_List[3].bttn+1), padx=5, pady=5)
                if i == 4:
                    Button(
                        root, text=app_List[4].name, padx=10, pady=5, font="calibri 12 bold", width = 20,
                        command=lambda: [SLIDE_WINDOW(slideshow_List[app_List[4].bttn], app_List[4].bttn+1)]
                        ).grid(row=9, column=(app_List[4].bttn+1), padx=5, pady=5)                    
                j += 1
            
        win.destroy()  
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# EDITING THE SLIDESHOWS :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def SLIDE_WINDOW(slide, num): # Button press sends the correct slideshow 'slide'
    global N, N1, N2, N3
    win = tk.Toplevel(root)
    disp = tk.IntVar()
    flsh = tk.IntVar()
    auto = tk.IntVar()
    if num == 1: N = N1 
    if num == 2: N = N2
    if num == 3: N = N3
    
    ttk.Button(
        win, text="Choose slideshow directory", width = 30,
        command=lambda: [SLIDESHOW_DIRECTORY(slide), SETUP_SLIDESHOW(slide), win.lift()]
        ).grid(row=1, column=1)
           
#-----------------------------------------------------------------------------------------------
# Choose the directory for the slideshow images
#-----------------------------------------------------------------------------------------------
    
    def SLIDESHOW_DIRECTORY(slide):
        global clicked_Style
        slide.path= fd.askdirectory(title="Choose your slideshow directory")
        slide.file = [] #2#
        for file in os.listdir(slide.path): #2#
            if fnmatch.fnmatch(file, '*.pgm'): #2#
                slide.file.append(file)  #2#
        slide.img = [""] * len(slide.file) # Default values for slideshow lists
        slide.time = [2500] * len(slide.file)
        slide.wfm = [5] * len(slide.file)
        slide.rot = [1] * len(slide.file)
        slide.disp = [None] * len(slide.file)
        slide.flsh = [None] * len(slide.file)
        slide.auto = [None] * len(slide.file)
        clicked_Style = tk.StringVar()
        SETUP_SLIDESHOW(slide)
    
    def SETUP_SLIDESHOW(slide):
        global time, wfm, rot, disp, flsh, auto, clicked_Style
        disp = tk.IntVar(); flsh = tk.IntVar(); auto = tk.IntVar()
        time = tk.StringVar(win, value = str(slide.time[N.get()]))
        wfm = tk.StringVar(win, value = str(slide.wfm[N.get()]))
        
        if isinstance(slide.disp[N.get()], int): disp.set(slide.disp[N.get()])
        else:  disp.set(1)
        if isinstance(slide.flsh[N.get()], int): flsh.set(slide.flsh[N.get()])
        else:  flsh.set(0)
        if isinstance(slide.auto[N.get()], int): auto.set(slide.auto[N.get()])
        else:  auto.set(1)
        
        time_Entrybox = Entry(win, textvariable = time)
        ttk.timeLabel = Label(win, text = "Screen time (ms)", font='calibri 12')
        ttk.timeLabel.grid(row=2, column=2, padx=5, pady=5)
        time_Entrybox.grid(row=3, column=2, padx=5, pady=5)
        
        wfm_Entrybox = Entry(win, textvariable = wfm)
        ttk.wfmLabel = Label(win, text = "Waveform mode", font='calibri 12')
        ttk.wfmLabel.grid(row=2, column=3, padx=5, pady=5)
        wfm_Entrybox.grid(row=3, column=3, padx=5, pady=5)
        
#-----------------------------------------------------------------------------------------------
# Slide buttons and checkboxes
#-----------------------------------------------------------------------------------------------           

        ttk.styleLabel = Label(win, text = "Slideshow style", font='calibri 12')
        ttk.styleLabel.grid(row=2, column=1, padx=5, pady=5)
                        
        styles = ttk.Combobox(win, values=["swipe", "center-out", "reader"], textvariable = clicked_Style)
        styles.grid(row=3, column=1, padx=5, pady=5)

        Button(
            win, text="Prev slide", padx=10, pady=5, font="calibri 12",
            command=lambda: [DEC_SN(slide)]
            ).grid(row=1, column=2, padx=5, pady=5)

        Button(
            win, text="Next slide", padx=10, pady=5, font="calibri 12",
            command=lambda: [INC_SN(slide)]
            ).grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Button(
            win, text="Rotate 90\N{DEGREE SIGN}", style="Rotate.TButton",
            command=lambda: [rotate(slide, N)]
            ).grid(row=3, column=4, padx=5, pady=5)
        
        check_Display1 = tk.Checkbutton(win, text='Full display', variable=disp, onvalue=1, offvalue=0)
        check_Display1.grid(row=1, column=5, padx=5, pady=5)
    
        check_Display2= tk.Checkbutton(win, text='Part display', variable=disp, onvalue=0, offvalue=1)
        check_Display2.grid(row=2, column=5, padx=5, pady=5)        

        check_Flash1 = tk.Checkbutton(win, text='Full flash', variable=flsh, onvalue=1, offvalue=0)
        check_Flash1.grid(row=1, column=6, padx=5, pady=5)
        
        check_Flash2 = tk.Checkbutton(win, text='Best flash', variable=flsh, onvalue=2, offvalue=0)
        check_Flash2.grid(row=2, column=6, padx=5, pady=5)
        
        check_Flash3 = tk.Checkbutton(win, text='Strd flash', variable=flsh, onvalue=3, offvalue=0)
        check_Flash3.grid(row=3, column=6, padx=5, pady=5)
        
        check_Flash4 = tk.Checkbutton(win, text='Fast flash', variable=flsh, onvalue=4, offvalue=0)
        check_Flash4.grid(row=4, column=6, padx=5, pady=5)
   
        check_Autoflash = tk.Checkbutton(win, text='Auto flash', variable=auto, onvalue=1, offvalue=0)
        check_Autoflash.grid(row=1, column=7, padx=5, pady=5)
        
        slide.img[N.get()] = imread(slide.path + "\\" + slide.file[N.get()])
        img = plt.imshow(slide.img[N.get()], cmap = 'gray')
        plt.show(img)
        
#-----------------------------------------------------------------------------------------------
# Moves through slides as the user clicked the prev or next buttons, saves time, wfm disp, and flash values
#-----------------------------------------------------------------------------------------------               
        
    def DEC_SN(slide): # Moves slides back 1, saves class characteristics
        global N, disp, flsh, auto, clicked_Style
        slide.time[N.get()] = int(time.get())
        slide.wfm[N.get()] = int(wfm.get())
        if disp.get() == 0: slide.disp[N.get()] = 0
        if disp.get() == 1: slide.disp[N.get()] = 1   
        if flsh.get() == 0: slide.flsh[N.get()] = 0
        if flsh.get() == 1: slide.flsh[N.get()] = 1 
        if flsh.get() == 2: slide.flsh[N.get()] = 2  
        if flsh.get() == 3: slide.flsh[N.get()] = 3  
        if flsh.get() == 4: slide.flsh[N.get()] = 4    
        if auto.get() == 0: slide.auto[N.get()] = 0
        if auto.get() == 1: slide.auto[N.get()] = 1   
        N.set(N.get() - 1)
        if N.get() < 0: N.set(len(slide.img)-1)
        slide.styl = clicked_Style.get()
        SETUP_SLIDESHOW(slide)

    def INC_SN(slide): # Moves slides forward 1, saves class characteristics
        global N, disp, flsh, auto, clicked_Style
        slide.time[N.get()] = int(time.get())
        slide.wfm[N.get()] = int(wfm.get())
        if disp.get() == 0: slide.disp[N.get()] = 0
        if disp.get() == 1: slide.disp[N.get()] = 1
        if flsh.get() == 0: slide.flsh[N.get()] = 0
        if flsh.get() == 1: slide.flsh[N.get()] = 1 
        if flsh.get() == 2: slide.flsh[N.get()] = 2  
        if flsh.get() == 3: slide.flsh[N.get()] = 3  
        if flsh.get() == 4: slide.flsh[N.get()] = 4  
        if auto.get() == 0: slide.auto[N.get()] = 0
        if auto.get() == 1: slide.auto[N.get()] = 1  
        N.set(N.get() + 1)
        if N.get() >= len(slide.img):  N.set(0)
        slide.styl = clicked_Style.get()
        SETUP_SLIDESHOW(slide)
    
        win.mainloop()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Writing to the module file to be reference by charmr.py ::::::::::::::::::::::::::::::::::::::
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

label = Label(root, text = "                              ") #Spacer
label.grid(row=4, column=5, padx=5, pady=5)
ttk.Button(
    root, text="Write & Close", style="Write.TButton",
    command=lambda: [WRITE_MODULE()]
    ).grid(row=8, column=6, padx=5, pady=5)
    
def WRITE_MODULE():   
    # Applying REAGL to images in slideshows (only forward transitions)         
    # print("REAGLing images")
    # j = 0
    # eng = matlab.engine.start_matlab()
    # for i in range(len(app_List)): 
    #     if app_List[i].form == 'slideshow':
    #         eng.python_REAGL(slideshow_List[j].path, nargout=0) 
    #         print("REAGLed: " + str(slideshow_List[j].path))   
    #         j += 1
    
    startup.wfm = int(startup.wfm.get())
    banner.wfm = int(banner.wfm.get())
      
    for i in range(len(slideshow_List)):     
        for j in range(len(slideshow_List[i].disp)):
            if slideshow_List[i].disp[j] == 0: slideshow_List[i].disp[j] = 'part'
            if slideshow_List[i].disp[j] == 1: slideshow_List[i].disp[j] = 'full'
            if slideshow_List[i].flsh[j] == 0: slideshow_List[i].flsh[j] = 'none'
            if slideshow_List[i].flsh[j] == 1: slideshow_List[i].flsh[j] = 'full'
            if slideshow_List[i].flsh[j] == 2: slideshow_List[i].flsh[j] = 'best'
            if slideshow_List[i].flsh[j] == 3: slideshow_List[i].flsh[j] = 'strd'
            if slideshow_List[i].flsh[j] == 4: slideshow_List[i].flsh[j] = 'fast'
            if slideshow_List[i].auto[j] == 1: slideshow_List[i].auto[j] = 'yes'
            if slideshow_List[i].auto[j] == 0: slideshow_List[i].auto[j] = 'no' 
    
    if module_Name.get()[-3] != ".py":
        module_Name.set(module_Name.get() + '.py')

    if os.path.exists(module_Name.get()): # Checks if module exists, deletes if it does. Then writes the module file.
        os.remove(module_Name.get())
    with open('charmr_classinfo.txt', 'r') as f0, open (module_Name.get(), "w") as f1:
        f1.write('\n')
        for line in f0:
            f1.write(line)
        f1.write('wsize=' + str(VSIZE.get()) + "\n")
        f1.write('hsize=' + str(HSIZE.get()) + "\n")
        f1.write('touch=' + str(touch.get()) + "\n")
        f1.write('aurora=' + str(aurora.get()) + "\n") 
        for i in [startup, banner]:
            f1.write(i.name + i.__name__())            
            f1.write(i.name + i.__file__())
            f1.write(i.name + i.__path__())
            f1.write(i.name + i.__time__())
            f1.write(i.name + i.__wfm__() )
            f1.write(i.name + i.__rot__() )
            f1.write(i.name + i.__size__())
        k = 1
        for i, j in enumerate(app_List):
            if app_List[i].name != "":
                f1.write("app" + str(k) + str(app_List[i].__name__()))
                f1.write("app" + str(k) + str(app_List[i].__form__()))
                k += 1
        for i, j in enumerate(slideshow_List):
            if len(slideshow_List[i].path) > 3:
                f1.write(slideshow_List[i].name + slideshow_List[i].__name__())            
                f1.write(slideshow_List[i].name + slideshow_List[i].__sfle__())
                f1.write(slideshow_List[i].name + slideshow_List[i].__path__())
                f1.write(slideshow_List[i].name + slideshow_List[i].__time__())
                f1.write(slideshow_List[i].name + slideshow_List[i].__wfm__() )
                f1.write(slideshow_List[i].name + slideshow_List[i].__rot__() )
                f1.write(slideshow_List[i].name + slideshow_List[i].__size__())
                f1.write(slideshow_List[i].name + slideshow_List[i].__disp__())
                f1.write(slideshow_List[i].name + slideshow_List[i].__flsh__())
                f1.write(slideshow_List[i].name + slideshow_List[i].__auto__())  
                f1.write(slideshow_List[i].name + slideshow_List[i].__styl__())
            
        check.wfm = 3; uncheck.wfm = 3
        check.rot = 1; uncheck.rot = 1
        if   VSIZE.get() == 1440 and HSIZE.get() == 1920:
            check.file = r"C:\Users\jriffle\Documents\Demos\charmr\1440x1920\check.pgm"
            uncheck.file =  r"C:\Users\jriffle\Documents\Demos\charmr\1440x1920\uncheck.pgm"
            #check.file = '/mnt/mmc/images/charmr/1440x1920/check.pgm'
            #uncheck.file = '/mnt/mmc/images/charmr/1440x1920/uncheck.pgm'  
            check.img = imread(check.file); uncheck.img = imread(uncheck.file)
            check.size = check.img.shape; uncheck.size = uncheck.img.shape
            for i in [check, uncheck]:
                f1.write(i.name + i.__file__())
                f1.write(i.name + i.__size__())
                f1.write(i.name + i.__wfm__() )
                f1.write(i.name + i.__rot__() )
            f1.write("area.header=([0,0],[1440,80])\n") 
            f1.write("area.clock=([1179,0],[1150,0])\n") 
            f1.write("area.banner=([0,80],[1440,300])\n") 
            f1.write("area.frontpage=([0,300],[1440,1716])\n") 
            f1.write("area.footer=([0,1716],[1440,1920])\n") 
            f1.write("area.menu=([220,360],[1220,1560])\n") 
            f1.write("area.exitbutton=([1110,330],[1240,470])\n") 
            f1.write("area.returnbutton=([970,330],[1110,470])\n") 
        elif VSIZE.get() == 1264 and HSIZE.get() == 1680:
            check.file = r"C:\Users\jriffle\Documents\Demos\charmr\1264x1680\check.pgm"
            uncheck.file = r"C:\Users\jriffle\Documents\Demos\charmr\1264x1680\uncheck.pgm"
            #check.file = '/mnt/mmc/images/charmr/1264x1680/check.pgm'
            #uncheck.file = '/mnt/mmc/images/charmr/1264x1680/uncheck.pgm'  
            check.img = imread(check.file); uncheck.img = imread(uncheck.file)
            check.size = check.img.shape; uncheck.size = uncheck.img.shape
            for i in [check, uncheck]:
                f1.write(i.name + i.__file__())
                f1.write(i.name + i.__size__())
                f1.write(i.name + i.__wfm__() )
                f1.write(i.name + i.__rot__() )            
            f1.write("area.header=([0,0],[1264,70])\n") 
            f1.write("area.clock=([1038,0],[1010,0])\n") 
            f1.write("area.banner=([0,70],[1264,260])\n") 
            f1.write("area.frontpage=([0,260],[1264,1500])\n") 
            f1.write("area.footer=([0,1500],[1264,1680])\n") 
            f1.write("area.menu=([195,315],[1068,1364])\n") 
            f1.write("area.exitbutton=([970,290],[1090,400])\n") 
            f1.write("area.returnbutton=([850,290],[970,400])\n") 
        
        f1.close()
        print("Finished constructing. You may now close the window.")
        
root.mainloop()
    