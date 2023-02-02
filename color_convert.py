from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np

def PP1_22_40C(im, from_Color, to_Color):
    im = Image.open(im)
    data = np.array(im)    
    
    if from_Color == 'text' and to_Color == 'pen':
        K = (data == 0);   data[...][K] = 16 # Convert black 0 and dark graytone 120 to black 16
        W = (data == 240); data[...][W] = 224 # Convert light graytone 152 and white 240 to white 224 
        print("CONVERTED")
        
    if from_Color == 'pen' and to_Color == 'text':
        K = (data == 16)  ; data[...][K] = 0 # Converts black 16 to black 0
        W = (data == 224); data[...][W] = 240 # Converts white 224 to white 240
        
    if from_Color == 'strd' and to_Color == 'fast':
        data = data + 8
        K = (data == 8)  ; data[...][K] = 0
        W = (data == 248); data[...][W] = 240
        
    if from_Color == 'fast' and to_Color == 'strd':
        data = data - 8
        K = (data == -8)  ; data[...][K] = 0
        W = (data == 232); data[...][W] = 240

    im2 = Image.fromarray(data)
    tmp = r"/mnt/mmc/images/charmr/tmp/tmp_convert.pgm"    
    im2.save(tmp)  
    
    return tmp