# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 16:55:14 2018

@author: Anna
"""
import re
from class_syllable import Syllable
from greek_prosody import get_syllables, count_syllables

CORRUPTION_REGEX = re.compile(r'†|\$|⟨\s+⟩')

def is_corrupt(text):
    """Checks whether a string contains markers of corruption. A line is 
    considered corrupt if it contains any obelized text or a lacuna. 
    Editor supplements in brackets are accepted as part of the text.
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
            raw_syllables = get_syllables(self.text, resolutions=True)
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
        return count_syllables(self.text)
    
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