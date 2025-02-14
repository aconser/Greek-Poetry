# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 19:27:25 2018

@author: Anna
"""
import re
import csv

def import_csv_pairs(file_name, directory):
    """Imports a .csv file where each row contains (a) the song number ("SONG %d"),
    (b) strophe text, (c) antistrophe text, and (d) any notes. 
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


#HARVEST NAMES AND CLEAN THEM UP

ST_RE = r'\s*\[ϲτρ\.(?: \w+)*\n'
AN_RE = r'\s*\[ἀντ\.(?: \w+)*\n'
STANZA_NAME_RE = re.compile(ST_RE + '|' + AN_RE)

SPEAKER_RE = re.compile(r"""
                        ^\s*        #at line start (including leading whitespace)
                        [Α-ΩϹ]      #a capital letter
                        (?:\w+\.    #letters up until a period (abbrev.)
                        |[Α-ΩϹ]+)   #or a string of ALL-CAPS (char entrance) 
                        \s          #whitespace
                        """, re.MULTILINE | re.X)

def get_stanza_name(stanza_text):
    """If a stanza (str) begins with a strophe or antistrophe label, this function
    finds and returns that text as a string."""
    text = stanza_text
    name = STANZA_NAME_RE.findall(text)[0]
    return name

def just_stanza (stanza_text):
    """Removes initial labels: (i) stanza name, (ii) speaker attribution."""
    text = stanza_text
    text = re.sub(ST_RE, '', text)
    text = re.sub(AN_RE, '', text)
    text = re.sub(SPEAKER_RE, '', text)
    return text

def reformat_csv (file_name, directory):
    stanza_list = import_csv_pairs(file_name, directory)
    new_list = []
    for song_num, st, an, notes in stanza_list:
        song_num = "\"" + song_num[5:] + "\""
        stanza_letter = "\"" + re.findall(r'^\[...\. *(.*)\n', st)[0] + "\""
        st_speaker = re.findall(SPEAKER_RE, st)
        if st_speaker:
            notes = 'St speaker: ' + st_speaker[0].strip() + '\n' + notes
        an_speaker = re.findall(SPEAKER_RE, an)
        if an_speaker:
            notes = 'An speaker: ' + an_speaker[0].strip() + '\n' + notes
        notes = "\"" + notes +"\""
        st = "\"" + just_stanza(st) + "\""
        an = "\"" + just_stanza(an) + "\""
        row = [song_num, stanza_letter, st, an, notes]
        new_list.append(row)
    export_file_name = file_name + "-NEW.csv"
    with open(directory+export_file_name, "w", encoding='utf-8') as output:
        for row in new_list:
            output_text = ','.join(row)+'\n'
            output.write(output_text)
            
#%%

#files = listdir(directory)
#for f in files:
#    print(f)
#    reformat_csv(f, directory)