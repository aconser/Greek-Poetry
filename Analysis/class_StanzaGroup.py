# -*- coding: utf-8 -*-
"""
CLASS STANZA GROUP

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""
#%%

from . import class_syllable as CS
from . import class_word as CW
from . import class_line as CL
import collections

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
            if not s.syl_count == first_syl_count:
                print ()
                print ("""Responsion issue in {}
                       
Line-by-line syllable counts [stanza 1, stanza 2, etc.]:
                       """.format(self.name))
                for line_set in zip(*[s.lines for s in self.stanzas]):
                     print([len(l.syllables) for l in line_set])
                     print()
            assert s.syl_count == first_syl_count, \
            """Responsion issue in {} -- SEE ABOVE""".format(self.name)

        self.line_count = self.strophe.line_count
        self.corrupt = any(s.corrupt for s in self.stanzas)
        self._syllables = []
        self._words = []
        self._secure_syls = []
        self._line_meters = []
        self._lines = []
        self._meter = []
        self._contours = []
        self._secure_contours = []
        self._pretty_contours = []
        self._match_statuses = []
        self._secure_match_statuses = []
        self._total_match_counter = None
        self._secure_match_counter = None
        self._total_cont_counter = None
        self._secure_cont_counter = None
        

    @property
    def syllables (self):
        """Creates a list of SylGroup objects from the responding syllables of
        all responding stanzas."""
        if not self._syllables: 
            position_list = zip(*[st.syllables for st in self.stanzas])
            combined = [CS.SylGroup(p) for p in position_list]
            if self._meter:
                with_meter = []
                for i, s in enumerate(combined):            
                    try:
                        s.meter = self.meter[i]
                    except:
                        print ("Meter index out of range in {}".format(self.name))
                    with_meter.append(s)
                self._syllables = with_meter
            else:
                self._syllables = combined
        return self._syllables
    
    @property
    def words (self):
        if not self._words:
            words = []
            for i, stanza in enumerate(self.stanzas):
                hold_syl = None
                start = 0
                for w in stanza.words:
                    end = start + w.syl_count
                    syls = self.syllables[start:end]
                    if hold_syl:
                        syls = [hold_syl] + syls
                        hold_syl = None
                    word = CW.Complex_Word(w, syls)
                    word.stanza_name = stanza.name
                    words.append(word)
                    start = end
                    # In case of word-final resolution, duplicate the syl as 
                    # the first syl of the next word.
                    if syls and '|' in syls[-1].texts[i]:
                        hold_syl = syls[-1]
            self._words = words
        return self._words
        
    @property
    def lines (self):
        if not self._lines:
            line_list = []
            current_line = []
            current = self.syllables[0].line_numbers
            for s in self.syllables:
                if s.line_numbers == current:
                    current_line.append(s)
                else:
                    line_list.append(current_line)
                    current_line = []
                    current = s.line_numbers
                    current_line.append(s)
            line_list.append(current_line)
            lines = []
            for i, l_list in enumerate(zip(*[s.lines for s in self.stanzas])):
                line = CL.LineGroup(l_list, line_list[i])
                if self._line_meters:
                    line.meter = [m for m in self._line_meters[i]]
                lines.append(line)
            self._lines = lines
        return self._lines
    
    @property
    def meter (self):
        if not self._meter:
            self._meter = [syl.prosody for syl in self.syllables]
        return self._meter
    
    @meter.setter
    def meter (self, meter_list):
        #assert type(meter_list) is list, 'Meter must be a list'
        self._meter = meter_list
        new_syl_list = []
        for i, s in enumerate(self.syllables):
            s.meter = meter_list[i]
            new_syl_list.append(s)
        self._syllables = new_syl_list
    
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
            self._secure_syls = [s for s in self.syllables if not s.corrupt]
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
    
    @property
    def all_tags (self):
        if not self._all_tags:
            self._all_tags = [s.all_tags for s in self.syllables]
        return self._all_tags

# WORD TAG ANALYSIS
        
    def tagged_words (self, tag):
        return [w for w in self.words if tag in w.word_tags]
    
    def word_tag_stats(self, tag):
        """Extracts raw match/repeat data for a given word tag.
        
        :param str tag: a word tag
        :return tuple stats: a tuple of ints (matches, repeats, total_syls)
        """ 
        tagged = self.tagged_words(tag)
        match_total = sum([w.match_count for w in tagged])
        repeat_total = sum([w.repeat_count for w in tagged])
        syl_total = sum([w.measured_syl_count for w in tagged])
        return (match_total, repeat_total, syl_total)
    
# SIMPLE STATISTICS

    #Count Syllables
    
    @property
    def total_syl_count (self):
        return self.strophe.syl_count
    
    @property
    def secure_syl_count (self):
        return len(self.secure_syls)
    
    def syl_count_DEV (self, wcorrupt=False):
        """Reminder for a future improvement, making all these doubled properties
        into single functions with a flag for whether or not to include corrupt
        syllables.
        """
        if wcorrupt:
            return self.strophe.syl_count
        else:
            return len(self.secure_syls)
    
    @property
    def corrupt_syl_count (self):
        return self.total_syl_count - self.secure_syl_count
    
    #Create Counters for match_statuses and contours
    
    @property
    def total_match_counter (self):
        if not self._total_match_counter:
            self._total_match_counter = collections.Counter(self.match_statuses)
        return self._total_match_counter
    
    @property
    def secure_match_counter (self):
        if not self._secure_match_counter:
            self._secure_match_counter = collections.Counter(self.secure_match_statuses)
        return self._secure_match_counter
    
    @property
    def total_cont_counter (self):
        if not self._total_cont_counter:
            self._total_cont_counter = collections.Counter(self.contours)
        return self._total_cont_counter

    @property
    def secure_cont_counter (self):
        if not self._secure_cont_counter:
            self._secure_cont_counter = collections.Counter(self.secure_contours)
        return self._secure_cont_counter
    
    # Counts
    
    @property
    def total_match_count (self):
        """The total number of matched post-accentual falls."""
        return self.total_match_counter['M1'] + self.total_match_counter['CIRC']
    
    @property
    def secure_match_count (self):
        """The total number of matched post-accentual falls."""
        return self.secure_match_counter['M1'] + self.secure_match_counter['CIRC']
    
    @property
    def total_circ_match_count (self):
        """The total number of matched post-accentual falls."""
        return self.total_match_counter['CIRC']
    
    @property
    def secure_circ_match_count (self):
        """The total number of matched post-accentual falls."""
        return self.secure_match_counter['CIRC']
    
    @property
    def total_contra_count (self):
        """The number of post-accentual falls that cannot be accomodated in 
        by conflicting contours in responding stanzas."""
        return self.total_match_counter['C1']
    
    @property
    def secure_contra_count (self):
        """The number of post-accentual falls that cannot be accomodated in 
        by conflicting contours in responding stanzas."""
        return self.secure_match_counter['C1']

    @property
    def total_repeat_count (self):
        """The number of repeated notes required by a stanza"""
        return self.total_cont_counter['='] + self.total_cont_counter['=-A']
    
    @property
    def secure_repeat_count (self):
        """The number of repeated notes required by a stanza"""
        return self.secure_cont_counter['='] + self.secure_cont_counter['=-A']
    
    @property
    def total_compatible_count (self):
        """The number of notes not requiring a melodic repetiton"""
        return self.total_syl_count - self.total_repeat_count
    
    @property
    def secure_compatible_count (self):
        """The number of notes not requiring a melodic repetiton"""
        return self.secure_syl_count - self.secure_repeat_count

    @property
    def total_matched_wb_count (self):
        """The number of aligned wordbreaks."""
        return self.total_match_counter['N']
    
    @property
    def secure_matched_wb_count (self):
        return self.secure_match_counter['N']
    
    #Percentages
    
    @property 
    def total_repeat_percentage (self):
        return (self.total_repeat_count / self.total_syl_count)

    @property 
    def secure_repeat_percentage (self):
        return (self.secure_repeat_count / self.secure_syl_count)
    
    @property 
    def total_compatible_percentage (self):
        return (self.total_compatible_count / self.total_syl_count)

    @property 
    def secure_compatible_percentage (self):
        return (self.secure_compatible_count / self.secure_syl_count)

    @property
    def total_match_percentage (self):
        return (self.total_match_count / self.total_syl_count)

    @property
    def secure_match_percentage (self):
        return (self.secure_match_count / self.secure_syl_count)
    
    @property
    def total_circ_match_percentage (self):
        return (self.total_circ_match_count / self.total_syl_count)

    @property
    def secure_circ_match_percentage (self):
        return (self.secure_circ_match_count / self.secure_syl_count)
    
# DISPLAY

    def display_data (self, match_status=False):
        """Returns a list of lines, each of which is a nested tuple containing 
        that line's attributes: 
            (syl_widths, 
            (meter, stanza_1_syls, stanza_2_syls... etc. , contours)
            )
        If the match_status flag is set, then the match_status is included last.
        """
        nested_lines = []
        start = 0
        for i in range(self.line_count):
            end = start + self.strophe.lines[i].syl_count
            numbers = [str(n) for n in range(start, end)]
            meter = self.meter[start:end]
            contours = self.pretty_contours[start:end]
            text_list_by_syl = []
            match_statuses = []
            widths = []
            for syl_group in self.syllables[start:end]:
                text_list_by_syl.append(syl_group.join_texts)
                widths.append( max(len(s) for s in syl_group.join_texts) )
                if match_status:
                    match_statuses.append(syl_group.match_status)
            text_list = list(zip(*text_list_by_syl))
            meter = self.meter[start:end]
            if match_status:
                line_data = (widths,
                         (numbers, meter) + tuple(text_list) + (contours, match_statuses)
                        )
            else:
                line_data = (widths,
                         (numbers, meter) + tuple(text_list) + (contours,)
                        )
            nested_lines.append(line_data)
            start = end
        return nested_lines

    def display (self, match_status=False):
        print()
        print(self.name)
        print()
        data = self.display_data(match_status=match_status)
        for (widths, attributes) in data:
            for a in attributes:
                print_items = [str(i).ljust(width) for width, i in zip(widths, a)]
                print(''.join(print_items))
            total_length = sum(widths)
            print ('-'*total_length)
  
    def print_stats (self, secure=True):
        self.add_stats()
        print (self.name)
        if secure:
            print('Stats excluding corrupt syllables')
        else:
            print('Stats including corrupt syllables')
        template = """Stats {} corrupt syllables
        
              Matches (both post-accentual fall) : {}
              Repeats (contradiction of contour) : {}
              Contra (repeat on post-accentual)  : {}
             
              Matches/Syls : {}
              Repeats/Syls : {}"""
        if secure:
            print(template.format(
              'excluding', self.secure_matches, self.secure_repeats, self.secure_contradictions,
              self.secure_match_percentage, self.secure_repeat_percentage)
              )
        else:
            print(template.format(
              'including', self.total_matches, self.total_repeats, self.total_contradictions,
              self.total_match_percentage, self.total_repeat_percentage)
              )
        
