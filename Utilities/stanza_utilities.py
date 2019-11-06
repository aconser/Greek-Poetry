
# coding: utf-8

# stanza_utilities
#
# a set of tools and constants for use in my python library for analyzing antistrophic song.

import re
import csv

CORPUS_DIR = '/Users/anna/Documents/Python Scripts/Corpus/'

def save_txt (filename, string):
    """Save a string as a txt file in the Song_Database directory."""
    directory = CORPUS_DIR
    export_file = directory + filename + '.txt'
    with open(export_file, "w", encoding='utf-8') as output:
        output.write(string)
    print('Saved string as {}'.format(export_file))
    
def save_csv (filename, mylist):
    """Save a string as a txt file in the Song_Database directory."""
    directory = '../'
    export_file = directory + filename + '.csv'
    with open(export_file, "w", encoding='utf-8') as output:
        for item in mylist:
            if type(item) is not str:
                export_text = ','.join(item)
            else:
                export_text = str(item)
            output.write(export_text + '\n')
    print('Saved list as {}'.format(export_file))
    
def load_text (file_name, directory_name, utf_type='utf-8-sig'):
    """
    Loads Greek text from a .txt file ("file_name") in a given directory and returns a string.
    Text files made in Windows require utf_type='utf-8-sig'. 
    
    :param str file_name: name of the file to load
    :param str directory_name: directory where the file is located
    :param str utf_type: type of encoding -- 'utf-8-sig'(default) or 'utf8' (non-Windows)
    :return: raw Greek text
    :rtype: string
    """
    with open(directory_name+file_name, encoding=utf_type) as f:
        raw_string = f.read()
    return raw_string

def import_csv (file_name, directory):
    """Imports a .csv file where each row contains (a) the song number, (b) the
    stanza letter, (c) strophe text, (d) antistrophe text, (e) metrical scansion 
    (where available) and (f) notes. 
    Returns a list of lists, each representing a row (i.e. a stanza pair) in the 
    original.
    """
    stanza_list = []
    if file_name.lower().endswith('csv'):
        file_name = file_name[:-4]
    csv_file = directory + file_name + '.csv'
    with open(csv_file, 'r', encoding='utf8') as file:
        reader = csv.reader(file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
        for row in reader:
            stanza_list.append(row)
    return stanza_list

def import_csv_OLD (file_name, directory):
    """Imports a .csv file where each row contains (a) the song number, (b) the
    stanza letter, (c) strophe text, (d) antistrophe text, and (e) notes. 
    Returns a list of lists (each representing a row in the original).
    """
    stanza_list = []
    if file_name.lower().endswith('csv'):
        file_name = file_name[:-4]
    csv_file = directory + file_name + '.csv'
    with open(csv_file, 'r', encoding='utf8') as file:
        reader = csv.reader(file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
        for row in reader:
            stanza_list.append(row)
    return stanza_list

def clean_string (raw_str):
    text = raw_str
    sub_list = [
        (u'\xa0', ' '),   #replace special tab characters with spaces
        (r'-\n\s*', ''),  #join words broken across lines by hyphens
        (r'^\s+', ''),    #remove extra whitespace at start
        (r'\n\s+', '\n'), #remove extra whitespace at start of lines
        (r'\n', ' '),     #replace all linebreaks with spaces
        (r'\s\s+', ' ')   #replace multiple spaces with a single space
    ]
    for old, new in sub_list:
        text = re.sub(old, new, text)
    return text