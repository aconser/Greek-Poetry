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

################################################
# CHARACTER DEFINITIONS, and a couple of tools
################################################

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
# Attic, as seen in especially in Comedy, to some degree in tragic trimeter,
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
HIATUS = 'S-H' # Used only for positional length.  Also used word-internally for
               # syllable break without consonant.

def strip_str (string):
    """Removes diacritical markings from a string and makes lowercase.
    
    :param str string: a string of text
    :return: a string of text without diacritical markings
    :rtype: str
    """
    bare_str = ''
    for ch in string:
        bare_ch = unicodedata.normalize('NFD', ch)[0]
        bare_str += bare_ch
    bare_str = bare_str.lower()
    return bare_str

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
# MAKING SYLLABLES
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
    clean_chs = strip_str(ch_a) + strip_str(ch_b)
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
#%%   
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
            new_syls[-1] += s
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
    syl_count = len(syls)
    resolution_count = text.count('|')
    return syl_count-resolution_count

    

#%%
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
    bare_syl = strip_str(syl)  #remove diacritics from vowels
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
    scansion_dict = {'X'  : '⏒',
                     'R'  : '⏔',
                     'ANC': '⏒',
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
                        elif prosody is 'R':
                            current = RESOLUTION_L
                    elif current is SHORT:
                        current = ANCEPS_S
                    elif current is 'R':
                        current = RESOLUTION_S
                    elif current in [ANCEPS_L, ANCEPS_S] and prosody is 'R':
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

def add_length_markers (word, scansion):
    """Identifies ambiguous vowels and adds combining diacriticals marking their
    length.
    
    NOTE: Current version marks vowels which are long by position within a word
    with a macron (not ideal). But to fix this, the function would have to use
    the data from the word_scansion function in the scan_dict module.  This can
    be fixed once all the modules are rearranged....
    """
    if len(scansion) is 0:
        return word
    macronized = ''
    syllables = get_syllables(word)
    if len(syllables) != len(scansion):
        print("Word ('{}') and scansion ('{}') do not match".format(word, scansion))
    for syl, prosody in zip(syllables, scansion):
        if natural_length(syl) is UNKNOWN and prosody is not UNKNOWN:
            for ch in syl:
                if strip_str(ch) in VOWELS:
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