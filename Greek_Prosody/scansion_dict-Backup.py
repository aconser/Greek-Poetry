# -*- coding: utf-8 -*-
"""
CREATE SCANSION DICTIONARY

Created on Thu May 10 15:53:27 2018

@author: Anna
"""

#%% STEP ONE: TOOLS TO PAIR METER AND WORDS

import re
import unicodedata
from .characters import PUNCTUATION
from .syllables import get_syllables
from .prosody import positional_length, prosody_tuples, add_length_markers, remove_length_markers
from .trimeter import scan_trimeter, just_trimeters

def lossless_split(string, separator=r'\s+'):
    regex = re.compile(r'(' + separator + r')')
    split = regex.split(string)
    chunks = []
    hold = ''
    for s in split:
        if hold:
            chunks.append(hold + s)
            hold = ''
        else:
            hold = s
    if hold:
        chunks.append(hold)
    return chunks

def normalize_sigmas (text, lunate=False):
    """Standardizes sigma characters within a string of text.  Word 
    internal sigma is 'σ'; word final sigma is 'ς'; capital sigma is Σ.  
    If the lunate flag is set to True, then all sigmas are set to 'ϲ' / 'Ϲ'. 
    (Lunate sigmas are standard in the OCT texts).
    
    :param str text: a string of greek text
    :return str t: a copy of the string with the sigmas standardized.
    """
    
    if lunate==True:
        t = re.sub(r'[σς]', r'ϲ', text)
        t = re.sub('Σ', 'Ϲ', t)        
    else:
        t = re.sub('ϲ', 'σ', text)
        t = re.sub('Ϲ', 'Σ', t)
        t = re.sub(r'σ\b(?!’)', r'ς', t)
    return t

def normalize (text):
    decomposed = unicodedata.normalize('NFD', text)
    recomposed = unicodedata.normalize('NFC', decomposed)
    return recomposed

def just_word (string):
    """Removes whitespace and punctuation from a string (not including apostrophe
    marking elision).
    
    Note: this task cannot be accomplished by removing \W (non-alphanumeric characters),
    because that includes some diacriticals (e.g. breathing mark combined with macron).
    
    :param str string: a string containing a word
    :return str just_word: just the word, with all whitespace and punctuation removed.
    """
    regex = re.compile(r'[\s' + re.escape(PUNCTUATION) + ']')
    just_word = regex.sub('', string)
    #text = text.lower()
    return just_word

def no_enclitic(string):
    """Strips a vowelless enclitic from the syllable it has been grouped with.
    
    :param str string: a string containing a word and (potentially) a vowelless enclitic.
    :return str string: just the main word, with enclitic and whitespace removed.
    """
    return re.sub(r' [⟨⟩\w]+', ' ', string)

WORD_END_RE = re.compile(r'.*[\s' + re.escape(PUNCTUATION) + '’]$')

def is_word_end(string):
    return bool(WORD_END_RE.search(string))

def word_scansion (line, meter='trimeter'):
    """Takes a line of poetry and returns a list containing the prosodic length
    of each syllable as it would be if the words of the line appeared in isolation.
    The length of indeterminate vowels is filled in, when possible, by the 
    metrical pattern of the poetic line. 
    """
    syllables = get_syllables(line)
    meter_tuples = prosody_tuples(line)
    trimeter = scan_trimeter(line, print_errors=False, conservative=True)
    assert trimeter, """This line did not scan properly:
        {}
        """.format(line)
    syl_count = len(syllables)
    scansion = ''
    for i, syl, nat_pos, trim in zip(
            range(syl_count), syllables, meter_tuples, trimeter
            ):
        nature, position = nat_pos
        word_end = is_word_end(syl)
        #Long by Nature
        if nature == 'L':
            length = 'L'
        #Check whether positional length at end of word is internal to the word,
        #or caused by the following word.
        elif word_end and position != 'S':
            bare_syl = no_enclitic(syl)
            position_in_word = positional_length(bare_syl, 'α')
            if position_in_word == 'L':
                length = 'L'
            elif position_in_word == 'X':
                length = 'X'
            else:
                length = nature
        #Otherwise, the trimeter scansion reflects the word scansion.
        else:
            length = trim
        scansion += length
    #Correct for final anceps
    if scansion[-1] == 'S':
        if meter_tuples[-1][0] == 'X':  #If ambiguous vowel
            scansion = scansion[:-1] + 'X'
    return(scansion)
            
