# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 11:37:07 2018

@author: Anna

Search Tragedy
"""

import re
from os import listdir
from stanza_utilities import load_text
from greek_prosody.scansion_dict import normalize_sigmas

#%%
directory = 'C:/Users/Anna/Anaconda3/SongDatabase/Corpus/clean_OCTs/'

A_filenames = [
 'Aesch-Ag-CLEAN.txt',
 'Aesch-Eum-CLEAN.txt',
 'Aesch-Lib-CLEAN.txt',
 'Aesch-PB-CLEAN.txt',
 'Aesch-Pers-CLEAN.txt',
 'Aesch-Seven-CLEAN.txt',
 'Aesch-Supp-CLEAN.txt']

S_filenames = [
 'Soph-Ant-CLEAN.txt',
 'Soph-El-CLEAN.txt',
 'Soph-OC-CLEAN.txt',
 'Soph-OT-CLEAN.txt',
 'Soph-Phil-CLEAN.txt',
 'Soph-Trach-CLEAN.txt']

E_filenames = [
        'Eur-Her-CLEAN.txt',
        'Eur-Or-CLEAN.txt']

all_filenames = listdir(directory)
#%%
def get_texts (author='All'):
    if author == 'Aesch':
        filenames = A_filenames
    elif author == 'Soph':
        filenames = S_filenames
    elif author == 'Eur':
        filenames = E_filenames
    else:
        filenames = all_filenames
    texts = []
    for name in filenames:
        text_tuple = (name, load_text(name, directory))
        texts.append(text_tuple)
    return texts

#%%
def search_tragedy (regex, author='All'):
    texts = get_texts (author=author)
    matches = []
    regex = normalize_sigmas(regex, lunate=True)
    regex = re.compile(regex)
    template = """
    {}, line ~{}:
     {}"""    
    for name, text in texts:
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
        
        

            
        