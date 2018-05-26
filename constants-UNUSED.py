# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 15:26:26 2018

@author: Anna

Constants and Character data
"""
import re

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
double_con_re = re.compile('[' + ''.join(DOUBLE_CONS) + ']')

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

SHORT_MARK = u"\u0306"

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

APOSTROPHE = u'\u02BC'
PUNCTUATION = ".,;·:'<>[]{}()=+\u037e\u0387\u00B7⟨⟩†"
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

