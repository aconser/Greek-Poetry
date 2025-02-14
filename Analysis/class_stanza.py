# -*- coding: utf-8 -*-
"""
CLASS STANZA

This class represents and analyzes data for a single song stanza from Greek tragedy.

Next steps for improvement:
    1. Clean up the total vs. corrupt distinctions.

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""
#%%
import re
import Greek_Prosody.syllables as SYLLABLES
import Greek_Prosody.prosody as PROSODY
#from accents import get_accent_index
from .class_word import Word
from .class_line import Line
from .class_syllable import Syllable
#from cltk.tag.pos import POSTag

class Stanza ():
    """A Stanza Object, which stores the data for a set of responding stanzas.
    """
    def __init__ (self, name, raw_text, start_line=1, author='Author Name'):
        self.name = name
        self.author = author
        self.raw_text = raw_text
        self.start_line = start_line
        self.scansion = []
        self.tags = []
        self._words = []
        self._syllables = []
        self._meter = []
        self._contours = []
        self._lines = []
        self._corrupt = None
        
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
        if not self._words:
            raw_words = self.clean_text.split()
            # POS Tagging - can't yet get CLTK tagger to work.
#            tagger = POSTag('greek')
#            pos_list = tagger.tag_tnt(self.clean_text)
#            assert len(raw_words = len(pos_list), 'Word count not same as POS count'
#            return [Word(w, POS=p) for w, p in zip(raw_words, pos_list)]
            for i, w in enumerate(raw_words):
                word = Word(w)
                word.number = i
                self._words.append(word)
        return self._words

    @property
    def meter (self):
        """If meter has been manually added, returns that.  Otherwise, combines 
        the metrical data that can be extracted from the texts.
        """
        if not self._meter:
            self._meter = PROSODY.get_prosody(self.clean_text)
        return self._meter
        
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
            #Check for word-end in middle of resolved syllable
            if (s.contains_resolution and ' ' in s.text):
                pre_accent = True
            #Check for ENCLITICS (excluding τοῦ), and correct previous syllable
            if 'enclitic' in s.word_tags and not 'proclitic' in s.word_tags:
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
        raw_syllables = SYLLABLES.get_syllables(self.clean_text, resolutions=True)
        syllables = [Syllable(i, s) for i, s in enumerate(raw_syllables)]
        # Assemble data about the containing word for each syllable
        word_data_list = []
        for w in self.words:
            data = (w.text, w.number, w.lemma, w.POS, w.tags)
            # If two words are joined by a resolution, the data of the SECOND word
            # is retroactively assigned to that resolved syllable, but the tags
            # of both are combined.
            if w.initial_resolution:
                previous_tags = word_data_list[-1][-1]
                combined_tags = w.tags + previous_tags
                combined_data = data[:-1] + (combined_tags,)
                word_data_list = word_data_list[:-1]
                word_data_list.append(combined_data)
            word_data_list.extend([data] * w.syl_count)
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
            s.meter = self.meter[i] #[ADDED FOR CONVENIENCE]
            s.word, s.word_number, s.lemma, s.POS, s.word_tags = word_data_list[i]
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
        if not self._corrupt:
            self._corrupt = any(l.corrupt for l in self.lines)
        return self._corrupt
    
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
    
    @property
    def accents (self):
        return [s.accent for s in self.syllables]
    
    @property
    def total_circ_count (self):
        """Counts the number of circumflex syllables in a stanza.  Note that
        this does NOT take into account corruption, so percentages should be 
        calculated using total_syl_count (not secure)."""
        
        return self.accents.count('C')
        
    @property
    def secure_circ_count (self):
        count = 0
        for s in self.syllables:
            if s.corrupt==False and s.accent=='C':
                count = count + 1
        return count
    
    @property
    def total_peak_count (self, enclitics=False):
        """ Counts the number of accentual peaks in a stanza, a.k.a.
        acutes and circumflexes (excluding second, pre-enclitic acutes)"""
        
        if enclitics:
            return (self.accents.count('A') + self.accents.count('C'))
        else:
            return self.contours.count('DN-A')
    
    @property
    def secure_peak_count (self, enclitics=False):
        count = 0
        if enclitics:
            for s in self.syllables:
                if s.corrupt==False and s.accent in ['C', 'A']:
                    count = count + 1
        else:
            for s in self.syllables:
                if s.corrupt==False and s.contour=='DN-A':
                    count = count + 1
               #  elif s.corrupt==False and s.accent=='C':
               #    count = count + 1
        return count
    

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

