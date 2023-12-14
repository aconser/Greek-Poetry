# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 19:01:06 2018

Trimeter Scansion

This program will take a line of iambic trimeter and return the scansion, as far
as can be determined.  It was able to scan 70 of 73 lines from the beginning of
Sophocles' Trachiniae.  Lines where it failed involved repeated resolutions in
combination with unknown natural quantities.

Next steps:
    - The best way forward will be to identify more natural quantities, by marking
    the text with macrons, or building a function to identify common prefixes 
    with ambiguous vowel (e.g. "δια"), to cut down on the number of unknowns.
    - Take account of correption
    - I haven't incorporated synezesis, but it hasn't been an issue so far, and
    may be rare enough to just ignore.  More testing needed.
    
@author: Anna Conser
"""

from Greek_Prosody.prosody import get_prosody
import re

NONFINAL_METRA = ['XLSL',
                  'SLSL',
                  'LLSL',
                  'XSSSL', #First Resolution
                  'SSSSL',
                  'XLSSS', #Second Resolution
                  'SLSSS',
                  'LLSSS', #Dactyl
                  'LSSSL',
                  'SSLSL' , #Anapest
                  'XSSSSS', #Double resolution
                  'SSSSSS',
                  'LSSSSS', #Dactyl + Resolution
                  'SSLSSS' #Anapest + Resolution
                  ]
FINAL_METRA = ['XLSX',
               'XLSL',
               'XLSS',
               'SLSX',
               'SLSL',
               'SLSS',
               'LLSX',
               'LLSL',
               'LLSS',
               'XSSSX', #First Resolution
               'SSSSL',
               'SSSSS',
               'XLSSS', #Second Resolution
               'SLSSS',
               'LLSSS',
               'LSSSX', #Dactyl (Can we have this in final metron?)
               'LSSSL',
               'LSSSS', 
               'SSLSX', #Anapest (Can we have this in final metron?)
               'SSLSL',
               'SSLSS',
               'XSSSSS', #Double resolution
               'SSSSSS',
               'LSSSSS', #Dactyl + Resolution
               'SSLSSS'] #Anapest + Resolution

def get_metron (meter_string, final=False, conservative=False):
    regex = meter_string.replace('X', '.')  
    regex = re.compile(r'^' + regex + r'$')
    if final:
        possible_metra = [x for x in FINAL_METRA if regex.match(x)]
    else:
        possible_metra = [x for x in NONFINAL_METRA if regex.match(x)]
    if not possible_metra:
        return None
    else:
        metron = possible_metra[0]
        if conservative and len(possible_metra) > 1:
            safe_metron = ''
            for position in zip(*possible_metra):
                first = position[0]
                if all(version == first for version in position):
                    safe_metron += first
                else:
                    safe_metron += 'X'
            return safe_metron
        else:
            return metron

def print_error (line, raw_meter):
    print('FAILED TO SCAN LINE:')
    print(line)
    print(raw_meter)
    print()
    
def scan_trimeter (line, print_errors=True, conservative=False):
    """Takes the string for a line of Greek iambic trimeter and returns the 
    scansion as well as can be determined based on available information. The 
    default method is to scan from back to front, and if that doesn't work, it
    tries again from the front (by calling scan_trimeter_2()). In instances where
    a satisfactory scansion cannot be determined, the program prints a message 
    announcing the failure, without throwing an error.
    
    Scansion is returned as a string of letters indicating metrical length:
        'L' (long), 
        'S' (short), or 
        'X' (unknown)
        
    :param str line: a line of text (presumably) in iambic trimeter
    :return list trimeter: a list of strings indicating metrical quantities
    """
    
    raw_meter = get_prosody(line)
    if not 12 <= len(raw_meter) <= 18:
        if print_errors:
            print_error(line, raw_meter)
        return None
    iambic_metra = []
    current = ''
    is_last = True               # starting from the end
    countdown = len(raw_meter)
    
    # Iterate through meter in REVERSE, adding each length to the FRONT of current metron
    for m in raw_meter[::-1]:
        current = m + current
        
        # Check for invalid conditions
        countdown -=1
        if len(iambic_metra) == 3:   # If these are syls in addition to a trimeter, break.
            iambic_metra = []
            break
        elif len(current) < 4 or \
            countdown < 4 and countdown is not 0:
            continue   #If less than 4 syls, or leaving orphans, keep adding syls
        else:
            
            # Check for a valid metron, add to list of iambic_metra, continue
            metron = get_metron(current, final=is_last, conservative=conservative)
            if not metron:
                continue
            else:
                iambic_metra = [metron] + iambic_metra
                current = ''
                is_last = False
    
    # Flatten the trimeter into a single list
    trimeter = [m for metron in iambic_metra for m in metron]
    
    #Check for a complete line of trimeter and return
    if len(trimeter) == len(raw_meter) and len(iambic_metra) == 3:
        return trimeter
    else:
        
        #If that fails, attempt again from the front, using _scan_trimeter_2():
        trimeter = _scan_trimeter_2(raw_meter, conservative=conservative, print_errors=print_errors)
        if trimeter:
            return trimeter
        else:
            if print_errors:
                print_error(line, raw_meter)
            return None
                
def _scan_trimeter_2 (raw_meter, conservative=False, print_errors=False):
    """Does the same thing as scan_trimeter(), but works from front to back.
    This is less effective overall, and is implemented as a secondary method,
    catching a few of the lines that the primary function cannot scan.
    
    :param str line: a line of text (presumably) in iambic trimeter
    :return list trimeter: a list of strings indicating metrical quantities
    """
    
    iambic_metra = []
    current = ''
    is_last = False              # starting from the front
    countdown = len(raw_meter)
    metra_count = 0
    # Iterate through meter, adding each length to the END of current metron
    for m in raw_meter:
        current = current + m     
        # Check for invalid conditions and continue
        countdown -= 1
        if len(iambic_metra) == 3:   # If these are syls in addition to a trimeter, break.
            iambic_metra = []
            break
        elif len(current) < 4 or \
            (countdown < 4 and countdown is not 0):
                continue  #If less than 4 syls, or leaving orphans, keep adding syls
        else:
            # Check for a valid metron, add to list of iambic_metra, continue
            metron = get_metron(current, final=is_last, conservative=conservative)
            if not metron:
                continue
            elif len(metron) > 6:  # If we have exceeded possible syllables, break.
                iambic_metra = []
                break
            else:
                iambic_metra.append(metron)
                current = ''
                metra_count += 1
                if metra_count == 2:       # check whether we are at the last foot
                    is_last = True
    trimeter = [m for metron in iambic_metra for m in metron]
    if len(trimeter) == len(raw_meter) and len(iambic_metra) == 3:
        return trimeter
    else:
        return None


##############################
# TOOL FOR EXTRACTING A BUNCH OF TRIMETERS FROM A PLAY FILE
##############################
        
SPEAKER_RE = re.compile(r"""
                        ^\s*        #at line start (including leading whitespace)
                        [Α-ΩϹ]      #a capital letter
                        (?:\w+\.    #letters up until a period (abbrev.)
                        |[Α-ΩϹ]+)   #or a string of ALL-CAPS (char entrance) 
                        \s          #whitespace
                        """, re.MULTILINE | re.X)
ST_RE = re.compile(r'\s*\[[ϲσ]τρ\.(?: \w+)*\n')
AN_RE = re.compile(r'\s*\[ἀντ\.(?: \w+)*\n')
    
def just_trimeters (text):
    """Removes character names and other intrusions from a text, as well as any
    lines which the scan_trimeter module cannot successfully scan as trimeter.
    Return is a list of strings of trimeter.
    """
    text = SPEAKER_RE.sub('', text)
    text = ST_RE.sub('', text)
    text = AN_RE.sub('', text)
    lines = text.splitlines()    
    trimeters = []
    for l in lines:
        if scan_trimeter(l, print_errors=False, conservative=True):
            trimeters.append(l)
    return trimeters

def just_hexameters (text):
    """Placeholder for when the hexameter scanner is added."""
    pass

###################################
# FOR POSSIBLE USE LATER
###################################

##IAMBIC_NONFINAL = re.compile(r"""
#                             ^(?:SS|L|S|X|SX|XS)  #anceps (with anapest)
#                             (?:SS|L|X|SX|XS)     #long / resolved
#                             (?:S|X)              #short
#                             (?:SS|L|X|XS|SX)$    #long / resolved
#                             """, re.VERBOSE)
#IAMBIC_FINAL = re.compile(r"""
#                             ^(?:SS|L|S|X|SX|XS)  #anceps (with anapest)
#                             (?:SS|L|X|SX|XS)     #long / resolved
#                             (?:S|X)              #short
#                             (?:L|S|X)$           #final anceps
#                             """, re.VERBOSE)
