#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUICK TOOLS

Created on Thu Jun 13 15:44:05 2019

@author: anna
"""

import Utilities.class_texts as CT

Ag_text = CT.Texts(text='Aesch-Ag-CLEAN.txt')
Ag_text.search('word')

def Ag_search (word):
    Ag_text.search(word)
    return
#%%
    
def quote_text(stanza_group):
    print()
    for l in stanza_group.strophe.lines:
        print(CT.normalize_sigmas(l.text))
    
    print()
    for l in stanza_group.antistrophe.lines:
        print(CT.normalize_sigmas(l.text))
    
    print()
    for l in stanza_group.lines:
        print(' '.join(l.meter))
    
    print()
    for l in stanza_group.lines:
        print(' '.join(l.pretty_contours))
    return
    