def scanned_words (line, meter='trimeter'):
    """Takes a line of poetry and returns a list of tuples containing each word
    and its independent prosodic scansion, as best it can be determined within 
    the line.  The word is a string, the scansion is a list.
    """
    words = [just_word(w) for w in line.split()]   
    syl_counts = [len(get_syllables(w)) for w in words]
    line_scansion = word_scansion(line)
    word_tuples = []
    start = 0
    for word, n in zip(words, syl_counts):
        end = start + n
        w_scansion = line_scansion[start:end]
        #if word == 'ἐν'and w_scansion == 'L':
        #    raise AssertionError
        word_tuples.append((word, w_scansion))
        start = end
    return word_tuples


#%%  STEP TWO: CLASS SCANSION DICT


# =============================================================================
# Building a dictionary as
# SCANSTION_DICT = {word : [prosody, prosody, prosody...], 
#                   word : [prosody, prosody, prosody...]
#                   }
# =============================================================================
from operator import itemgetter
import pickle
from greek_prosody import combine_scansions
import re

class Scansion_Dict ():

    def __init__ (self, lunate=False):
        self.lunate = lunate
        self.raw = {}
        self._quantified = {}
        self._consolidated = {}
    
    def __getitem__ (self, key):
        try:
            return self.consolidated[key]
        except KeyError:
            raise KeyError("Key ('{}') not in dictionary".format(key))

    def __contains__ (self, key):
        return key in self.raw.keys()

    def __len__ (self):
        return len(self.raw)
        
    def add_text (self, text, meter='trimeter'):
        """Adds a list of scanned_words tuples to the raw dictionary, creating
        new keys/entries for new word forms and otherwise adding the prosody to 
        the existing entry, which is a list of occuring prosodies.  If texts are
        added multiple times, the repeats are not treated differently.
        
        Resets the consolidated and quantified dicts so they are 
        recalculated.
        
        param str text: a string of ancient Greek text in a covered meter.
        param str meter: identifies the meter (currently only trimeter is covered)
                            so it can be scanned properly.
        return None: the word and prosody are added to the self.raw dict
        
        """
        text = normalize(text)
        text = normalize_sigmas(text, lunate=self.lunate)
        word_tuples = []
        if meter == 'trimeter':
            for line in just_trimeters(text):
                try:
                    sw = scanned_words(line)
                except AssertionError:
                    print('FOUND IT')
                    print(line)
                    print()
                word_tuples.extend(sw)
        #if meter == 'hexameter': (SOMEDAY)
        #   for line in ... etc.
        
        for word, prosody in word_tuples:
            key = remove_length_markers(word)
            if key in self.raw:
                self.raw[key].append(prosody) 
            else:
                self.raw[key] = [prosody]
        
        #Reset processed dicts so they are recalculated
        self._quantified = {}
        self._consolidated = {}
    
    @property
    def quantified (self):
        """Creates a copy of the raw dictionary, so that each entry is a list of
        tuples, each containing a possible scansion and the number of attestations
        in the texts that have been added to the dictionary. The entries are
        sorted in order of frequency.
            e.g. {ἀτρειδῶν : [('SLL', 7), ('LLL', 2)]}
        """
        if self._quantified:
            return self._quantified
        else:
            quantified_dict = {}
            for key in self.raw.keys():
                new_entry = {}
                for scansion in self.raw[key]:
                    if scansion in new_entry:
                        new_entry[scansion] += 1
                    else:
                        new_entry[scansion] = 1
                new_entry = list(new_entry.items())
                new_entry.sort(key=itemgetter(1))
                quantified_dict[key] = new_entry
            self._quantified = quantified_dict
            return quantified_dict

    @property
    def consolidated (self):
        """Combines the possible scansions for each entry into a single entry.
        Syllables which are long or unknown in all instances are marked 'L';
        those which are short or unknown in all instances are marked 'S', and
        those which are unknown in all instances or have conflicting scansions
        are marked 'X'.
        
        This is the main dictionary for use, and is accessed by key indexing of
        the Scansion_Dict object.
        
        Note: In a future implementation, it coould be useful to screen for extreme
        outliers in the prosody list, for example if 'ἐπί' is somehow once scanned
        as 'SL' instead of 'SS'.  Currently, this would consolidate to 'SX', even
        if it is a clear error/exception.
        """
        if self._consolidated:
            return self._consolidated
        else:
            consolidated_dict = {}
            for key in self.quantified.keys():
                old_entry = [scansion for scansion, count in self.quantified[key]]
                if len(old_entry) == 1:
                    new_entry = old_entry[0]
                else:
                    new_entry = combine_scansions(old_entry)
                consolidated_dict[key] = new_entry
            self._consolidated = consolidated_dict
            return consolidated_dict
        
