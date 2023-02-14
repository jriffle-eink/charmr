import sys
import math
import fnmatch
import os
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
from tkinter import filedialog as fd
import textwrap
import unicodedata
import re

PREFIX_LIST = ['pre', 'mono', 'macro', 'micro', 'anti', 'contra', 'sym', 'com', 'fore', 'post', 'inter', 'intra', 'sub',
               'trans', 'mal', 'exo', 'circum', 'pro', 'con', 'auto', 'counter', 'dis', 'multi', 'hyper', 'hemi', 'extra', 'over', 
               'super', 'suprea', 'ultra', 'tri', 'mis']
                 
SUFFIX_LIST = ['ing','tion', 'logist', 'logical', 'logic', 'ment' , 'ful', 'age', 'ance', 'ant', 'ence', 'ery', 'ness', 'ess', 'ism', 'ist', 'able', 'ible', 'ish', 
               'less', 'like', 'ious' ,'ous', 'some', 'ward' ,'ways', 'ship', 'wize', 'ize', 'sphere', 'ity', 'aneous', 'eous'] 

class HYPHENATED_WORD():
    def __init__(self, word, first_half, second_half, remaining_pixels, buf):
        self.word = word
        self.first_half = first_half
        self.second_half = second_half
        self.remaining_pixels = remaining_pixels
        self.buf = buf

