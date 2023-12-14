# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 10:42:16 2018

RESP_CHECK_CSVS

This is a collection of scripts for applying the responsion module to my csv
files containing the paired stanzas for each play.

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""
#%%
import csv
import re
from responsion_old import resp_check_stanza

#%%
#IMPORT AND ORGANIZE PAIRS

def import_csv (file_name, directory):
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


#%%

def resp_check_play(file_name, dir_name):
    pairs = import_csv(file_name, dir_name)
    output_list = []
    issue_total = 0
    for song_num, pair, st, an, _ in pairs:
        name = song_num + ' - ' + pair
        output_list.append('\n----- {} -----'.format(name))
        check, messages = resp_check_stanza(st, an)
        output_list.extend(messages)
        issue_total +=len(messages)
        if check == True:
            output_list.append('No responsion issues found!')
    output_file = file_name+'-ISSUES.txt'
    with open(dir_name+output_file, 'w', encoding='utf-8-sig') as output:
        output.write(
                "{} TOTAL RESPONSION ISSUES in '{}'\n\n".format(
                        issue_total, file_name))
        for n in output_list:
            output.write(n + '\n')
    print("""Responsion issues exported to file:
{}""".format(dir_name+output_file))

#%%
#from os import listdir
#directory = "C:/Users/Anna/Anaconda3/SongDatabase/Corpus/Aeschylus/"
#file_names = listdir(directory)
#for f in file_names:
#    print(f)
#    
#%%
directory = "C:/Users/Anna/Anaconda3/SongDatabase/Corpus/Aeschylus/"
file_names = ['Aesch-PB.csv',
 'Aesch-Pers.csv',
 'Aesch-Seven.csv',
 'Aesch-Supp.csv']
#%%
from resp_check_csvs import resp_check_play
for f in file_names:
    resp_check_play(f, directory)
#%%
file_name = 'Eur-Her-SONGS.csv'
dir_name = 'C:/Users/Anna/Anaconda3/SongDatabase/Corpus/csv_songs_TESTING/'
           
#ORGANIZE THEM INTO A PLAY
   #%% 
def organize_pairs(csv_pairs):
    song_list = []
    current_song = []
    current_number = 1
    for song_number, strophe, antistrophe in csv_pairs:
        song_number = re.sub('SONG ', '', song_number)
        song_number = int(song_number)
        if song_number != current_number:
            song_list.append(current_song)
            current_song = []
        current_number = song_number
        st_title, st_text = re.split('\n', strophe, maxsplit=1)
        an_title, an_text = re.split('\n', antistrophe, maxsplit=1)
        current_song.append(((st_title, st_text), (an_title, an_text)))
    return song_list


    
    