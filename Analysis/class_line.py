# -*- coding: utf-8 -*-
"""
CLASS LINE

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""
import re
from .class_syllable import Syllable
import Greek_Prosody.syllables as SYLLABLES

CORRUPTION_REGEX = re.compile(r'†|\$|⟨\s+⟩|@') # More acurately "EXCLUSION_REGEX"

def is_corrupt (text):
    """Checks whether a string contains markers of corruption OR is to be 
    excluded on other grounds. A line is considered corrupt if it contains 
    any obelized text or a lacuna. Editor supplements in brackets are accepted 
    as part of the text.
    I have marked lines to be excluded on other grounds with '@'. This includes 
    lines of trimeter (where they are included as well as lines that are 
    precisely repeated between strophe and antistrophe.
    :param text str:
    :rtype: bool
    """
    return bool(CORRUPTION_REGEX.search(text))

##################################
        
class Line ():
    """A Line Object, which stores the data for a line within a stanza.
    """
    def __init__ (self, line_number, text):
        self.number = line_number
        self.text = text
        self.tags = []
        self._syllables = None
        
    def __repr__ (self):
        return """Line {}:\n{}""".format(self.number, self.text)
    
    @property
    def corrupt (self):
        """Checks whether a line is corrupt, using the is_corrupt() method."""
        return is_corrupt(self.text)
    
    @property
    def syllables (self):
        """Breaks the line into syllables and returns a list of Syllable objects, 
        each of which inherit the line data."""
        if self._syllables:
            return self._syllables
        else:
            raw_syllables = SYLLABLES.get_syllables(self.text, resolutions=True)
            syllables = [Syllable(i, s) for i, s in enumerate(raw_syllables)]
            for s in syllables:
                s.line_number = self.number
                s.line_tags = self.tags
                s.corrupt = self.corrupt
            return syllables
    
    @syllables.setter
    def syllables (self, syl_list):
        self._syllables = syl_list
    
    @property
    def syl_count (self):
        return len(self.syllables)
    
    @property
    def display_data (self):
        numbers = []
        texts = []
        contours = []
        meters = []
        tags = []
        for s in self.syllables:
            numbers.append(str(s.number))
            texts.append(s.text)
            contours.append(s.contour)
            meters.append(s.prosody)
            tags.append('/'.join(s.all_tags))
        data = (numbers, texts, contours, meters, tags)
        return data
    
    def display (self):
        for row in self.display_data:
            print(''.join(['{:<6}'.format(item) for item in row]))
            
class LineGroup ():
    def __init__ (self, line_list, syl_list):
        self.lines = line_list
        self.texts = [l.text for l in self.lines]
        self.syllables = syl_list
        self.corrupt = any(l.corrupt for l in self.lines)
        self.syl_count = len(self.syllables)
        self.all_tags = [s.all_tags for s in self.syllables]
        self.meter = [s.prosody for s in self.syllables]
        self.match_statuses = [s.match_status for s in self.syllables]
        self.contours = [s.contour for s in self.syllables]
        self.pretty_contours = [s.pretty_contour for s in self.syllables]
    
    @property    
    def stats (self):
        percent_match = self.match_statuses.count('M1')/self.syl_count
        percent_repeat = self.contours.count('=')/self.syl_count
        return (percent_match, percent_repeat)
        
        