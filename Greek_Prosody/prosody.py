# -*- coding: utf-8 -*-
"""
GREEK SCANSION

This program takes a line of Greek text, breaks it into syllables and returns
the scansion as a list of syllable markers: 
    LONG ('L'), SHORT ('S'), or UNKNOWN ('X').  
The module is appropriate for analyzing prose or poetry.

Next steps for improvement are to increase the program's ability to recognize
vowels that are long or short by nature:
    1. Create a tool to macronize known suffixes (i.e. syntactical endings).
    2. Scrape the LSJ to build a macronized dictionary of ambiguous words.

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT

"""
import re
import unicodedata
from .syllables import get_syllables
from .characters import *


################################################
# SCANNING PROSODIC LENGTHS
################################################

def is_wordbreak(syl, next_syl):
    if re.search(r'\s', syl[-1] + next_syl[0]):
        return True
    else:
        return False
        
def natural_length (syl):
    """Checks the natural length of syllable, returning LONG, SHORT, or UNKNOWN.
    -- LONG are identified by long vowels, diphthongs, or long diacritics.  
    -- SHORT are identified by short vowels or a short mark.  
    -- UNKNOWN are α, ι, or υ without diacritics indicating length.  
    """
    bare_syl = basic_chars(syl)  #remove diacritics from vowels
    split_chs = unicodedata.normalize('NFD', syl) #get list including diacritics
    if re.search(long_vowel_re, bare_syl): #eta and omega
        status = LONG
    elif re.search(diphthong_re, bare_syl): #diphthongs
        status = LONG
    elif re.search(long_mark_re, split_chs): #circumflex, iota subscript, marcon
        status = LONG
    elif re.search(short_vowel_re, bare_syl): #epsilon, omicron
        status = SHORT
    elif SHORT_MARK in split_chs: #short mark
        status = SHORT
    else:                  #alpha, upsilon, iota without length diacritic
        status = UNKNOWN
    return status

def positional_length (syl, next_syl):
    """Takes the two sequential syllables and returns the positional length of 
    the first. Syllables can be created using any tool that separates vowel 
    clusters.  Stop + liquid rules follow the principles that apply in tragedy
    (see notes below).
    """
    #Check for placeholder syllables
    if '$' in syl:
        return UNKNOWN
    #Clean extraneous markings from the ends of syllables
    syl = alnum_syl(syl)
    next_syl = alnum_syl(next_syl)
    #Create a list of the consonants separating the two syls' vowel-clusters
    consonant_cluster = ''
    #Add consonants post-vowel in the first syl
    for ch in syl[::-1]:              
        if ch in CONSONANTS:
            consonant_cluster = ch + consonant_cluster
        else:
            break
    #Add consonants pre-vowel in the following syl
    for ch in next_syl:
        if ch in CONSONANTS:
            consonant_cluster +=ch
        else:
            break

    #Categorize position based on lengthening conditions:    
    con_count = len(consonant_cluster) 
    #Adjoinging vowels (generally) short within words, hiatus at word-break
    if con_count == 0:
        if is_wordbreak(syl, next_syl):
            position = HIATUS
        else:
            position = SHORT
    #Followed by a single consonant = SHORT, unless it's a double consonant
    elif con_count == 1:
        if consonant_cluster in DOUBLE_CONS:  #see note on this list about ῤ
            position = LONG
        else:
            position = SHORT
    #Two or more consonants lengthen, except certain stop+liquid combos. If 
    #these occur after a wordbreak, first syl is short; but within a word they
    #can lengthen or not as required in context.
    else:
        if consonant_cluster in MUTE_LIQUID:
            if syl[-1] in VOWELS and is_wordbreak(syl, next_syl):
                position = SHORT
            else:
                position = UNKNOWN
        else:
            position = LONG
    #short syl can function as long at line end (final anceps)
    if next_syl == 'end' and position in [SHORT, HIATUS]:
        position = UNKNOWN
    return position

##############################################
# get_prosody: PRIMARY FUNCTION  
##############################################
    


