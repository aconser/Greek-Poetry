"""
ACCENTS

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""
import unicodedata

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

def count_circs (string):
    chs = unicodedata.normalize("NFD", string)
    return chs.count(CIRCUMFLEX)

#def get_accent_index (word):
#    """Breaks a word into syllables, checks each syllable for an accent, and
#    returns the syllable index of the first syllable with an accent.
#    
#    :param str word: a word or contonation
#    :return int syl_num: the index of the accented syl within the word
#    """
#    syl_num = 0
#    for syl in get_syllables(word, resolutions=True):
#        if get_named_accent(syl) != '-':
#            return syl_num
#        syl_num += 1
