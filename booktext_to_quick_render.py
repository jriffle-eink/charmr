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

with open('HYPHEN_DICT.json') as json_file:
    DICT = json.load(json_file)

DASH_LIST = ['\u2014\u2014','\u2014','\u2013', '-'] # U+2013: en-dash, U+2014: em-dash

POST_SUFFIX = ['!\u201D','?\u201D','.\u201D','.',',',';',':','!','?','\u201D'] # U+u201D: right double quotation mark

class HYPHENATED_WORD():
    def __init__(self, word, first_half, second_half, remaining_pixels, buf):
        self.word = word
        self.first_half = first_half
        self.second_half = second_half
        self.remaining_pixels = remaining_pixels
        self.buf = buf

class CHAPTER_TO_QUICK_RENDER(object):
    """ Helper class to wrap text in lines, based on given text, font
        and max allowed line width.
    """
    def __init__(self, 
                 font_file, 
                 font_size, 
                 file_name=None, 
                 text=None, 
                 side_margin=150, 
                 top_margin=250, 
                 leading=1.2, 
                 indent=None, 
                 page_number=1, 
                 chapter_numbering='roman',
                 file_type = '.pgm'
                 ):
        
        self.font_file = font_file
        self.font = ImageFont.truetype(font_file, font_size)
        self.text = text
        self.side_margin = side_margin
        self.top_margin = top_margin
        self.leading = self.font.size*leading
        self.indent = indent*self.font.size
        self.first_page_number = page_number
        self.page_number = page_number
        self.start_line = 0
        self.line_number = 0
        self.file_type = file_type
        self.file_name = file_name
        self.new_chapter = True
        self.quick_render = r"C:\Users\jriffle\Documents\Demos\charmr\texts\The_Time_Machine\quick_render.py"
        self.page = Image.new("L", (1440, 1920), 240)
        self.draw_page = ImageDraw.Draw(self.page)
        self.chapter_number = None # remove the extension
        self.chapter_numbering = chapter_numbering
        self.draw = ImageDraw.Draw(Image.new(mode='RGB', size=(100, 100)))
        self.space_width = self.draw.textlength(text=' ', font=self.font)

    def CHECK_DASH(self):
        global check
        for dash in DASH_LIST: # Check this first. Do not hyphenate a dashed or already hyphenated word
            if dash in check.word: # hyphen, en-dash, or em-dash
                word_part_pixel_width = self.font.getlength(str(check.word.split(dash)[0] +  str(dash)))
                if word_part_pixel_width < check.remaining_pixels:
                    check.first_half = check.word.split(dash)[0] + dash
                    check.second_half = check.word.split(dash)[1]
                    check.buf.append(check.first_half)       
                    check.remaining_pixels = check.remaining_pixels - word_part_pixel_width
                    return True
                else: return False
    
    def CHECK_ROOT(self):
        global check
        root_list = []
        # If no dash, look for any roots, to separate the root and leave a possible suffix ending
        # Only need to look for roots up to the last 3 characters in the string b/c suffixes need to be at least 3 characters long
        for num_char in range(3,len(check.word)-2): # for word "washing" of length 7 (range 3:5), num_char=3:4 
            for start_char in range(0,len(check.word)): # for num_char=3, range(0,4), start_char=0:3
                #print(check.word[start_char:start_char+num_char])
                root_part = check.word[start_char:start_char+num_char]
                if root_part.lower() in DICT and DICT[root_part.lower()] == 'root':
                    root_list.append(root_part)
        
        if len(root_list) != 0:
            root = max(root_list, key=len)
            check.first_half = check.word.split(root)[0] + root + '-'
            check.second_half = check.word.split(root)[1]      
            word_part_pixel_width = self.font.getlength(check.first_half)
            if word_part_pixel_width < check.remaining_pixels and len(check.second_half) > 2:
                check.buf.append(check.first_half)
                check.remaining_pixels = check.remaining_pixels - word_part_pixel_width 
                return True  
            else: return False
        
    def CHECK_POST_SUFFIX(self):
        global check
        check.post_suffix_character = ""
        for character in POST_SUFFIX: # checking if the suffix exists but there are end-of-word characters
            if check.word.endswith(character):   
                check.word = check.word[0:len(check.word)-len(character)]
                check.post_suffix_character = character
    
    def CHECK_SUFFIX(self):
        global check
        for num_char in reversed(range(3,len(check.word)-2)): # Checking for suffixes
            if check.word[len(check.word)-num_char:] in DICT and DICT[check.word[len(check.word)-num_char:]] == 'suffix':      
                check.first_half = check.word[0:len(check.word)-num_char] + '-'
                check.second_half = check.word[len(check.word)-num_char:] + check.post_suffix_character
                word_part_pixel_width = self.font.getlength(check.first_half)
                if word_part_pixel_width < check.remaining_pixels:
                    check.buf.append(check.first_half)
                    check.remaining_pixels = check.remaining_pixels - word_part_pixel_width 
                    return True
    
    def CHECK_PREFIX(self):
        global check
        for num_char in reversed(range(3,len(check.word)-2)): # Checking for prefixes
            lower_case_word = check.word.lower() 
            if lower_case_word[0:num_char].lower() in DICT and DICT[lower_case_word[0:num_char]] == 'prefix':
                check.first_half = check.word[0:num_char] + '-'
                check.second_half = check.word[num_char:] + check.post_suffix_character
                word_part_pixel_width = self.font.getlength(check.first_half)
                if word_part_pixel_width < check.remaining_pixels:
                    check.buf.append(check.first_half)
                    check.remaining_pixels = check.remaining_pixels - word_part_pixel_width  
                    return True 

    def check_hyphen(self):
        global check
        word_part_pixel_width = 0
        if len(check.word) < 7: return False
        result = self.CHECK_DASH()
        if result == True: return True
        if result == False: return False
        result = self.CHECK_ROOT()
        if result == True: return True
        if result == False: return False
        self.CHECK_POST_SUFFIX()
        if   self.CHECK_SUFFIX(): return True
        elif self.CHECK_PREFIX(): return True
        else: return False        
        return False

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
        self.line_number = 0
        self.start_line = 0
        with open(self.quick_render, 'a', encoding="utf8") as file:
            file.write("\nP" + str(self.page_number) + "={\n")
        self.page_number += 1

    def save_page(self):
        with open(self.quick_render, 'a', encoding="utf8") as file:
            if self.new_chapter:
                if '--' in self.chapter_number:
                    file.write("\'CHAPTER\':" + self.chapter_number.split('--')[0] + ",\n")
                else: 
                    file.write("\'CHAPTER\':" + self.chapter_number + ",\n")
            else:
                file.write("\'CHAPTER\':" + str(None) + ",\n")
            file.write("\'LINES\':(" + str(self.start_line) + ',' + str(self.line_number-1) + ")\n")
            file.write("}\n")
        # write page # footer before saving
        w = self.font.getlength(str(self.page_number)) # width of character
        
        # For writing the age number to the file name
        if self.page_number < 10: 
            page_number = "00" + str(self.page_number)
        elif self.page_number < 100: 
            page_number = "0" + str(self.page_number)
        else: page_number = str(self.page_number)
        
        self.new_chapter = False
    
    def write_chapter_title(self):
        title = os.path.basename(self.file_name).split('.')[0] # remove the extension
        self.chapter_number, title = os.path.basename(title).split('__') # remove the extension
        
        if self.chapter_number[0] == '0': 
            self.chapter_number = self.chapter_number[1:]
        title = title.replace("_", " " ) # remove the underscores and replace with spaces
        
        old_size = self.font.size
        self.line_number = 3
        
        if "--" in self.chapter_number:
            text = title
            
        else:
            if self.chapter_numbering == 'roman': 
                chapter_number_roman = self.DECIMAL_TO_ROMAN(int(self.chapter_number))
                text = chapter_number_roman + ". " + title
            if self.chapter_numbering == 'decimal':
                text = "CHAPTER " + self.chapter_number + "\n\n" + title
                
        self.font = ImageFont.truetype(self.font_file, self.font.size + 20)
        
        #self.draw_page.multiline_text((1440/2,self.top_margin + self.leading*self.line_number), text, font=self.font, fill=0, align='center', anchor='mm')
        self.line_number = 10
        self.start_line = 10
        self.font = ImageFont.truetype(self.font_file, old_size)

    def get_text_width(self, text):
        return self.draw.textlength(text=text, font=self.font )
    
    def get_line_pixel_width(self, text):
        return self.font.getlength(text)
    
    def write_text_line(self, xy, single_line, tracking=0, leading=None):
        global indentation
        x, y = xy # starting position
        lines = single_line.splitlines()
        
        with open(self.quick_render, 'a', encoding="utf8") as file:
            for line in lines: # There is only one line
                file.write(str(self.line_number) + ":[" + str(tracking) + "," + str(indentation) + ",\"" + line  + "\"],\n")
            
    def write_chapter(self):
        global check, indentation
        single_line = []
        buf = []
        buf_width = 0
        self.new_page()
        self.new_chapter = True
        
        if self.indent == None: # Default paragraph indent in pixels (dependent on font size)
            self.indent = 2.5*self.font.size
        
        if self.text == None:
           self. file_name = fd.askopenfilename(title="Choose chapter text file", )
            
        with open(self.file_name, 'r', encoding="utf8") as file:
            self.text = file.read()
        self.text = r"{}".format(self.text)
        
        text_paragraphs = [' '.join([w.strip() for w in l.split(' ') if w]) for l in self.text.split('\n') if l]
        self.write_chapter_title()
        
        for paragraph in text_paragraphs:
            indentation = True # Indent the paragraph
            for i, word in enumerate(paragraph.split(' ')):
                word_width = self.draw.textlength(text=word, font=self.font)
                expected_width = word_width if not buf else \
                    buf_width + self.space_width + word_width
                                        
                if 2*self.top_margin + self.leading*self.line_number > 1920:
                    self.save_page()
                    self.new_page()

                # word fits in line
                if indentation == True and expected_width <= 1440-2*self.side_margin - self.indent:
                    buf_width = expected_width           
                    buf.append(word)
                elif indentation == False and expected_width <= 1440-2*self.side_margin:
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
                    
                    tracking=remaining_pixels/(number_characters-1) # Extra spacing between each letter ( > 0 ) 
                     
                    check = HYPHENATED_WORD(word, "", "", remaining_pixels, buf) # Returns true if the word that doesn't fit can be hyphenated
                    
                    if tracking > 0.5 and self.check_hyphen():
                        # if hypen is True, change all necessary variables 
                        remaining_pixels = check.remaining_pixels
                        number_characters += len(check.first_half) + 1
                        tracking = remaining_pixels/(number_characters)
                        buf = check.buf 
                        single_line = ' '.join(buf)
                        word = check.second_half # Change the word to the latter half of the hyphenated word
                                             
                    if indentation == True: # Indent paragraphs
                        start_position = (self.side_margin + self.indent, self.top_margin + self.leading*self.line_number)
                        self.write_text_line(start_position, 
                                             single_line, 
                                             tracking)
                        
                    else:
                        start_position = (self.side_margin, self.top_margin + self.leading*self.line_number)
                        self.write_text_line(start_position, 
                                             single_line, 
                                             tracking)
                        
                    single_line = []
                    self.line_number+=1
                    buf = [word]
                    buf_width = self.draw.textlength(text=word, font=self.font)
                    indentation = False
                    
            if buf: # Text line goes part way across page
                single_line = ' '.join(buf)
                if indentation == True: 
                    start_position = (self.side_margin + self.indent, self.top_margin + self.leading*self.line_number)
                    self.write_text_line(start_position, 
                                         single_line, 
                                         tracking = 0)
                else: 
                    start_position = (self.side_margin, self.top_margin + self.leading*self.line_number)
                    self.write_text_line(start_position, 
                                         single_line, 
                                         tracking=0)

                self.line_number+=1
                buf = []
                buf_width = 0
        
        self.save_page()