def get_prosody (line, final_anceps=False):
    """Scans a string of Greek poetry or prose, as best as possible without 
    knowing whether ambiguous vowels are long by nature. Returns the meter as a list of
    syllables marked LONG ('L'), SHORT ('S') or UNKNOWN ('X').  If resolutions
    have been marked in the text with '|', the resulting bi-syllable is marked 
    RESOLUTION ('R').
    If final_anceps is set to True, then the final syllable is marked as UNKNOWN,
    regardless of length.
    """
    line = line.strip()
    scansion = []
    syl_list = get_syllables(line, resolutions=True)
    #Iterate through syllables, determining prosodic quantity
    for i, syl in enumerate(syl_list):
        #Check for resolution
        if '|' in syl:
            scansion.append(RESOLVED)
        else:
            #Natural length of vowel
            nature = natural_length(syl) 
            #Positional length, based in part on next syllable
            try:
                next_syl = syl_list[i+1]
            except IndexError:
                next_syl = 'end'
            if '$' in next_syl:
                next_syl = 'end'
            position = positional_length(syl, next_syl)
            #Check for epic correption:
            if nature is LONG and position is HIATUS:
                scansion.append(SHORT)   #or UNKNOWN?
            #Long by position (followed by two vowels or equivalent)
            elif position is LONG:
                scansion.append(LONG)
            #Ambiguous by position (short followed by muta-cum-liquida within word)
            elif nature is SHORT and position is UNKNOWN:
                scansion.append(UNKNOWN)
            #Otherwise, syllable quantity is the natural length of vowel
            else:
                scansion.append(nature)
    #Correct for final anceps, if flag is set:
    if final_anceps:
        if scansion:
            scansion[-1] = UNKNOWN
    return scansion

def prosody_tuples (line):
    """Returns a list of tuples giving the natural and positional length of each
    syllable in a string of Greek text. Long is 'L', Short is 'S', and Unknown 
    is 'X'.
    
    If resolutions have been marked in the text with '|', the resulting 
    bi-syllable is marked RESOLUTION ('R') by nature, and Short by position.
    """
    line = line.strip()
    syl_list = get_syllables(line, resolutions=True)
    
    length_tuples = []
    
    #Iterate through syllables
    for i, syl in enumerate(syl_list):
        
        #Check for Resolution
        if '|' in syl:
            length_tuples.append(RESOLVED, SHORT)
            continue
        
        #Natural Length
        nat_length = natural_length(syl)
        
        #Positional Length
        if i == len(syl_list)-1: 
                next_syl = 'END'
        else:
            next_syl = syl_list[i+1]
        pos_length = positional_length(syl, next_syl)
        
        length_tuples.append((nat_length, pos_length))
    
    return length_tuples

def get_prosody_alt (text):
    tuples = prosody_tuples(text)
    scansion = []
    for nature, position in tuples:
        if nature is LONG and position is HIATUS:
            scansion.append(SHORT)  # or UNKNOWN?
        elif position is LONG:
            scansion.append(LONG)
        elif nature is SHORT and position is UNKNOWN:
            scansion.append(UNKNOWN)
        else:
            scansion.append(nature)
    return 
            

def pretty_scansion (scansion_list):
    scansion_dict = {'X'  : 'x',
                     'R'  : '⏔',
                     'W'  : '⏕',
                     'ANC': '⏒',
                     'A': '⏒',
                     'B': '⏓',
                     'L' : '–',
                     'S' : '⏑',
                     }
    pretty_meter = [scansion_dict[m] for m in scansion_list]
    return pretty_meter

LONGUM = '–' #(en dash)
BREVE = '⏑' #(metrical breve)
ANCEPS_L = '⏒' #(metrical long over short)
ANCEPS_S = '⏓' #(metrical short over long)
RESOLUTION_L = '⏔' #(metrical long over two shorts)
RESOLUTION_S = '⏕' #(metrical two shorts over long)
RESOLUTION = '⏖' #(metrical two shorts joined)]

SCANSION_MARKS = [LONGUM, BREVE, ANCEPS_L, ANCEPS_S, RESOLUTION_L, RESOLUTION_S, RESOLUTION]