class CHAPTER_TO_PGM(object):
    """ Helper class to wrap text in lines, based on given text, font
        and max allowed line width.
    """
    def __init__(self, font_dir, font_size, file_name=None, text=None, side_margin=150, top_margin=250, leading=1.2, indent = None, page_number=1):
        self.font_dir = font_dir
        self.font_size = font_size
        self.font = ImageFont.truetype(font_dir, font_size)
        self.text = text
        self.side_margin = side_margin
        self.top_margin = top_margin
        self.leading = self.font.size*leading
        self.indent = indent*self.font.size
        self.text_paragraphs = None
        self.page_number = page_number
        self.line_number = 0
        self.file_name = file_name
        self.page = Image.new("L", (1440, 1920), 240)
        self.draw_page = ImageDraw.Draw(self.page)
        self.draw = ImageDraw.Draw(Image.new(mode='RGB', size=(100, 100)))
        self.space_width = self.draw.textlength(text=' ', font=self.font)

    def check_hyphen(self):
        global checking_hyphen
        word_part_pixel_width = 0
        word_part = ""
        pre_buf = ""

        if checking_hyphen.remaining_pixels > 4*self.font.size:
            
            if len(checking_hyphen.word) > 7:
                    
                if "–" in checking_hyphen.word:
                    word_part_pixel_width = self.font.getlength(str(checking_hyphen.word.split("–")[0]))
                    if word_part_pixel_width < checking_hyphen.remaining_pixels:
                        checking_hyphen.buf.append(checking_hyphen.word.split("–")[0])
                        checking_hyphen.first_half = checking_hyphen.ord.split("–")[0]
                        checking_hyphen.second_half = str("–" + checking_hyphen.word.split("–")[1])
                        checking_hyphen.remaining_pixels = checking_hyphen.remaining_pixels - word_part_pixel_width
                        return True
                    
                elif "-" in checking_hyphen.word:
                    word_part_pixel_width = self.font.getlength(str(checking_hyphen.word.split("-")[0]))
                    if word_part_pixel_width < checking_hyphen.remaining_pixels:
                        checking_hyphen.buf.append(checking_hyphen.word.split("-")[0])
                        checking_hyphen.first_half = checking_hyphen.word.split("-")[0]
                        checking_hyphen.second_half = str(r"-" + checking_hyphen.word.split("-")[1])
                        checking_hyphen.remaining_pixels = checking_hyphen.remaining_pixels - word_part_pixel_width
                        return True
                            
                for suffix in SUFFIX_LIST:
                    if suffix in checking_hyphen.word:
                        word_part_pixel_width = self.font.getlength(str(checking_hyphen.word.split(suffix)[0] + "-"))
                        if word_part_pixel_width < checking_hyphen.remaining_pixels:
                            checking_hyphen.buf.append(checking_hyphen.word.split(suffix)[0] + "-")
                            checking_hyphen.first_half = str(checking_hyphen.word.split(suffix)[0] + "-")
                            checking_hyphen.second_half = suffix
                            after_suffix = ['.',',',';',':','!','?']
                            if checking_hyphen.word[-1] in after_suffix:
                                checking_hyphen.second_half = str(suffix + checking_hyphen.word[-1])
                            checking_hyphen.remaining_pixels = checking_hyphen.remaining_pixels - word_part_pixel_width
                            return True
                            
                for prefix in PREFIX_LIST:
                    if prefix in checking_hyphen.word:
                        word_part_pixel_width = self.font.getlength(str(prefix + "-"))
                        if word_part_pixel_width < checking_hyphen.remaining_pixels:
                            checking_hyphen.buf.append(prefix + "-")
                            checking_hyphen.first_half = str(prefix + "-")
                            checking_hyphen.second_half = checking_hyphen.word.split(prefix)[1]
                            checking_hyphen.remaining_pixels = checking_hyphen.remaining_pixels - word_part_pixel_width  
                            return True                 
                    else: return False
            else: return False
        else: return False
                        

    def new_page(self):
        self.page = Image.new("L", (1440, 1920), 240)
        self.draw_page = ImageDraw.Draw(self.page)
        self.draw = ImageDraw.Draw(Image.new(mode='RGB', size=(100, 100)))
        self.page_number += 1
        self.line_number = 0

    def save_page(self):
        # write page # footer before saving
        w = self.font.getlength(str(self.page_number)) # width of character
        self.draw_page.text((1440 - self.side_margin - w, 1920 - 0.6*self.top_margin), str(self.page_number), font_size = self.font.size, font=self.font, fill=0)
        
        # For writing the age number to the file name
        if self.page_number < 10: 
            page_number = "0" + str(self.page_number)
        else: page_number = str(self.page_number)
        
        if not os.path.exists(os.path.dirname(self.file_name) + "/pages/"):
            os.makedirs(os.path.dirname(self.file_name) + "/pages/")
        image_name = os.path.dirname(self.file_name) + "/pages/" + os.path.basename(self.file_name).split('.')[0] + "--" + page_number + ".png"

        self.page.save(image_name)
    
    def write_chapter_title(self):
        title = os.path.basename(self.file_name).split('.')[0] # remove the extension
        chapter_number, title = os.path.basename(title).split('--') # remove the extension
        
        if chapter_number[0] == '0': 
            chapter_number = chapter_number[1:]
        title = title.replace("_", " " ) # remove the underscores and replace with spaces
        
        old_size = self.font.size
        self.line_number = 3
        text = "CHAPTER " + chapter_number + "\n\n" + title
        self.font = ImageFont.truetype(self.font_dir, self.font.size + 20)
        self.draw_page.fontmode = "1"
        self.draw_page.multiline_text((1440/2,self.top_margin + self.leading*self.line_number), text, font=self.font, fill=0, align='center', anchor='mm')
        self.line_number = 10
        self.font = ImageFont.truetype(self.font_dir, old_size)

    def get_text_width(self, text):
        return self.draw.textlength(text=text, font=self.font )
    
    def get_line_pixel_width(self, text):
        return self.font.getlength(text)
    
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
    
    def write_chapter(self):
        global checking_hyphen
        wrapped_lines = []
        single_line = []
        buf = []
        buf_width = 0
        
        if self.indent == None: # Default paragraph indent in pixels (dependent on font size)
            self.indent = 2.5*self.font.size
        
        if self.text == None:
           self. file_name = fd.askopenfilename(title="Choose chapter text file", )
            
        with open(self.file_name, 'r', encoding="utf8") as file:
            self.text = file.read()
        self.text = r"{}".format(self.text)
        
        self.text_paragraphs = [' '.join([w.strip() for w in l.split(' ') if w]) for l in self.text.split('\n') if l]
        self.write_chapter_title()
        
        for paragraph in self.text_paragraphs:
            indentation = True # Indent the paragraph
            for i, word in enumerate(paragraph.split(' ')):
                word_width = self.draw.textlength(text=word, font=self.font)
                expected_width = word_width if not buf else \
                    buf_width + self.space_width + word_width
                                        
                if 2*self.top_margin + self.leading*self.line_number > 1920:
                    self.save_page()
                    self.new_page()

                # word fits in line
                if expected_width <= 1440-2*self.side_margin:
                    buf_width = expected_width           
                    buf.append(word)
                
                # word doesn't fit in line
                else: 
                    single_line = ' '.join(buf)
                    line_pixel_width = self.font.getlength(single_line)
                    
                    number_characters = len(buf) - 1 # Start with the number of spaces between words
                    for every_word in buf: # Add the number of characters per word
                         number_characters += len(every_word)
                         
                    if indentation == True: remaining_pixels = 1440 - 2*self.side_margin - self.indent - line_pixel_width
                    if indentation == False: remaining_pixels = 1440 - 2*self.side_margin - line_pixel_width
                    
                    tracking=remaining_pixels/(number_characters-1)
                      
                    checking_hyphen = HYPHENATED_WORD(word, "", "", remaining_pixels, buf)
                    check = self.check_hyphen()
                    
                    if check:
                        remaining_pixels = checking_hyphen.remaining_pixels
                        buf = checking_hyphen.buf
                        single_line = ' '.join(buf)
                        number_characters += len(checking_hyphen.first_half) + 1
                        tracking = remaining_pixels/(number_characters-1)

                        word = checking_hyphen.second_half
                         
                    wrapped_lines.append(' '.join(buf))
                    
                    if indentation == True: # Indent paragraphs
                        self.write_text_line((self.side_margin + self.indent, self.top_margin + self.leading*self.line_number), single_line, tracking)
                        indentation = False
                    else:
                        self.write_text_line((self.side_margin, self.top_margin + self.leading*self.line_number), single_line, tracking)
                    single_line = []
                    self.line_number+=1
                    
                    buf = [word]
                    buf_width = self.draw.textlength(text=word, font=self.font)

            if buf: # Text line goes part way across page
                wrapped_lines.append(' '.join(buf))
                single_line = ' '.join(buf)
                self.write_text_line((self.side_margin, self.top_margin + self.leading*self.line_number), single_line)
                self.line_number+=1
                buf = []
                buf_width = 0

        self.save_page()
            
        return '\n'.join(wrapped_lines)
    
#### MAIN ####    

def BOOK_TO_PGM(font_dir, font_size, side_margin=150, top_margin=250, leading=1.2, indent = None):
    
    path= fd.askdirectory(title="Choose your book directory")
    file = [] #2#
    page_number = 1
    
    for file in os.listdir(path): #2#
    
        if fnmatch.fnmatch(file, '*.txt'): #2#   
            
            with open(path + '/' + file, 'r', encoding="utf8") as chapter:
                chapter = chapter.read()
            chapter = r"{}".format(chapter)
            chapter = CHAPTER_TO_PGM(font_dir = font_dir, 
                                     font_size = font_size, 
                                     file_name = path+'/'+file, 
                                     text = chapter,
                                     side_margin = side_margin, 
                                     top_margin = top_margin, 
                                     leading = leading, 
                                     indent = indent, 
                                     page_number = page_number)
            
            chapter.write_chapter()
            page_number = chapter.page_number + 1

font_dir = r"C:\Users\jriffle\Documents\Demos\charmr\TrueTypeFonts\Serif_Zachery.otf"
font_size = 40

BOOK_TO_PGM(font_dir, font_size, side_margin=150, top_margin=250, leading=1.2, indent=2)