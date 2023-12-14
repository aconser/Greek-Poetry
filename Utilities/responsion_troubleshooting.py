#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 10:29:47 2023

@author: conser
"""
import Analysis.class_play as CP
Trach = CP.load_play('Trachiniae', 'Soph-Trach', author='Sophocles')
Trach.display()
Trach.export_analysis(Operating_Location + 'Corpus/Sophocles/')
   
#%%
import pandas as pd
import Greek_Prosody.syllables as S
Operating_Location = '/Users/conser/Library/CloudStorage/OneDrive-UniversityofCincinnati/Conser Research/Python Scripts/'

CSV = Operating_Location + r'Corpus/Sophocles/Soph-OT.csv'

stanzas = pd.read_csv(CSV, header=None, index_col=False)
stanzas.columns = ['song', 'letter', 'strophe', 'ant', 'meter', 'notes']

def check_pair (stanzas, index):
    """ stanzas here refers to a pandas object created above"""
    strophe = stanzas.iloc[index]['strophe']
    ant = stanzas.iloc[index]['ant']
    #print counts
    str_syls = S.get_syllables(strophe)
    ant_syls = S.get_syllables(ant)
    print('STROPHE')
    print ('count: '+ str(len(str_syls)))
    print()
    print('ANTISTROPHE')
    print ('count: '+ str(len(ant_syls)))
    print()
    #print interlaced lines
    str_lines = strophe.splitlines()
    ant_lines = ant.splitlines()
    line_pairs = zip(str_lines, ant_lines)
    for p in line_pairs:
        for l in p:
            syls = S.get_syllables(l)
            print (' - '.join(['{:<6}'.format(s.strip()) for s in syls]))
        print()
        

check_pair(stanzas, 9)