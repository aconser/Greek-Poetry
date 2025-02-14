# -*- coding: utf-8 -*-
"""
CLASS TAG ANALYSIS

--probably obsolete with improved word analysis in stanza_group--

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""

class Tag_Analysis:
    def __init__ (self, pair, tag):
        self.pair = pair
        self.tag = tag
        self.syllables = [s for s in self.pair.syllables if tag in s.all_tags]
        self.secure_syllables = [s for s in self.syllables if not s.corrupt]
        self.total_syl_count = len(self.syllables)
        self.secure_syl_count = len(self.secure_syllables)
        
    @property
    def words (self):
        if not self._words:
            all_words = [(s.word, s.corrupt, s.word_number) for s in self.syllables]
            unique_words = set(all_words)
            ordered_words = sorted(unique_words, key=lambda tup: tup[2])
            self._words = [(w, c) for w, c, _ in ordered_words]
        return self._words
    
    def match_count (self, wcorrupt=False):
        if wcorrupt:
            return len([s for s in self.syllables if s.is_match()])
        else:
            return len([s for s in self.secure_syllables if s.is_match()])
        
    def percentage_match (self, wcorrupt=False):
        if wcorrupt:
            return self.match_count(wcorrupt=True) / self.total_syl_count
        else:
            return self.match_count() / self.secure_syl_count
        
    def repeat_count (self, wcorrupt=False):
        if wcorrupt:
            return len([s for s in self.syllables if s.is_repeat()])
        else:
            return len([s for s in self.secure_syllables if s.is_repeat])
        
    def percentage_repeat (self, wcorrupt=False):
        if wcorrupt:
            return self.repeat_count(wcorrupt=True) / self.total_syl_count
        else:
            return self.repeat_count() / self.secure_syl_count
        
    def display (self, wcorrupt=False):
        print("Analysis of tag '{}' in Pair '{}'".format(self.tag, self.pair.name))
        if wcorrupt:
            print('(Including corrupt syllables)')
            print()
            print('Number of syllables: {}'.format(self.syl_count))
        else:
            print('(Excluding corrupt syllables)')
            print()
            print('Number of syllables: {}'.format(self.secure_syl_count))
        print('Percentage Match:  {}'.format(self.percentage_match(wcorrupt=wcorrupt)))
        print('Percentage Repeat: {}'.format(self.percentage_repeat(wcorrupt=wcorrupt)))
        print()
        
    def display_words (self):
        pass
#%%

def Analyze_tags (Author="all"):
    """Runs the about study on a group of texts and compiles data"""
    pass