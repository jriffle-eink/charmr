from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
from matplotlib import pyplot as plt

def COLOR_CONVERT(im, from_Color, to_Color):
    im = Image.open(im)
    data = np.array(im)    
    
    if from_Color == 'text' and to_Color == 'pen':
        K = (data == 0)  ; data[...][K] = 16
        W = (data == 240); data[...][W] = 224
        
    if from_Color == 'strd' and to_Color == 'fast':
        data = data + 8
        K = (data == 8)  ; data[...][K] = 0
        W = (data == 248); data[...][W] = 240
        
    if from_Color == 'fast' and to_Color == 'strd':
        data = data - 8
        K = (data == -8)  ; data[...][K] = 0
        W = (data == 232); data[...][W] = 240

    im2 = Image.fromarray(data)
    tmp = r"C:\Users\jriffle\Documents\Demos\charmr\1440x1920\Books\dithered2\tmp.pgm"    
    im2.save(tmp)    
    
    return im