#    @property
#    def macron_entries (self):
#        """Creates an additional dictionary, in which each word is paired with
#        a macronized version of itself.  Macrons are placed on ambiguous vowels.
#        """
#        if hasattr(self, '_macron_entries'):
#            return self._macron_entries
#        else:
#            self.consolidate()
#            macronized = {}
#            for word in self.keys():
#                scansion = self[word]
#                for syl in zip(get_syllables(word), scansion):
#                    pass
    
    def pickle (self, file_name, directory='.//Pickled/'):
        """Pickles the raw dictionary (self.raw) to the default folder, unless
        another directory is specified.  This raw dictionary can be loaded much
        more quickly (using Load_Dictionary) rather than rebuilding from the
        source texts every time.
        """
        export_file = directory + file_name + '.pkl'
        with open(export_file, 'wb+') as f:
            pickle.dump(self.raw, f)
        print('Pickled dictionary saved as {}'.format(export_file))
            
    def mark_length (self, text, lunate=False):
        """The Scansion_Dict object can be used to mark ambiguous vowels (α, ι, υ) 
        in a string of Greek text, whenever a given form is found in the dictionary.
        Length is marked with a unicode breve or macron (combining diacriticals).
        
        NOTE: Unicode length markers displace other combining diacriticals 
        (accents, breathing marks and diaereses) so they are separate characters 
        in the string. This is taken into account in my greek_prosody module, 
        but may cause problems elsewhere. For example len() will count these as 
        additional characters.  Only a few fonts will present all diacriticals
        over a single character.
        """
        
        text = normalize_sigmas(text, lunate=self.lunate)
        new_text = ''
        for chunk in lossless_split(text):
            #print("CHUNK: '{}'".format(chunk))
            word = just_word(chunk)
            #print("WORD: '{}'".format(word))
            if word in self.consolidated:
                marked = add_length_markers(word, self.consolidated[word])
                new_text += chunk.replace(word, marked)
            else:
                new_text += chunk
            #print("New Text: '{}'".format(new_text))
        if lunate:
            new_text = normalize_sigmas(new_text, lunate=True)
        return new_text
    
#%%
      
#############################################
#DEAL WITH THE CORPUS OF TEXTS
#############################################
        
from os import listdir

PLAY_DIRECTORY = 'C:/Users/Anna/Anaconda3/SongDatabase/Corpus/clean_OCTs/'
# THIS MUST BE CHANGED TO MATCH THE LOCATION OF YOUR TEXT FILES

def _get_text_list (meter='trimeter', encoding='utf-8-sig'):
    """Loads all the texts for a certain meter and returns a list of strings, 
    each containing the whole text of wach file.  Further texts can be added as
    TXT files in the TEXT directory subfolder for the given meter.
    
    NOTE: Because my text files were created using WIndows Notepad, they are encoded
    as 'utf-8-sig'. If more texts are added from another machine, everything should
    be standardized as 'utf-8', and the default switched accordingly.
    
    :param str meter: Now, only 'trimeter' is supported. (Next will be 'hexameter')
    :return list text_list: a list of strings containing the full text of each
                            file in the given directory.
    """
    if meter == 'trimeter':
        directory = PLAY_DIRECTORY
    #elif meter is 'hexameter':
    #    directory = EPIC_DIRECTORY
    else:
        raise ValueError("Requested meter ('{}') is not available".format(meter))
        
    file_list = listdir(directory)
    text_list = []
    for f in file_list:
        with open(directory + f, encoding=encoding) as file:
            text = file.read()
            text = normalize(text)
        text_list.append(text)
    return text_list

def pickle_texts (meter='trimeter', directory='.//Pickled/', encoding='utf-8-sig'):
    """Loads the full text list for the specified meter using get_text_list, 
    and then pickles that list for future use.  It also returns the text list
    for current use.  See note on get_text_list regarding encoding.
    
    NOTE: This function should be run everytime new texts are added to the Texts
    folder, so that those texts are added to the pickled repository accessed by
    other functions.
    """
    
    text_list = _get_text_list(meter=meter, encoding=encoding)
    export_file = directory + 'text_list_' + meter + '.pkl'
    with open(export_file, 'wb+') as f:
        pickle.dump(text_list, f)
    print('Pickled texts saved as {}'.format(export_file))
    return text_list
    
