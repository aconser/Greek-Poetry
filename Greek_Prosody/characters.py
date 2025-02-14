"""
CHARACTER TOOLS

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""

import re
import unicodedata

#########################
# CHARACTER DEFINITIONS
#########################

VOWELS = ['α', 'ε', 'η', 'ι', 'ο', 'υ', 'ω']
vowel_re = re.compile('[' + ''.join(VOWELS) + ']')

LONG_VOWELS = ['η', 'ω']
long_vowel_re = re.compile('[' + ''.join(LONG_VOWELS) + ']')

SHORT_VOWELS = ['ε', 'ο']
short_vowel_re = re.compile('[' + ''.join(SHORT_VOWELS) + ']')

DIPHTHONGS = ['αι', 'ει', 'οι', 'υι', 'αυ', 'ευ', 'ου', 'ηυ']
diphthong_re = re.compile('(' + '|'.join(DIPHTHONGS)+ ')')

IOTA_ADSCRIPTS = ['ωι', 'ηι']
iota_adscripts_re = re.compile('(' + '|'.join(IOTA_ADSCRIPTS)+ ')')

CONSONANTS = ['β', 'γ', 'δ', 'ζ', 'θ', 'κ', 'λ', 'μ', 'ν', 'ξ', 
              'π', 'ρ', 'ῥ', 'ϲ', 'σ', 'ς', 'τ', 'φ', 'χ', 'ψ'
              ]
consonant_re = re.compile('[' + ''.join(CONSONANTS) + ']')

DOUBLE_CONS = ['ζ', 'ξ', 'ψ'] 
# NOTE: Initial rho ('ῥ') should be added to this list for analyzing conversational 
# Attic, as seen especially in Comedy, to some degree in tragic trimeter,
# and almost never in tragic lyric or epic.

#double_con_re = re.compile('[' + ''.join(DOUBLE_CONS) + ']')

MUTE_LIQUID = ['θλ', 'θρ', 'θμ', 'θν',   #voiceless stop + liquid or nasal
               'κλ', 'κρ', 'κμ', 'κν',
               'πλ', 'πρ', 'πν', 'πμ',
               'τλ', 'τρ', 'τν', 'τμ',
               'φλ', 'φρ', 'φν', 'φμ',
               'χλ', 'χρ', 'χν', 'χμ',
               'βρ', 'γρ', 'δρ'          #voiced stop + rho
               ]
# NOTE: the following stop+liquid combinations have been excluded as they almost
# universally make a syllable long by position:
# long_stop_liquids = ['γμ', 'γν', 'δμ', 'δν', 'βλ', 'γλ']
# Cf. Baechle p. 309.

LONG_MARKS = [#combining forms:
              u'\u0304',  #COMBINING MACRON
              u'\u0342',  #COMBINING GREEK PERISPOMENI
              u'\u0345',  #COMBINING GREEK YPOGEGRAMMENI
              u'\u0302',  #COMBINING CIRCUMFLEX ACCENT (caret-style)
              #non-combining forms, just in case:
              u'\u00af',  #MACRON
              u'\u1fc0',  #GREEK PERISPOMENI
              u'\u037A',  #GREEK YPOGEGRAMMENI
              u'\u005E',  #CIRCUMFLEX ACCENT (caret-style)
              u'\u02C6'   #MODIFIER LETTER CIRCUMFLEX ACCENT
              ]
long_mark_re = re.compile('['+ ''.join(LONG_MARKS)+']')

SHORT_MARK = u'\u0306'
MACRON = u'\u0304'  #COMBINING MACRON
LENGTH_MARKERS = [MACRON, SHORT_MARK]

APOSTROPHE = u'\u02BC'
PUNCTUATION = ".,;·:'<>[]{}()=+\u037e\u0387\u00B7⟨⟩†—"
DIAERESIS = u'\u0308'

BREATHINGS = [u'\u0313', #COMBINING COMMA ABOVE
              u'\u0314', #COMBINING REVERSED COMMA ABOVE
              u'\u1fbf', #GREEK PSILI
              u'\u1ffe'  #GREEK DASIA
              ]

ACUTE = u'\u0301'
GRAVE = u'\u0300'
CIRCUMFLEX = u'\u0342'

ACCENTS = [ACUTE, GRAVE, CIRCUMFLEX]

UNKNOWN = 'X'
LONG = 'L'
SHORT = 'S'
RESOLVED = 'R'
EQUAL_LONG = [LONG, RESOLVED]   # long and resolved are equal
HIATUS = 'S-H' # Used only for positional length.  Also used word-internally for
               # syllable break without consonant.

#############################
# TOOLS FOR CLEANING STRINGS
#############################

def basic_chars (string):
    """Removes diacritical markings from a string or character and makes lowercase.
    
    :param str string: a string of text
    :return: a string of text without diacritical markings
    :rtype: str
    """
    basic_chars = ''
    for ch in string:
        bare_ch = unicodedata.normalize('NFD', ch)[0]
        basic_chars += bare_ch
    basic_chars = basic_chars.lower()
    return basic_chars

def alnum_syl (string):
    """Removes everything except alphanumeric characters from a syllable,
    including apostrophes indicating apocope. Also makes lowercase.
    """
    text = string
    text = re.sub(r'\W+', '', text)
    text = re.sub(APOSTROPHE, '', text)
    text = text.lower()
    return text

################################################
# TOOLS FOR IDENTIFYING CHARACTERS
################################################
    
def has_consonant (string):
    for ch in unicodedata.normalize('NFD', string).lower():
        if ch in CONSONANTS:
            return True
        else:
            return False

def is_mute_liquid (ch_a, ch_b):
    if ch_a.lower() + ch_b.lower() in MUTE_LIQUID:
        return True
    else:
        return False
        
def has_vowel (string):
    for ch in unicodedata.normalize('NFD', string).lower():
        if ch in VOWELS:
            return True
    return False

def has_diaeresis (string):
    if DIAERESIS in unicodedata.normalize('NFD', string):
        return True
    else:
        return False

def has_breathing (string):
    for ch in unicodedata.normalize('NFD', string):
        if ch in BREATHINGS:
            return True
    return False

def has_circumflex (string):
    if CIRCUMFLEX in unicodedata.normalize('NFD', string):
        return True
    else:
        return False

def has_accent (string):
    for ch in unicodedata.normalize('NFD', string):
        if ch in ACCENTS:
            return True
    return False

def has_length_mark(string):
    for ch in unicodedata.normalize('NFD', string):
        if ch in LENGTH_MARKERS:
            return True
    return False

#################################
# TOOLS FOR ADDING LENGTH MARKS
#################################
    
def add_macron (vowel):
    subchars = unicodedata.normalize('NFD', vowel)
    new = subchars[0] + MACRON + subchars[1:]
    macronized = unicodedata.normalize('NFC', new)
    return macronized

def add_breve (vowel):
    subchars = unicodedata.normalize('NFD', vowel)
    new = subchars[0] + SHORT_MARK + subchars[1:]
    macronized = unicodedata.normalize('NFC', new)
    return macronized

