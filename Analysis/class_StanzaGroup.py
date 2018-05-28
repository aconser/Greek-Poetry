# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:06:07 2018

@author: Anna
CLASS StanzaGroup
"""
import Greek_Prosody.prosody as GP
import class_syllable as CS


class StanzaGroup:
    """Contains, compares, and displays the data for two or more stanzas which 
    metrically respond to one another."""  
    
    def __init__ (self, name, stanza_list):
        self.name = name
        self.stanzas = stanza_list
        self.count = len(self.stanzas)
        
        #Check for sufficient stanzas
        assert self.count > 1, \
        'Two few stanzas for a StanzaGroup (see {})'.format(stanza_list[0].name)
        
        #Name strophe and antistrophe for easy access
        self.strophe = self.stanzas[0]
        self.antistrophe = self.stanzas[1]
        
        #Check for responsion
        first_syl_count = self.strophe.syl_count
        for s in self.stanzas:
            assert s.syl_count == first_syl_count, \
            'Responsion issue in {}'.format(self.name)
            
        self._syllables = []
        self._corrupt_list = []
        self._contours = []
        self._raw_contours = []
        self._meter = []
        self._repeat_count = None
        self._match_count = None
        self._syl_tags = []
        
    @property
    def raw_syl_count (self):
        return self.strophe.syl_count
    
    @property
    def corrupt (self):
        for s in self.stanzas:
            if s.corrupt:
                return True
        else:
            return False
            
    @property
    def line_count (self):
        return self.strophe.line_count

    @property
    def syllables (self):
        """Combines the syllables from all stanzas into a single list of Syllable
        objects.
        """
        if self._syllables:
            return self._syllables
        syllables = []
        for syl_group in zip(*[s.syllables for s in self.stanzas]):
            syllables.append(CS.combine_syls(syl_group))
        self._syllables = syllables
        return syllables
    

    @property
    def meter (self):
        """Merges the meter data for responding stanzas, to fill in unknown 
        quantities wherever possible. If the stanzas disagree on the quantity of
        a given position, it is marked as anceps ('ANC').
        """
        if self._meter:
            return self._meter
        merged_meter = GP.combine_scansions([s.meter for s in self.stanzas], metrical_symbols=True)
        self._meter = merged_meter
        return merged_meter
            
    @meter.setter
    def meter (self, meter_list):
        self._meter = meter_list
        
    @property
    def pretty_meter (self):
        scansion_dict = {'X'  : '⏒',
                         'R'  : '⏔',
                         'ANC': '⏒',
                         'L' : '–',
                         'S' : '⏑',
                         }
        pretty_meter = [scansion_dict[m] for m in self.meter]
        return pretty_meter
    
    @property
    def raw_contours (self):
        """Merges the contour data for responding stanzas, and returns a list
        of melodic contours.  This presumes that the melody was repeated 
        identically but also followed the contours of the word accentuation in 
        all reponding stanzas.
        """
        if self._raw_contours:
            return self._raw_contours
        contours = []
        for position in zip(*[s.contours for s in self.stanzas]):
            if all(p == 'N' for p in position):
                contours.append('N')
            elif 'UP-G' in position:
                if 'DN' in position or 'DN-A' in position:
                    contours.append('=')
                else:
                    contours.append('UP-G')
            elif 'UP' in position:
                if 'DN' in position or 'DN-A' in position:
                    contours.append('=')
                else:
                    contours.append('UP')
            elif all(p == 'DN-A' for p in position):
                contours.append('DN-A')
            else:
                contours.append('DN')
        self._raw_contours = contours
        return contours
    
    @property
    def contours (self):
        """Contours with corrupt syllables marked as 'X'
        """
        if self._contours:
            return self._contours
        new_contours = []
        for i, c in enumerate (self.raw_contours):
            if self.corrupt_list[i]:
                c = 'X'
            new_contours.append(c)
        self._contours = new_contours
        return new_contours
    
    @property
    def pretty_contours (self):
        """Contours as needed for display / composition. Melodic movement is 
        indicated by arrows. Corrupt syllables are included.
        """
        
        arrow_dict = {'N' : 'x',
                      '=' : '=',
                      'UP-G' : '≤',
                      'UP' : '↗',
                      'DN-A' : '⇘',
                      'DN' : '↘',
                     }
                       #Other arrow options I could sub in: '→', '⇗'
        pretty_contours = [arrow_dict[c] for c in self.raw_contours]
        return pretty_contours
        
    @property
    def corrupt_list (self):
        if self._corrupt_list:
            return self._corrupt_list
        corrupt_list = []
        for i in range(self.raw_syl_count):
            corrupt = False
            if self.strophe.syllables[i].corrupt:
                corrupt = True
            elif self.antistrophe.syllables[i].corrupt:
                corrupt = True
            corrupt_list.append(corrupt)
        self._corrupt_list = corrupt_list
        return corrupt_list
    
    @property
    def corrupt_count (self):
        return self.corrupt_list.count(True)
    
    @property
    def syl_count (self):
        return (self.raw_syl_count - self.corrupt_count)
    
    def add_stats (self):
        """NOTE THIS IS ONLY FOR PAIRS, and won't work for Pindar, etc."""
        strong_match = 0    # All contours are 'DN-A'
        mid_match = 0       # All contours are 'DN-A' or 'DN'
        match = 0           # All contours are 'UP' or all are 'DN'
        strong_conflict = 0 # Position contains 'DN-A' and 'UP' or '='
        mid_conflict = 0    # Position contains 'UP' and 'DN'
        weak_conflict = 0   # Position contains '=' and 'UP or 'DN'
        non_conflict = 0    # All other combinations (weak match, since compatible)
        stat_list = []
        for i, position in enumerate( zip(*[s.contours for s in self.stanzas])):
            #Check for corruption:
            if self.corrupt_list[i]:
                stat_list.append('X')
                continue
            #Check for matches:
            if all(p == 'DN-A' for p in position):
                strong_match += 1
                stat_list.append('M-1')
            elif all(p in ['DN-A', 'DN'] for p in position):
                mid_match += 1
                stat_list.append('M-2')
            elif all(p in ['UP', 'UP-G'] for p in position):
                match += 1
                stat_list.append('M-3')
            elif all(p == 'DN' for p in position):
                match += 1
                stat_list.append('M-3')
            elif 'N' in position:
                non_conflict += 1
                stat_list.append('M-4')
            else:
                #Check for and sort conflicts:
                if 'DN-A' in position:
                    strong_conflict += 1
                    stat_list.append('Con-1')
                elif 'UP' in position:
                    mid_conflict += 1
                    stat_list.append('Con-2')
                elif 'UP-G' in position:
                    weak_conflict += 1
                    stat_list.append('Con-3')
                else:
                    assert False, 'Missing Stat Category for {}'.format(self.name)
        self.M1 = strong_match
        self.M2 = mid_match
        self.M3 = match
        self.C2 = mid_conflict
        self.C1 = strong_conflict
        self.C3 = weak_conflict
        self.M4 = non_conflict
        self.stat_list = stat_list
        

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
        self.add_stats()
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
    
    @property 
    def repeat_percentage (self):
        return (self.repeat_count / self.syl_count)
    
    @property
    def match_count (self):
        if self._match_count:
            return self._match_count
        else:
            self.add_stats()
            self._match_count = self.M1
            return self._match_count
        
    @property
    def match_percentage (self):
        return (self.match_count / self.syl_count)
    
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