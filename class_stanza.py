# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 15:08:07 2018

@author: Anna

Class Stanza
"""
#%%
import re
#from contonations import contonations
from greek_prosody import get_syllables, count_syllables, scan_line
#from accents import get_accent_index
from class_word import Word
from class_line import Line
from class_syllable import Syllable
#from cltk.tag.pos import POSTag

class Stanza ():
    """A Stanza Object, which stores the data for a set of responding stanzas.
    """
    def __init__ (self, name, raw_text, start_line=0):
        self.name = name
        self.raw_text = raw_text
        self.start_line = start_line
        self.scansion = 0
        self.tags = []
        self._syllables = []
        self._contours = []
        self._lines = []
        
    def __repr__ (self):
        return '{}: {} '.format(self.name, self.raw_text)

    @property
    def clean_text (self):
        """Returns the stanzas each as a single string of text
        without tabs or linebreaks. Hyphenated words are re-joined."""
        CLEANING_LIST = [(u'\xa0', ' '),   #replace special tab characters with spaces
            (r'[-–]\n\s*', ''),  #join words broken across lines by hyphens or dashes
            (r'^\s+', ''),    #remove extra whitespace at start
          # (r'\n\s+', '\n'), #remove extra whitespace at start of lines
            (r'\n', ' '),     #replace all linebreaks with spaces
            (r'\s\s+', ' ')   #replace multiple spaces with a single space
            ]
        text = self.raw_text
        for old, new in CLEANING_LIST:
            text = re.sub(old, new, text)
        return text
    
    @property
    def words (self):
        """The stanza broken into words, each of which are turned into a Word
        object, which extracts data about the word and applies automatic tagging.
        """
        raw_words = self.clean_text.split()
        # POS Tagging - can't yet get CLTK tagger to work.
#        tagger = POSTag('greek')
#        pos_list = tagger.tag_tnt(self.clean_text)
#        assert len(raw_words = len(pos_list), 'Word count not same as POS count'
#        return [Word(w, pos=p) for w, p in zip(raw_words, pos_list)]
        return [Word(w) for w in raw_words]
    
#    @property
#    def contonations (self):
#        """Returns a list of accentual groups, roughly equivalent to the prosodic
#        'appositive groups' outlined in Devine and Stephens (1994: 285-375).
#        Proclitics (including articles and prepositions) and enclitics are attached
#        to their host words.  These units would form a single accentual arc.
#        """
#        return contonations(self.clean_text)

    @property
    def meter (self):
        """If meter has been manually added, returns that.  Otherwise, combines 
        the metrical data that can be extracted from the texts.
        """
        if self.scansion != 0:
            return self.meter
        else:
            return scan_line(self.clean_text)
        
    @property
    def raw_lines (self):
        """Returns a list of line objects."""
        raw_lines = self.raw_text.split('\n')
        return [Line(i+self.start_line, l.strip()) for i, l in enumerate(raw_lines)]
    
    @property
    def line_count (self):
        return len(self.raw_lines)
    
    def _get_contours (self, syl_list):
        """Iterates through a list of Syllables objects and creates a list of 
        melodic contours."""
        contours = []
        pre_accent = True
        last_contour = ''
        for s in syl_list:
            contour = ''
            #Check for ENCLITICS, and correct previous syllable
            if 'enclitic' in s.word_tags:
                if contours[-1] == 'N':
                    contours[-1] = last_contour
                    pre_accent = False
            #MAIN ACCENT followed by characteristic fall
            if s.accent in ['A', 'C']:
                if pre_accent:
                    contour = 'DN-A'
                    pre_accent = False
                else:               #unless a second accent caused by an enclitic
                    contour = 'DN'
            #BEFORE ACCENT, the melody rises
            elif pre_accent:
                contour = 'UP'
            #AFTER ACCENT, the melody falls
            elif not pre_accent:
                contour = 'DN' 
            #WORD END can be followed by any note
            if s.word_end:
                last_contour = contour   #copy contour in case of subsequent enclitic
                contour = 'N'
                pre_accent = True
            #Except PROCLITICS and GRAVES followed by a very small rise or a repetition
            if 'proclitic' in s.word_tags:
                contour = 'UP-G'
            elif s.accent == 'G':
                contour = 'UP-G'
                
            contours.append(contour)
 
        return contours

    @property
    def syllables (self):
        """Extracts the syllables from the raw_lines, and adds additional data
        about the stanza, the syllable's position within an accentual arc (here
        called contonation) stanza-level data 
        to each."""
        if self._syllables:
            return self._syllables
        raw_syllables = get_syllables(self.clean_text, resolutions=True)
        syllables = [Syllable(i, s) for i, s in enumerate(raw_syllables)]
        # Assemble data about the containing word for each syllable
        word_data_list = []
        for w in self.words:
            data = (w.text, w.lemma, w.POS, w.tags)
            word_data_list.extend([data] * count_syllables(w.text))
        # Assemble data about the containing line for each syllable
        line_data_list = []
        for l in self.raw_lines:
            data = (l.number, l.corrupt, l.tags)
            line_data_list.extend([data]*l.syl_count)
        # Update each syllable with word, line and stanza data
        for i, s in enumerate(syllables):
            s.number = i
            s.stanza = self.name
            s.stanza_tags = self.tags
            s.prosody = self.meter[i]
            s.word, s.lemma, s.POS, s.word_tags = word_data_list[i]
            s.line_number, s.corrupt, s.line_tags = line_data_list[i]
        # Assemble and add contour data
        contours = self._get_contours(syllables)
        for i, s in enumerate(syllables):
            s.contour = contours[i]
        self._syllables = syllables
        return syllables

    @property
    def syl_count (self):
        return len(self.syllables)
    
    @property
    def corrupt (self):
        for l in self.lines:
            if l.corrupt:
                self.corrupt = True
                return True
        else:
            return False
    
    @property
    def lines (self):
        """Sorts the syllables back into lines."""
        if self._lines:
            return self._lines
        nested_syllables = []
        current_line = []
        current_line_number = self.syllables[0].line_number
        for s in self.syllables:
            if s.line_number == current_line_number:
                current_line.append(s)
            else:
                nested_syllables.append(current_line)
                current_line = []
                current_line.append(s)
                current_line_number = s.line_number
        nested_syllables.append(current_line)
        lines = self.raw_lines
        for l, s in zip(lines, nested_syllables):
            l.syllables = s
        self._lines = lines
        return lines
            
    @property
    def contours (self):
        return [s.contour for s in self.syllables]
    
    def display(self):
        print()
        print (self.name)
        for l in self.lines:
            l.display()
            print ('------'* l.syl_count)

    @property                     
    def all_tags (self):
        all_tags = [t for s in self.syllables for t in s.all_tags]
        return list(set(all_tags))

