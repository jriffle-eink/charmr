import os
import imp
import time
import subprocess
import multiprocessing as mp
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from matplotlib import pyplot as plt
from skimage.transform import resize

# class Process(mp.Process):
#     def __init__(self, ID):
#         super(Process, self).__init__()
#         self.ID = ID
#     def run(self):
#         time.sleep(1)
#         print("Process ID: {}".format(self.ID))
        
# if __name__ == '__main__':
#     p = Process(0)
#     p.start()
#     p = Process(1)
#     p.start()

def get_target_val(old_val):
    """
    Get the "closest" color to old_val in the range [0,1] per channel divided
    into n values.
    """
    check = [float(0)]*8
    check = np.array(check)
    check[0] = old_val[0]**2 + old_val[1]**2 + old_val[2]**2 # BLACK
    check[1] = (1 - old_val[0])**2 + old_val[1]**2 + old_val[2]**2 # RED
    check[2] = old_val[0]**2 + (1 - old_val[1])**2 + old_val[2]**2 # GREEN
    check[3] = old_val[0]**2 + old_val[1]**2 + (1 - old_val[2])**2 # BLUE
    check[4] = (1 - old_val[0])**2 + (1 - old_val[1])**2 + old_val[2]**2 # YELLOW
    check[5] = (1 - old_val[0])**2 + old_val[1]**2 + (1 - old_val[2])**2 # MAGENTA
    check[6] = old_val[0]**2 + (1 - old_val[1])**2 + (1 - old_val[2])**2 # CYAN
    check[7] = (1 - old_val[0])**2 + (1 - old_val[1])**2 + (1 - old_val[2])**2 # WHITE
    
    dist = float(3); minimum = 1
    for i in range(8):
        if check[i] < dist: dist = check[i]; minimum = i
        
    if   minimum == 0: target_value = [0,0,0]
    elif minimum == 1: target_value = [1,0,0]
    elif minimum == 2: target_value = [0,1,0]
    elif minimum == 3: target_value = [0,0,1]
    elif minimum == 4: target_value = [1,1,0]
    elif minimum == 5: target_value = [1,0,1]
    elif minimum == 6: target_value = [0,1,1]
    elif minimum == 7: target_value = [1,1,1]
    
    return target_value

def dither(img):
    """
    Floyd-Steinberg dither the image img into a palette with n colors per
    channel.
    """

    arr = np.array(img, dtype=float) / 255 # Everything already on a 0 to 1 scale
                    
    for j in range(height-1):
        for i in range(width-1):
            old_val = arr[j, i].copy()
            target_value = get_target_val(old_val)
            arr[j, i] = target_value
            err = np.subtract(old_val, target_value)
            arr[j, i+1] = np.add(err*7/16, arr[j, i+1])
            if i > 0:
                arr[j+1, i-1] += err*3/16
            arr[j+1, i] += err*5/16
            arr[j+1, i+1] += err/16  
    for j in range(height-1):
        old_val = arr[j, width-1]
        target_value = get_target_val(old_val)
        arr[j, width-1] = target_value
        err = np.subtract(old_val, target_value)
        arr[j+1, width-1] += err*5/16
    for i in range(width-1):
        old_val = arr[height-1, i]
        target_value = get_target_val(old_val)
        arr[height-1, i] = target_value
        err = np.subtract(old_val, target_value)
        arr[height-1, i+1] += err*7/16
    old_val = arr[height-1, width-1]
    target_value = get_target_val(old_val)
    arr[height-1, width-1] = target_value              

    arr = arr * 255
    arr = arr.astype(np.uint8)
    return Image.fromarray(arr)

path = r"C:\Users\jriffle\Documents\Demos\General_demo\photos"
directories = os.listdir(path)

for file in directories:
    img_name = path + '\\' + file
    if os.path.isfile(img_name):

        img = Image.open(img_name)

        width = 1440; height = 1920
        img = img.resize((width, height))
        
        converter = ImageEnhance.Color(img)
        img = converter.enhance(2)
        
        img = dither(img)
        pixels = img.load()
        
        # REMAPPING PIXEL VALUES
        for i in range(height):
            for j in range(width):
                if pixels[j,i] == (0,0,0):       pixels[j,i] = (0,0,0)       # BLACK     
                if pixels[j,i] == (0,0,255):     pixels[j,i] = (96,96,96)    # BLUE
                if pixels[j,i] == (0,255,0):     pixels[j,i] = (64,64,64)    # GREEN
                if pixels[j,i] == (255,0,0):     pixels[j,i] = (32,32,32)    # RED
                if pixels[j,i] == (0,255,255):   pixels[j,i] = (128,128,128) # CYAN
                if pixels[j,i] == (255,255,0):   pixels[j,i] = (192,192,192) # YELLOW
                if pixels[j,i] == (255,0,255):   pixels[j,i] = (160,160,160) # MAGENTA
                if pixels[j,i] == (255,255,255): pixels[j,i] = (240,240,240) # WHITE

        img = img.convert("L")    
                
        save_name = file.split('.')
        img.save(path + '\\dithered\\' + 'dimg-{}.pgm'.format(save_name[0]))