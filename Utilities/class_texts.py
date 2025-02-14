# -*- coding: utf-8 -*-
"""
CLASS TEXTS

This class loads and normalizes text files, creating a list of texts that can 
be searched or otherwise accessed. The user should update the directories and
encoding type in the System Constants section below, as described.  

I have included picked text lists for tragedy from the OCTs.

NEXT STEPS (for search function)
    
    1. Add a no-diacriticals option, to make it easier to find similar segments
       in different word forms.
    
    2. Make it possible to find words split across line breaks.

    3. Add other export options, such as screening for meter types or author
    
    4. Add lemma-based search functionality.

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""

from os import listdir
import unicodedata
import re
import pickle
from Utilities.stanza_utilities import CORPUS_DIR

######################################
# SYSTEM CONSTANTS -- Edit before use!
######################################

PLAY_DIRECTORY = CORPUS_DIR +'clean_OCTs/'
#EPIC_DIRECTORY = ''

#DIRECTORIES MUST BE CHANGED TO MATCH THE LOCATION OF YOUR SOURCE FILES
# I used OCT texts downloaded as PDFs from the Oxford website. I copied them 
# into text files and used regex functions to clean up the text.
# TLG texts would be another obvious choice, but I haven't tested them. Please 
# let me know if you try it!

ENCODING = 'utf-8-sig'

#ENCODING MUST BE CHANGED TO MATCH SOURCE FILES
# Text files made in Windows (like mine are) require 'utf-8-sig'.  Other 
# systems typically use just 'utf-8'.

###################
# BASIC TEXT TOOLS
###################

def load_text (file_name, directory_name):
    """
    Loads Greek text from a .txt file ("file_name") in a given directory and returns a string. 
    
    :param str file_name: name of the file to load
    :param str directory_name: directory where the file is located
    :param str utf_type: type of encoding -- 'utf-8-sig'(default) or 'utf8' (non-Windows)
    :return: raw Greek text
    :rtype: str
    """
    with open(directory_name+file_name, encoding=ENCODING) as f:
        string = f.read()
        string = normalize(string)
    return string

def normalize (text):
    """Normalizes unicode text."""
    decomposed = unicodedata.normalize('NFD', text)
    recomposed = unicodedata.normalize('NFC', decomposed)
    return recomposed

def normalize_sigmas (text, lunate=False):
    """Standardizes sigma characters within a string of text.  Word 
    internal sigma is 'σ'; word final sigma is 'ς'; capital sigma is Σ.  
    If the lunate flag is set to True, then all sigmas are set to 'ϲ' / 'Ϲ'. 
    (Lunate sigmas are standard in the OCT texts).
    
    :param str text: a string of greek text
    :return str t: a copy of the string with the sigmas standardized.
    """
    
    if lunate:
        t = re.sub(r'[σς]', r'ϲ', text)
        t = re.sub('Σ', 'Ϲ', t)        
    else:
        t = re.sub('ϲ', 'σ', text)
        t = re.sub('Ϲ', 'Σ', t)
        t = re.sub(r'σ\b(?!’)', r'ς', t)  #corrected for elision-marking apostrophe
    return t

# For Future Refactoring:
#Based on https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html
#(maybe 'multiple replace' would be useful elsewhere, too)
#
#NORMAL_RE = re.compile(r'[σςΣ]')
#LUNATE_RE = re.compile(r'[ϲϹ]')
#
#def multiple_replace(text, adict):
#    def one_xlat(match):
#        return adict[match.group(0)]
#    return rx.sub(one_xlat, text)

###############################################################################
    
class Texts:
    def __init__ (self, text=None, lunate=False):
        self.lunate=lunate
        self.text_list = [] #Note that texts are stored as tuples (file_name, text)
        if not text:
            self.load_pickled('all-texts')
        elif text == 'all-plays':
            for f in listdir(PLAY_DIRECTORY):
                print(f)
                self.add_text(f)
#        if text = 'all-hexameter':
#        file_names = listdir(EPIC_DIRECTORY)
#            for f in file_names:
#                with open(directory + f, encoding=encoding) as file:
#                    text = file.read()
#                    text = normalize(text)
#                    self.text_list.append(text)
        else:
            self.add_text(text)
    
    def __iter__ (self):
        for text in self.texts:
            yield text
            
    @property
    def names (self):
        return [name for name, text in self.text_list]
            
    @property
    def texts (self):
        return [text for name, text in self.text_list]
        
    def add_text (self, file_name):
        """Checks for the given file_name in the default directories, and adds
        text from the file to the Texts object."""
        try:
            text = load_text(file_name, PLAY_DIRECTORY)
        except FileNotFoundError:
            #try:
            #text = load_text(file_name, EPIC_DIRECTORY)
            #except FileNotFoundError:
            raise FileNotFoundError("""{} is not a valid file name in current directories.
            Play directory is currently set to {}.
            Epic directory not yet created.""".format(file_name, PLAY_DIRECTORY))
        text = normalize_sigmas(text, lunate=self.lunate)
        self.text_list.append((file_name, text))
    
    def pickle (self, file_name, directory='.//Pickled_Texts/', overwrite=False):
        """Pickles the current text list for future use in the specified directory.
        """
        assert directory != './/Picked_Texts/Default/', \
        'You cannot overwrite the default pickled texts with this function.'
        export_file = directory + file_name + '.pkl'
        with open(export_file, 'wb+') as f:
            pickle.dump(self.text_list, f)
        print('Pickled texts saved as {}'.format(export_file))
        
    def load_pickled (self, file_name, directory='.//Pickled_Texts/Default/'):
        """Loads a previously pickled text list from the default directory. This
        overwrites any existing text_list the Text instance may have.
        """
        with open(directory + file_name +'.pkl', 'rb') as f:
            text_list = pickle.load(f)
        self.text_list = text_list
        
    def search (self, search_term, whole_word=False):
        """Searches through self.text_list for a search term and prints each line
        in which the term appears, along with the approximate line number. 
        If whole_word flag is set, then only whole words will be included.
        """
        matches = []
        regex = normalize_sigmas(search_term, lunate=True)
        if whole_word:
            search_term = '/b' + search_term + '/b'
        regex = re.compile(regex)
        template = """
        {}, line ~{}:
         {}"""
        for name, text in self.text_list:
            line_count = 0
            print("Searching " + name)
            for l in text.splitlines():
                line_count += 1
                if regex.search(l):
                    message = template.format(name, line_count, l)
                    matches.append(message)
        print()
        print('Total matches: {}'.format(len(matches)))
        for m in matches:
            print (m)
            
################################################

def Update_Default_Pickled_Texts (directory='.//Pickled_Texts/Default/'):
    
    # All Plays
    all_plays = Texts()
    all_plays.text_list = []
    for f in listdir(PLAY_DIRECTORY):
        all_plays.add_text(f)
    export_file = 'all-plays.pkl'
    with open(directory + export_file, 'wb+') as f:
        pickle.dump(all_plays.text_list, f)
    print('All Plays saved as {}'.format(export_file))
    
#    # All Epics
#    all_epics = Texts()
#    all_epics.text_list = []
#    for f in listdir(EPIC_DIRECTORY):
#        all_epics.add_text(f)
#    export_file = 'all_epics.pkl'
#    with open(directory + export_file, 'wb+') as f:
#        pickle.dump(all_epics.text_list, f)
#    print('All Epics saved as {}'.format(export_file))
    
    #All Texts
    all_texts = Texts(text = 'Aesch-Ag-CLEAN.txt')
    all_texts.text_list = all_plays.text_list # + all_epics.text_list
    export_file = 'all-texts.pkl'
    with open(directory + export_file, 'wb+') as f:
        pickle.dump(all_texts.text_list, f)
    print('All texts saved as {}'.format(export_file))
    
        
    
    