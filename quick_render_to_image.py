import sys
import math
import fnmatch
import os
import time
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
from tkinter import filedialog as fd
import textwrap
import json
import unicodedata
import re
import quick_render as qr

class QUICK_RENDER_TO_IMAGE(object):
    """ Helper class to wrap text in lines, based on given text, font
        and max allowed line width.
    """
    def __init__(self, 
                 chapter_numbering='roman',
                 file_type = '.pgm'
                 ):
        
        self.font_file = qr.PARAMETERS['FONT']
        self.font = ImageFont.truetype(self.font_file, qr.PARAMETERS['FONT_SIZE'])
        self.side_margin = qr.PARAMETERS['SIDE_MARGIN']
        self.top_margin = qr.PARAMETERS['TOP_MARGIN']
        self.leading = qr.PARAMETERS['LEADING']
        self.indent = qr.PARAMETERS['INDENT']
        self.file_name = None
        self.text_paragraphs = None
        self.chapter_numbering = chapter_numbering
        self.page_number = 1
        self.line_number = 0
        self.file_type = file_type
        self.page = Image.new("L", (1440, 1920), 240)
        self.draw_page = ImageDraw.Draw(self.page)
        self.draw = ImageDraw.Draw(Image.new(mode='RGB', size=(100, 100)))
        self.space_width = self.draw.textlength(text=' ', font=self.font)


    def DECIMAL_TO_ROMAN(self, number):
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        roman_number = ''
        i = 0
        while number > 0:
            for _ in range(number // val[i]):
                roman_number += syb[i]
                number -= val[i]
            i += 1
        return roman_number
        
    def new_page(self):
        self.page = Image.new("L", (1440, 1920), 240)
        self.draw_page = ImageDraw.Draw(self.page)
        self.draw = ImageDraw.Draw(Image.new(mode='RGB', size=(100, 100)))
        self.page_number += 1
        self.line_number = 0    

    def save_page(self, page_number):
        # write page # footer before saving
        w = self.font.getlength(str(page_number)) # width of character
        self.draw_page.text((1440 - self.side_margin - w, 1920 - 0.6*self.top_margin), str(page_number), font_size = self.font.size, font=self.font, fill=0)
        
        # For writing the age number to the file name
        if page_number < 10: 
            page_number = "000" + str(page_number)
        elif page_number < 100: 
            page_number = "00" + str(page_number)
        elif page_number < 1000: 
            page_number = "0" + str(page_number)
        else: page_number = str(page_number)
        
        if not os.path.exists(r"C:\Users\jriffle\Documents\Demos\charmr\texts\The_Time_Machine\pages"):
            os.makedirs(r"C:\Users\jriffle\Documents\Demos\charmr\texts\The_Time_Machine\pages")
        image_name = str(r"C:\Users\jriffle\Documents\Demos\charmr\texts\The_Time_Machine\pages" + "\\P"  +  str(page_number) + self.file_type)
        self.page.save(image_name)
    
    def write_text_line(self, xy, single_line, tracking=0, leading=None):
        x, y = xy # starting position
        lines = single_line.splitlines()
        for line in lines:
            for character in line:
                w = self.font.getlength(character) # width of character
                self.draw_page.fontmode = "1"
                self.draw_page.text((x, y), character, font_size = self.font.size, font=self.font, fill=0)
                x += w + tracking # Next printing position in pixels
            x = xy[0]
            
    def write_chapter_title(self, chapter_number):
        chapter_title = qr.CHAPTER[chapter_number][0]     
        
        old_size = self.font.size
        self.line_number = 3
        
        if self.chapter_numbering == 'roman': 
            chapter_number = self.DECIMAL_TO_ROMAN(int(chapter_number))
            chapter_title = chapter_number + ". " + chapter_title
        if self.chapter_numbering == 'decimal':
            chapter_title = "CHAPTER " + chapter_number + "\n\n" + chapter_title
                        
        self.font = ImageFont.truetype(self.font_file, self.font.size + 20)
        self.draw_page.fontmode = "1"
        self.draw_page.multiline_text((1440/2,self.top_margin + self.leading*self.line_number), chapter_title, font=self.font, fill=0, align='center', anchor='mm')        
        self.line_number = 10
        self.start_line = 10
        self.font = ImageFont.truetype(self.font_file, old_size)

def RENDER_ALL():
    for page_dict in qr.PAGES:
        quick_render.file_name = str(page)
        
        if page_dict['CHAPTER'] != None:
            quick_render.write_chapter_title(page_dict['CHAPTER'])
        else: pass

        for line in range(page_dict['LINES'][0], page_dict['LINES'][1]+1):
            if page[line][1]: # Indentation True
                line_position = (quick_render.side_margin + quick_render.indent, quick_render.top_margin + quick_render.leading*line)
            else: # Indentation False
                line_position = (quick_render.side_margin, quick_render.top_margin + quick_render.leading*line)
            quick_render.write_text_line(line_position, page_dict[line][2], page_dict[line][0], qr.PARAMETERS['LEADING'])
        quick_render.save_page(page_number)
        quick_render.new_page()
        
def RENDER_PAGE(page_number):
    page_dict = qr.PAGES[page_number-1]
    if page_dict['CHAPTER'] != None:
        quick_render.write_chapter_title(page_dict['CHAPTER'])
    else: pass

    for line in range(page_dict['LINES'][0], page_dict['LINES'][1]+1):
        if page_dict[line][1]: # Indentation True
            line_position = (quick_render.side_margin + quick_render.indent, quick_render.top_margin + quick_render.leading*line)
        else: # Indentation False
            line_position = (quick_render.side_margin, quick_render.top_margin + quick_render.leading*line)
        quick_render.write_text_line(line_position, page_dict[line][2], page_dict[line][0], qr.PARAMETERS['LEADING'])
    quick_render.save_page(page_number)
    
start_time = time.time()
quick_render = QUICK_RENDER_TO_IMAGE()
RENDER_PAGE(1)
print("run time: " + str(time.time() - start_time))