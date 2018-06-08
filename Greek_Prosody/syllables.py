# -*- coding: utf-8 -*-
"""
SYLLABLES

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""
from .characters import *
   
def is_vowel_combo (ch_a, ch_b):
    """Determines whether two vowels are one syllable (a diphthong or adscript)
    or two syllables (incompatible vowels, or marked by breathing/diaeresis).
    There is unfortunately some ambiguity in using the OCT texts, since they are
    not consistent in differentiating adscripts and diaereses, e.g. Δηιάνειρα 
    is not an adscript, while ἆιστος can be either, depending on accentuation
    and meter. 
    
    In the case of apparent adscripts with missing diaereses, I will have to 
    add these to the text manually (e.g. Δηϊάνειρα). If, however, the iota has
    an accent, this distinguishes it as two syllables.
    
    In the case of alpha + iota, the program defaults to separate syllables,
    with the exception of alphas which are accented with a circumflex, e.g. 
    ἆιϲτοϲ.  In a basic search of Aeschylus and Sophocles, these were all
    subscripts. Other subscripts may have to be joined as resolutions.
    """
    #Check for diaeresis (two syls) or length mark on second vowel (trace of a 
    # diaeresis which was separated by the length mark -- unicode is deficient here.)
    if has_diaeresis(ch_b) or has_length_mark(ch_b):
        return False
    clean_chs = basic_chars(ch_a) + basic_chars(ch_b)
    #Check for diphtongs (one syl)
    if clean_chs in DIPHTHONGS:
        #Except with diacritical on first vowel (two syls)
        if has_breathing(ch_a) or has_accent(ch_a):
            #Unless it is alpha with iota-subscript, sometimes with circumflex
            if clean_chs == 'αι' and has_circumflex(ch_a):
                return True
            else:
                return False
        else:
            return True
    elif clean_chs in IOTA_ADSCRIPTS:
        if has_accent(ch_b):
            return False
        else:
            return True          #This will occasionally be wrong
    else:
        return False

def is_syl_break (pre_next_ch, next_ch, ch):
    """Determines whether ch is the beginning of a syllable, with reference to 
    next_ch, the character to the LEFT of it in the text.
    NOTE: this function itself does not check whether the syllable contains a
    vowel yet, which is determined in the higher order processing.
    """
    #If preceded by whitespace, break
    if next_ch.isspace():
        return True
    #If preceded by non-letter, break
    elif not next_ch.isalpha() and next_ch not in LENGTH_MARKERS:
        return True
    #Adjacent vowels break, unless a vowel combo
    elif has_vowel(ch) and has_vowel(next_ch):
        if is_vowel_combo(next_ch, ch):
            return False
        else:
            return True
    #Consonants break, unless part of a mute-liquid or initial consonant group.
    elif has_consonant(ch):
        if is_mute_liquid(next_ch, ch):
            return False
        elif has_consonant(next_ch) and pre_next_ch.isspace():
            return False
        else:
            return True
    #Other circumstances (i.e. vowel preceded by consonant) do not break
    else:
        return False

def join_vowelless(syl_list):
    """Iterates through a list and joins syllables without vowels (e.g. "τʼ") 
    to the following syllable.""" 
    new_syls = []
    hold_syl = ''
    for s in syl_list:
        if has_vowel(s) or '$' in s:
            new_syls.append(hold_syl + s)
            hold_syl = ''
        else:
            hold_syl += s
    return new_syls

def join_resolutions(syl_list):
    """Iterates through a list and joins syllables divided by a '|', indicating
    a metrical resolution.
    """ 
    new_syls = []
    waiting = False
    for s in syl_list:
        #if previous syl ended in pipe, append current syl to previous syl
        if waiting == True:
            new_syls[-1] += s
            waiting = False
        #if current syl starts with pipe, append it to previous syl
        elif s.strip().strip(PUNCTUATION).startswith('|'):
            try:
                new_syls[-1] += s
            except IndexError:       #Exception for processing individual words
                new_syls.append(s)
        #otherwise, add the syl as a new item in the list
        else:
            new_syls.append(s)
        #then, if this syl ends with a pipe, mark waiting as False
        if s.strip().strip(PUNCTUATION).endswith('|'):
            waiting = True
    return new_syls

def get_syllables (text, strip=False, resolutions=True):
    """Breaks a string of Greek text into its constituent syllables. Single 
    consonants are grouped with the following vowel, unless word-final. Double
    consonants are split between two syllables, unless word-initial or one of 
    the muta-cum-liquida combinations, which are treated as a single consonant.
    Punctuation is grouped with its adjacent syllable.  By default whitespace
    is likewise included, but it can be removed by setting the strip flag to True.
    
    If the resolutions flag is set to True, then metrical resolutions marked in
    the text with '|' between the constituent syllables are returned as a 
    single conjoined syllable.
    
    If the text is marked with placeholder syllables ($), these are treated as
    independent syllables.
    
    :param str text: a string of Greek text, resolutions marked if desired.
    :param bool strip: if marked True, trailing whitespace will be removed
    :param bool resolutions: if marked True, resolved syllables will be joined
    :return list syls: a list of strings, each containing a syllable
    
    """
    syls = []
    current_syl = ''
    #Iterate through text in reverse, adding each char to the front of the 
    #current syl, then checking whether to continue or start a new syl.
    for i, ch in reversed(list(enumerate(text))):
        current_syl = ch + current_syl
        #If we've reached the first character, stop here.
        if i == 0:             
            syls = [current_syl] + syls 
            break
        #Check for placeholder syllable ($)
        if '$' in current_syl:
            syls = [current_syl] + syls 
            current_syl = ''
            continue
        #If syllable doesn't have a vowel, keep adding characters
        if not has_vowel(current_syl):
            continue
        #If remaining text is whitespace, continue, so it is grouped with a syl.
        if text[:i].isspace():
            continue
        #Check for the beginning of a syllable, and if so start a new one.
        next_ch = text[i-1]
        try:
            pre_next_ch = text[i-2]
        except IndexError:
            pre_next_ch = ' '
                #print("PRE: {} / NEXT: {} / CUR: {}".format(pre_next_ch, next_ch, ch))
        if is_syl_break(pre_next_ch, next_ch, ch):
            syls = [current_syl] + syls
            current_syl = ''
    if strip == True:
        syls = [syl.strip() for syl in syls]
    if resolutions == True:
        syls = join_resolutions(syls)
    final_syls = join_vowelless(syls)
    return final_syls

def count_syllables (text):
    syls = get_syllables(text)
    return len(syls)
