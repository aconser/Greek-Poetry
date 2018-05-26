# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 16:11:32 2018

@author: Anna

ACCENTS
Tools for looking at accents
"""
import unicodedata
from Greek_Prosody.greek_prosody import get_syllables
#%%

ACUTE = u'\u0301'
GRAVE = u'\u0300'
CIRCUMFLEX = u'\u0342'

ACCENTS = [ACUTE, GRAVE, CIRCUMFLEX]

ACCENT_DICT = {ACUTE: 'A',
               GRAVE: 'G',
               CIRCUMFLEX: 'C',
               None: '-'
               }
def remove_accents (text):
    split_chs = unicodedata.normalize("NFD", text)
    accentless = ''
    for ch in split_chs:
        if ch not in ACCENTS:
            accentless += ch
    return accentless

def get_accent (syllable):
    chs = unicodedata.normalize("NFD", syllable)
    for a in ACCENTS:
            if a in chs:
                return a
            
def get_named_accent (syllable):
    accent = get_accent(syllable)
    return ACCENT_DICT[accent]

def get_accent_index (word):
    """Breaks a word into syllables, checks each syllable for an accent, and
    returns the syllable index of the first syllable with an accent.
    
    :param str word: a word or contonation
    :return int syl_num: the index of the accented syl within the word
    """
    syl_num = 0
    for syl in get_syllables(word, resolutions=True):
        if get_named_accent(syl) != '-':
            return syl_num
        syl_num += 1

#def compare_accents (acc_a, acc_b):
#    """Identifies the basic responsion status of a syllable, returns a string
#    of the abbreviation representing that status."""
#    match_status = ''
#    if acc_a == 'A-2':
#        acc_a = '-'
#    if acc_b == 'A-2':
#        acc_b = '-'
#    if acc_a == '-' and acc_b == '-':
#        match_status = '-'
#        # Null (not accented in either)
#    elif acc_a == acc_b:
#        match_status = 'M-EX'
#        # Match-Exact (same accent in both stanzas)
#    elif acc_a != '-' and acc_b != '-':
#        match_status = 'M-CA'
#        # Match-Crossaccentual (accented in both, but with different accent type)
#    else:
#        match_status = 'C'
#        # Contradiction (accented in one but not the other)
#    return match_status