def add_length_markers (word, scansion):
    """Identifies ambiguous vowels and adds combining diacriticals marking their
    length.
    
    NOTE: Current version marks vowels which are long by position within a word
    with a macron (not ideal). But to fix this, the function would have to use
    the data from the word_scansion function in the scan_dict module.  This can
    be fixed once all the modules are rearranged....
    """
    if len(scansion) == 0:
        return word
    macronized = ''
    syllables = get_syllables(word)
    if len(syllables) != len(scansion):
        print("Word ('{}') and scansion ('{}') do not match".format(word, scansion))
    for syl, prosody in zip(syllables, scansion):
        if natural_length(syl) is UNKNOWN and prosody is not UNKNOWN:
            for ch in syl:
                if basic_chars(ch) in VOWELS:
                    if prosody is LONG:
                        ch = add_macron(ch)
                    elif prosody is SHORT:   
                        ch = add_breve(ch)
                macronized += ch
        else:
            macronized += syl
    return macronized                
                    
def remove_length_markers (string):
    """Removes all long and short marks from a string"""
    decomposed = unicodedata.normalize('NFD', string)
    decomposed = decomposed.replace(MACRON, '')
    decomposed = decomposed.replace(SHORT_MARK, '')
    return unicodedata.normalize('NFC', decomposed)
   
def combine_scansions (scansion_list, metrical_symbols=False):
    """Extrapolates a single metrical scheme from a list of scansions containing
    unknown quantities. Each syllable's quantity is determined as follows:
        L or X in all versions --> LONG ('L')
        S or X in all versions --> SHORT ('S')
        X in all versions --> UNKNOWN ('X')
        L and S in versions --> ANCEPS ('X')
    If metrical_symbols is set to True, then the return is as metrical symbols:
        Long = '–' (en dash)
        Short = '⏑' (metrical breve)
        AncepsLong = '⏒' (metrical long over short)
        AncepsShort = '⏓' (metrical short over long)
        ResolutionLong = '⏔' (metrical long over two shorts)
        ResolutionShort = '⏕' (metrical two shorts over long)
        [Resolution = '⏖' (metrical two shorts joined)]
    """
    if not scansion_list:
        return ''
    else:
        combined = ''
        for syl in zip(*scansion_list):
            current = ''
            for prosody in syl:
                if not current or current is UNKNOWN:
                    current = prosody
                elif prosody == current:
                    continue
                else:
                    if current is LONG:
                        if prosody is SHORT:
                            current = ANCEPS_L
                        elif prosody == 'R':
                            current = RESOLUTION_L
                    elif current is SHORT:
                        if prosody is LONG:
                            current = ANCEPS_S
                        else:
                            current = SHORT
                    elif current == 'R':
                        current = RESOLUTION_S
                    elif current in [ANCEPS_L, ANCEPS_S] and prosody == 'R':
                        current = RESOLUTION_L
            combined += current
        if metrical_symbols:
            replace_list = [(LONG, LONGUM),
                            (SHORT, BREVE),
                            ('R', RESOLUTION)]
            for old, new in replace_list:
                combined = combined.replace(old, new)
        else:
            replace_list = [(ANCEPS_L, 'X'),
                            (ANCEPS_S, 'X'),
                            (RESOLUTION_L, 'R'),
                            (RESOLUTION_S, 'R')]
            for old, new in replace_list:
                combined = combined.replace(old, new)
        return combined

def display_prosody (text, final_anceps=False):
    lines = text.splitlines()
    for l in lines:
        syls = get_syllables(l.strip())
        widths = [len(s) for s in syls]
        prosody = get_prosody(l, final_anceps)
        pretty = pretty_scansion(prosody)
        sized = [p.center(w) for p, w in zip(pretty, widths)]
        print('' .join(sized))
        print(''.join(syls))
        print()
           
    
    
################################################
# TESTING
################################################
    
def simple_test():
    stanza = """ποθουμένᾳ γὰρ φρενὶ πυνθάνομαι
    τὰν ἀμφινεικῆ Δηιάνειραν ἀεί,
    οἷά τινʼ ἄθλιον ὄρνιν,
    οὔποτʼ εὐνάζειν ἀδάκρυ-
    τον βλεφάρων πόθον, ἀλλʼ
    εὔμναϲτον ἀνδρὸϲ δεῖμα τρέφουϲαν ὁδοῦ
    ἐνθυμίοιϲ εὐναῖϲ ἀναν-
    δρώτοιϲι τρύχεϲθαι, κακὰν
    δύϲτανον ἐλπίζουϲαν αἶϲαν."""
    for line in stanza.splitlines():
        print(line)
        print(get_syllables(line))
        print(get_prosody(line))
        print()