def Load_Texts (meter='trimeter', directory='.//Pickled/'):
    """Loads the full text list.  If a pickled version is available, that is
    preferred, but if it is not, then the text list is created, pickled, and 
    returned.
    """
    file_name = 'text_list_' + meter + '.pkl'
    try:
        with open(directory + file_name, 'rb') as f:
            text_list = pickle.load(f)
    except FileNotFoundError:
        print()
        print('Pickled text_list not available. Building text_list...')
        print()
        text_list = pickle_texts(meter=meter, directory=directory)
    return text_list

def find_instances (string, context=30, meter='trimeter', full_word=False):
    """Searches for the input string in all the texts for a given meter.
    Especially useful for troubleshooting prosody of specific entries.
    The return is a list of string Messages giving the text number and the match
    in context.
    
    If full_word flag is set, the string must have wordbreaks at the start and
    end.  This is useful for finding short words that might also appear within
    larger words.
    
    :param str string: Greek text to match
    :param int context: number of characters of context in each direction
    :param str meter: currently only trimeter available
    :return list instances: a list of string messages with text # and context.
    """
    MESSAGE = """
    Text #{}:
    {}"""
    string = normalize_sigmas(string, lunate=True)
    if full_word:
        regex = re.compile(r'/b'+ string + r'/b')
    else:
        regex = re.compile(string)
    try:
        text_list = Load_Texts(meter=meter)
    except ValueError:
        print("Meter ({}) not available".format(meter))
    
    instances = []
    for i, text in enumerate(text_list):
        for m in regex.finditer(text):
            instances.append(MESSAGE.format(
                    i, text[int(m.start()) - context : int(m.end()) + context]))
    return instances

def Simple_Dictionary (lunate=False):
    """This function is mostly for testing. It creates a Scansion_Dict instance
    and adds the full text list once."""
    
    tri_text_list = Load_Texts(meter='trimeter')    
#    hex_text_list = get_text_list(meter='hexameter)
    simple_dict = Scansion_Dict(lunate=lunate)
    for i, t in enumerate(tri_text_list):
        simple_dict.add_text(t)
    if lunate:
        export_name = 'simple_dict_lunate'
    else:
        export_name = 'simple_dict'
    simple_dict.pickle(export_name)
    return simple_dict        
      
def Build_Dictionary (lunate=False, test_mode=False):
    """Creates the most authoritative scansion dictionary possible based on the 
    available texts. The Scansion_Dict object is returned, and is also pickled 
    for future use. This function should be called to rebuild the stored 
    dictionary whenever there are updates to the Texts or the processing.
    
    A lengthy (~5 min?) recursive method is employed, by which more data can be
    extracted from the source texts.  Each time a dictionary is built from the
    texts, it is stored and used to mark the length of ambiguous vowels in texts
    before the next pass.  This allows the scansion algorithms to successfully
    scan more lines than in the previous pass, adding more prosodies to the
    dictionary than before.  The process ends when no further progress is made 
    (OR when six passes have been made without success).
    
    If six passes are made without reaching equilibrium, both the previous and
    the current dictionary are returned, to help with troubleshooting.
    
    If the test_mode flag is set, then the dictionary is built using only a
    short excerpt from the Agamemnon (see below).
    """
    if test_mode:
        tri_text_list = TEST_TEXT
    else:
        tri_text_list = Load_Texts(meter='trimeter')    
#       hex_text_list = load_texts(meter='hexameter)  (SOMEDAY)
    current_dict = Scansion_Dict(lunate=lunate)
    finished = False
    counter = 1
    while not finished:
        print()
        print('PASS ({}) ...'.format(counter))
        new_dict = Scansion_Dict(lunate=lunate)
        for i, t in enumerate(tri_text_list):
            print('  Adding text {}'.format(i+1))
            text = current_dict.mark_length(t)
            new_dict.add_text(text)
#        for t in hex_text_list:
#            Dictionary.add_text(t, meter='hexameter')
        print('TOTAL KEYS: {}'.format(len(new_dict.consolidated)))
        
