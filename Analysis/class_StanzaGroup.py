# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:06:07 2018

@author: Anna
CLASS StanzaGroup
"""
#%%

from class_syllable import SylGroup

class StanzaGroup:
    """Contains, compares, and displays the data for two or more stanzas which 
    metrically respond to one another."""  
    
    def __init__ (self, name, stanza_list):
        self.name = name
        self.stanzas = stanza_list
        self.stanza_count = len(self.stanzas)
        
        #Check for sufficient stanzas
        assert self.stanza_count > 1, \
        'Two few stanzas for a StanzaGroup (see {})'.format(stanza_list[0].name)
        
        #Name strophe and antistrophe for easy access
        self.strophe = self.stanzas[0]
        self.antistrophe = self.stanzas[1]
        
        #Check for responsion
        first_syl_count = self.strophe.syl_count
        for s in self.stanzas:
            assert s.syl_count == first_syl_count, \
            'Responsion issue in {}'.format(self.name)
        self.line_count = self.strophe.line_count
        self.corrupt = any(s.corrupt for s in self.stanzas)
        self._syllables = []
        self._secure_syls = []
        self._meter = []
        self._contours = []
        self._pretty_contours = []
        self._match_statuses = []
        self._secure_match_statuses = []
        self._repeat_count = None
        self._match_count = None
        self._syl_tags = []
        

    @property
    def syllables (self):
        """Creates a list of SylGroup objects from the responding syllables of
        all responding stanzas."""
        if self._syllables:
            return self._syllables
        position_list = zip([st.syllables for st in self.stanzas])
        combined = [SylGroup(p) for p in position_list]
        self._syllables = combined
        return combined
    
    @property
    def meter (self):
        if not self._meter:
            self._meter = [syl.prosody for syl in self.syllables]
        return self._meter
    
    @meter.setter
    def meter (self, meter_list):
        assert type(meter_list) is list, 'Meter must be a list'
        self._meter = meter_list
    
    @property
    def contours (self):
        """The merged contour data for responding stanzas. This presumes that 
        the melody was repeated identically but also followed the contours of 
        the word accentuation in all reponding stanzas.
        """
        if not self._contours:
            self._contours = [s.contour for s in self.syllables]
        return self._contours
    
    @property
    def pretty_contours (self):
        """Contours as needed for display / composition. Melodic movement is 
        indicated by arrows.
        """
        if not self._pretty_contours:
             self._pretty_contours = [s.pretty_contour for s in self.syllables]
        return self._pretty_contours
    
    @property    
    def match_statuses (self):
        if not self._match_statuses:
            self._match_statuses = [s.match_status for s in self.syllables]
        return self._match_statuses
    
    @property
    def secure_syls (self):
        """Only the syllables in lines without signs of corruption."""
        if not self._secure_syls:
            self._secure_syls = [s for s in self.syls if not s.corrupt]
        return self._secure_syls

    @property
    def secure_match_statuses (self):
        """Used for statistics purposes."""
        if not self._secure_match_statuses:
            self._secure_match_statuses = [s.match_status for s in self.secure_syls]
        return self._secure_match_statuses
    
    @property
    def secure_contours (self):
        """Used for statistics purposes."""
        if not self._secure_contours:
            self._secure_contours = [s.contour for s in self.secure_syls]
        return self._secure_contours

# SIMPLE STATISTICS
        
    @property
    def total_syl_count (self):
        return self.strophe.syl_count
    
    @property
    def secure_syl_count (self):
        return len(self.secure_syls)
    
    @property
    def corrupt_syl_count (self):
        return self.total_syl_count - self.secure_syl_count
    
    @property
    def total_match_count (self):
        """The total number of matched post-accentual falls."""
        return self.match_statuses.count('M1')
    
    @property
    def secure_match_count (self):
        """The total number of matched post-accentual falls."""
        return self.secure_match_statuses.count('M1')
    
    @property
    def total_contra_count (self):
        """The number of post-accentual falls that cannot be accomodated in 
        by conflicting contours in responding stanzas."""
        return self.match_statuses.count('C1')
    
    @property
    def secure_contra_count (self):
        """The number of post-accentual falls that cannot be accomodated in 
        by conflicting contours in responding stanzas."""
        return self._secure_match_statuses.count('C1')

    @property
    def total_repeat_count (self):
        """The number of repeated notes required by a stanza"""
        return self.contours.count('=')
    
    @property
    def secure_repeat_count (self):
        """The number of repeated notes required by a stanza"""
        return self.secure_contours.count('=')

    @property
    def total_matched_wb_count (self):
        """The number of aligned wordbreaks."""
        return self.match_statuses.count('N')
    
    @property 
    def total_repeat_percentage (self, secure=True):
        return (self.repeat_count / self.secure_syl_count)

    @property 
    def secure_repeat_percentage (self, secure=True):
        return (self.secure_repeat_count / self.secure_syl_count)

    @property
    def total_match_percentage (self, secure=True):
        return (self.match_count / self.secure_syl_count)

    @property
    def secure_match_percentage (self, secure=True):
        return (self.secure_match_count / self.secure_syl_count)
    
# DISPLAY

    def display_data_2 (self):
        """Returns a list of lines, each of which is a nested tuple containing 
        that line's attributes: 
            (syl_widths, 
            (meter, stanza_1_syls, stanza_2_syls... etc. , contours)
            )
        """
        nested_lines = []
        start = 0
        for i in range(self.line_count):
            end = start + self.strophe.lines[i].syl_count
            numbers = [str(n) for n in range(start, end)]
            meter = self.meter[start:end]
            contours = self.pretty_contours[start:end]
            syl_texts= []
            widths = []
            for s in self.syllables[start:end]
            syl_texts = list(zip(*[s.join_texts for s in self.syllables[start:end]]))
            syl_widths = 
            
            stanza_syls = []
            for st in self.stanzas:
                stanza_syls.append(
                        [s.join_text for s in st.syllables[start:end]]
                        )
            meter = self.meter[start:end]
            syl_widths = []
            for syl in self.syllables:
                width = max(len(s) for s in syl.texts)
                syl_widths.append(width)
            line_data = (syl_widths,
                         (numbers, meter) + tuple(stanza_syls) + (contours,)
                        )
            nested_lines.append(line_data)
            start = end
        return nested_lines

    def _nested_lines (self):
        """Returns a list of lines, each of which is tuple containing that 
        line's attributes 
            (syl numbers, st_syllables, an_syllables, meter, and contours) 
        as lists. e.g.
        [
        (['0', '1'...], ['st_syl0', 'st_syl1'...], ['an_syl0', 'an_syl1'...], ...),
        (['23', '24', ...], ['syl23', 'syl24',...], ...),
        ... ]
        """
        nested_lines = []
        start = 0
        for i in range(self.line_count):
            end = start + self.strophe.lines[i].syl_count
            numbers = [str(n) for n in range(start, end)]
            st_syls = [s.text for s in self.strophe.syllables[start:end]]
            an_syls = [s.text for s in self.antistrophe.syllables[start:end]]
            meter = self.meter[start:end]
            contours = self.contours[start:end]
            stats = self.stat_list[start:end]
            line_data = (numbers, st_syls, an_syls, meter, contours, stats)
            nested_lines.append(line_data)
            start = end
        return nested_lines

    def display (self):
        print()
        print(self.name)
        for l in self._nested_lines():
            for attribute in l:
                print(''.join(['{:6}'.format(a) for a in attribute]))
            print ('------'*len(l[0]))
    
    def display_data (self):
        """Returns a list of lines, each of which is a nested tuple containing 
        that line's attributes: 
            (syl_widths, 
            (meter, stanza_1_syls, stanza_2_syls... etc. , contours)
            )
        """
        nested_lines = []
        start = 0
        for i in range(self.line_count):
            end = start + self.strophe.lines[i].syl_count
            numbers = [str(n) for n in range(start, end)]
            stanza_syls = []
            for st in self.stanzas:
                stanza_syls.append(
                        [s.join_text for s in st.syllables[start:end]]
                        )
            meter = self.pretty_meter[start:end]
            contours = self.pretty_contours[start:end]
            syl_widths = []
            for syl in zip(*stanza_syls):
                width = max(len(s) for s in syl)
                syl_widths.append(width)
            line_data = (syl_widths,
                         (numbers, meter) + tuple(stanza_syls) + (contours,)
                        )
            nested_lines.append(line_data)
            start = end
        return nested_lines
        
    def display_readable (self):
        print()
        print(self.name)
        print()
        data = self.display_data()
        for (widths, attributes) in data:
            for a in attributes:
                print_items = [str(i).ljust(width) for width, i in zip(widths, a)]
                print(''.join(print_items))
            total_length = sum(widths)
            print ('-'*total_length)
    
    @property
    def repeat_count (self):
        if self._repeat_count:
            return self._repeat_count
        else:
            repeat_count = self.contours.count('=')
            self._repeat_count = repeat_count
            return repeat_count
    

    
    def print_stats (self):
        self.add_stats()
        print (self.name)
        print("""
              M1 [DN-A]          : {}
              M2 [DN-A, DN]      : {}
              M3 [DN], [UP,UP-G] : {}
              M4 (contains 'N')  : {}
              C3 DN / UP-G       : {}
              C2 DN / UP         : {}
              C1 DN-A /[UP, UP-G]: {}
              
              Repeats : {}
              Repeats/Syls : {}""".format(
              self.M1, self.M2, self.M3, self.M4, self.C3, self.C2, self.C1, 
              self.repeat_count, self.repeat_percentage)
              )
        
    @property
    def syl_tags (self):
        if self._syl_tags:
            return self._syl_tags
        syl_tags = []
        for position in zip(*[s.syllables for s in self.stanzas]):
            tags = []
            for syl in position:
                tags.extend(syl.all_tags)
            syl_tags.append(tags)
        self._syl_tags = syl_tags
        return syl_tags
            
#class Position:
#    def __init__ (self, syl_list):
#        self.syls = syl_list
#    
#    @property
#    def texts:
#        return [s.text for s in self.syls]
#    
#    @property
#    def tags:
#        return [s.alltags for s in self.syls]