def BOOKTEXT_TO_QUICK_RENDER(font_file,
                      font_size, 
                      side_margin=150, 
                      top_margin=250, 
                      leading=1.2, 
                      indent=None, 
                      file_type='.pgm',
                      chapter_numbering='roman'
                      ):

    r"""
    Convert .txt files into rendered images of book pages.
    
    The .txt files must be in a folder of their own, with each file a chapter
    Chapter files must be two-digit numbered followed by a double underscore, followed
    by the title of the chapter with spaces replaced with underscores

        ex. Chapter 5: In the Golden Age
            05__In_the_Golden_Age.txt
            
        To prevent chapter numbering, insert '--' after the chapter number
        
        ex. 05--__In_the_Golden_Age.txt
        
    The book pages can be formatted using the following arguments
        
        font type: any TrueType font file destination. *.ttf, *.otf 
            ex. font_file=r"C:\Users\User\TrueTypeFonts\Serif_Zachery.otf"
        font size: Any integer number
            ex. font_size=36
            
        Optional arguments:
            
        line spacing: Spacing between the top of a type row relative to the top
            of the row above it. Input in terms of {em}
            ex. leading=1.2 #(1.2em from the line above)
            
        indent size: Paragraph indentations in terms of {em}
            ex. indent=2 #(indented 2em from side margin)
            
        side margins: Number of pixels for the side margins
            ex. side_margin=150
            
        top margin: Number of pixels for the top (and bottom) margin
            ex. top_margin=250
            
        chapter numbering: Decimal or roman numeral chapter numbering
            ex. chapter_numbering='decimal'
            ex. chapter_numbering='roman'
    
    The function will run through all .txt files in the directory and output
    numbered pages in the file format of your choice

        ex. file_type='pgm'

    Function call example:
                
        BOOK_TO_PGM(font_file=r"C:\Users\User\TrueTypeFonts\Serif_Zachery.otf", 
                    font_size=36, 
                    side_margin=150, 
                    top_margin=250, 
                    leading=1.2, 
                    indent=2, 
                    file_type='.pgm',
                    chapter_numbering='roman'
                    )
    """
    
    path= fd.askdirectory(title="Choose your book directory")
    file = []
    chapter_pages = {}
    parameters = {}
    all_chapter_numbers = []
    page_number = 1
    global start_time
    start_time = time.time()
    
    for i, file in enumerate(os.listdir(path)):
    
        if fnmatch.fnmatch(file, '*.txt'): 
            
            with open(path + '/' + file, 'r', encoding="utf8") as chapter:
                chapter = chapter.read()
            chapter = r"{}".format(chapter)
            chapter = CHAPTER_TO_QUICK_RENDER(font_file = font_file, 
                                     font_size = font_size, 
                                     file_name = path + '/' + file, 
                                     file_type = file_type,
                                     text = chapter,
                                     side_margin = side_margin, 
                                     top_margin = top_margin, 
                                     leading = leading, 
                                     indent = indent, 
                                     page_number = page_number)
            
            chapter.write_chapter()
            title = os.path.basename(chapter.file_name).split('.')[0]
            chapter_number= os.path.basename(title).split('__')[0] 
            all_chapter_numbers.append(chapter_number)
            
            title = os.path.basename(chapter.file_name).split('.')[0] # remove the extension
            title = os.path.basename(title).split('__')[1] # remove the extension
            title = title.replace("_", " " ) # remove the underscores and replace with spaces
            
            if '--' in chapter_number:
                chapter_number = chapter_number.split('--')[0]
                chapter_pages[int(chapter_number)]=(title, chapter.first_page_number, chapter.page_number-1, False)
            else: 
                chapter_pages[int(chapter_number)]=(title, chapter.first_page_number, chapter.page_number-1, True)
            page_number = chapter.page_number  
            page_number = chapter.page_number  
            
            parameters['FONT'] = chapter.font_file
            parameters['FONT_SIZE'] = chapter.font.size
            parameters['SIDE_MARGIN'] = chapter.side_margin
            parameters['TOP_MARGIN'] = chapter.top_margin
            parameters['LEADING'] = chapter.leading
            parameters['INDENT'] = chapter.indent
    
    parameters
    with open(chapter.quick_render, 'a', encoding="utf8") as file:
        file.write("\nPARAMETERS=")
        file.write(str(parameters))
        file.write("\nPAGES=(")
        for n in range(1,page_number):
            if n == page_number-1:
                file.write("P" + str(n) + ")")
            else:
                file.write("P" + str(n) + ", ")
        file.write("\nCHAPTER=")
        file.write(str(chapter_pages))
    
#---------------------------------------------------------------------
#   MAIN
#---------------------------------------------------------------------

# Need TrueType font (.ttf or .otf)
font_file = r"C:\Users\jriffle\Documents\Demos\charmr\TrueTypeFonts\Serif_DejaVu.ttf"
font_size = 40

BOOKTEXT_TO_QUICK_RENDER(font_file, 
            font_size, 
            side_margin=150, 
            top_margin=200, 
            leading=1.4, 
            indent=2, 
            file_type='.png',
            chapter_numbering='roman' # can be 'roman' or 'decimal'
            )
global start_time
print(time.time() - start_time)