#        For examining issues with particular words:
#        if counter > 1:
#            print('CURRENT: {}'.format(current_dict.consolidated['ἐν']))
#        print('NEW: {}'.format(new_dict.consolidated['ἐν']))
        
        #Check for completion (i.e. pass without changes):
        if counter > 3:
            all_match = True
            for key in new_dict.consolidated.keys():
                try:
                    other = current_dict.consolidated[key]
                except KeyError:
                    other = None
                if new_dict.consolidated[key] != other:
                    all_match = False
                    break
            if all_match:
                finished=True
        
        #Check if more than five passes have been made
        if not finished and counter > 5:
            print()
            print('Dictionary could not be completed. (Old, New) dicts have been returned.')
            print()
            return current_dict, new_dict
        
        #Otherwise, update the 'current' dict and start another pass
        else:
            current_dict = new_dict
            counter += 1
            
    if lunate:
        export_name = 'scansion_dict_lunate'
    else:
        export_name = 'scansion_dict'
    new_dict.pickle(export_name)
    return new_dict        

TEST_TEXT = ["""
add. M sub titulo Ἀγαμέμνων ante prologum
ΑΓΑΜΕΜΝΩΝ
ΦΥΛΑΞ θεοὺϲ μὲν αἰτῶ τῶνδʼ ἀπαλλαγὴν πόνων,
φρουρᾶϲ ἐτείαϲ μῆκοϲ, ἣν κοιμώμενοϲ
ϲτέγαιϲ Ἀτρειδῶν ἄγκαθεν, κυνὸϲ δίκην,
ἄϲτρων κάτοιδα νυκτέρων ὁμήγυριν
καὶ τοὺϲ φέρονταϲ χεῖμα καὶ θέροϲ βροτοῖϲ
λαμπροὺϲ δυνάϲταϲ, ἐμπρέπονταϲ αἰθέρι
ἀϲτέραϲ, ὅταν φθίνωϲιν ἀντολαῖϲ τε τῶν·
καὶ νῦν φυλάϲϲω λαμπάδοϲ τὸ ϲύμβολον,
αὐγὴν πυρὸϲ φέρουϲαν ἐκ Τροίαϲ φάτιν
ἁλώϲιμόν τε βάξιν· ὧδε γὰρ κρατεῖ
γυναικὸϲ ἀνδρόβουλον ἐλπίζον κέαρ·
εὖτʼ ἂν δὲ νυκτίπλαγκτον ἔνδροϲόν τʼ ἔχω
εὐνὴν ὀνείροιϲ οὐκ ἐπιϲκοπουμένην
ἐμήν· φόβοϲ γὰρ ἀνθʼ ὕπνου παραϲτατεῖ,
τὸ μὴ βεβαίωϲ βλέφαρα ϲυμβαλεῖν ὕπνωι·
ὅταν δʼ ἀείδειν ἢ μινύρεϲθαι δοκῶ,
ὕπνου τόδʼ ἀντίμολπον ἐντέμνων ἄκοϲ,
κλαίω τότʼ οἴκου τοῦδε ϲυμφορὰν ϲτένων
οὐχ ὡϲ τὰ πρόϲθʼ ἄριϲτα διαπονουμένου.
νῦν δʼ εὐτυχὴϲ γένοιτʼ ἀπαλλαγὴ πόνων
εὐαγγέλου φανέντοϲ ὀρφναίου πυρόϲ.
ὦ χαῖρε λαμπτὴρ νυκτόϲ, ἡμερήϲιον
φάοϲ πιφαύϲκων καὶ χορῶν κατάϲταϲιν
πολλῶν ἐν Ἄργει τῆϲδε ϲυμφορᾶϲ χάριν.

ἰοὺ ἰού·
Ἀγαμέμνονοϲ γυναικὶ ϲημαίνω τορῶϲ"""]

def Load_Dictionary (lunate=False, simple=False):
    """Loads the pickled scansion dictionary with the required specifications.
    If no such dictionary is found, one is built and pickled for future use.
    This is the function that should be called by other programs, to avoid long
    waits rebuilding the dictionary.
    
    """
    directory='.//Pickled/'
    # Identify dictionary file name:
    if simple:
        file_name = 'simple_dict'
    else:
        file_name = 'scansion_dict'
    if lunate:
        file_name += '_lunate'
    file_name += '.pkl'
    # Attempt to unpickle specified dictionary:
    try:
        NewDict = Scansion_Dict()
        with open(directory + file_name, 'rb') as f:
            NewDict.raw = pickle.load(f)
    except FileNotFoundError:
        print('Pickled dictionary not available. Building dictionary...')
        NewDict = Build_Dictionary()
    return NewDict
        
