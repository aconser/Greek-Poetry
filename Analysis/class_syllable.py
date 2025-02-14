# -*- coding: utf-8 -*-
"""
CLASS SYLLABLE

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""

import Greek_Prosody.accents as ACCENTS
import re
WORD_END_RE = re.compile(r".*[\s.,;·!’']$")
###############################################

class Syllable:
    def __init__ (self, syl_number, text):
        self.number = syl_number
        self.raw_text = text
        self.text = self.raw_text.strip()
        self.corrupt = False
        self.tags = []
        self.stanza_tags = []
        self.line_tags = []
        self.word_tags = []
        self.POS = ''
        self.lemma = ''
        
    @property
    def accent (self):
        return ACCENTS.get_named_accent(self.text)
    
    @property
    def word_end (self):
        clean = re.sub(r'[†\$⟨⟩\|]', '', self.raw_text)
        if WORD_END_RE.search(clean):
            return True
        else:
            return False 
    
    @property
    def join_text (self):
        if self.word_end:
            return self.text + ' '
        else:
            return self.text + '-'
    
    @property
    def all_tags (self):
        return self.tags + self.stanza_tags + self.line_tags + self.word_tags
    
    def add_tag (self, tag):
        self.tags.append(tag)
        
    @property
    def contains_resolution (self):
        if "|" in self.text:
            return True
        else:
            return False

#######################################
import Greek_Prosody.prosody as PROSODY

class SylGroup:
    """Takes a list/tuple of Syllable objects that occupy the same metrical position
    in responding stanzas and combines their data into a single Syllable object.
    
    :param list syl_list: a list of syllable objects
    :return Syllable combined: a single Syllable object
    """
    
    def __init__ (self, syl_list):
        self.number = syl_list[0].number
        self.stanza = syl_list[0].stanza
#        assert all(syl.number == self.number for syl in syl_list), \
#        'Syllables do not have same number'
        self.syllables = syl_list
        self.corrupt = any(s.corrupt for s in self.syllables)
        self.line_numbers = [s.line_number for s in self.syllables]
        self.prosody = PROSODY.combine_scansions(
                [s.prosody for s in self.syllables], metrical_symbols=True)
        self.meter = self.prosody
        self.all_contours = [s.contour for s in self.syllables]
        self.all_accents = [s.accent for s in self.syllables]
        self._contour = ''
        self._pretty_contour = ''
        self._match_status = ''
        self.tags = []
        self.word_tags = [t for s in self.syllables for t in s.word_tags]
        self.line_tags = [t for s in self.syllables for t in s.line_tags]
        self.word_tags = [t for s in self.syllables for t in s.word_tags]
        self.stanza_tags = [t for s in self.syllables for t in s.stanza_tags]
        self.all_tags = self.tags + self.stanza_tags + self.line_tags + self.word_tags

    @property
    def texts (self):
        return [s.text for s in self.syllables]

    @property
    def join_texts (self):
        return [s.join_text for s in self.syllables]
    
    @property 
    def width (self):
        return max(len(s) for s in self.join_texts)
    
    @property
    def contour_OLD (self):
        if self._contour:
            return self._contour
        contours = self.all_contours
        combined = ''
        if all(c == 'N' for c in contours):
            combined = 'N'
        elif 'UP-G' in contours:
            if 'DN' in contours or 'DN-A' in contours:
                combined = '='
            else:
                combined = 'UP-G'
        elif 'UP' in contours:
            if 'DN' in contours or 'DN-A' in contours:
                combined = '='
            else:
                combined = 'UP'
        elif all(c == 'DN-A' for c in contours):
            combined = 'DN-A'
        else:
            combined = 'DN'
        self._contour = combined
        return combined
    
    @property
    def contour (self):
        if self._contour:
            return self._contour
        contours = self.all_contours
        combined = ''
        if all(a == 'C' for a in self.all_accents):
        #if all(a == 'C' for a in self.all_accents) or (
        #        'C' in self.all_accents and self.prosody in ['⏕', '⏔']):
        
                # In order to make this work, I need to limit to resolutions 
                # with accent on first syllable.
        
            if 'DN-A' in contours:
                combined = 'CIRC-DN'
            else:
                combined = 'CIRC-X'
        elif 'DN-A' in contours:
            if all(c == 'DN-A' for c in contours):
                combined = 'DN-A'
            elif 'UP-G' in contours or 'UP' in contours:
                combined = '=-A'
            else:
                combined = 'DN'
        elif 'DN' in contours:
            if 'UP-G' in contours or 'UP' in contours:
                combined = '='
            else:
                combined = 'DN'
        elif 'UP-G' in contours:
            combined = 'UP-G'
        elif 'UP' in contours:
            combined = 'UP'
        else:
            combined = 'N'
        self._contour = combined
        return combined
    
    @property
    def pretty_contour (self):
        """Contour as needed for display / composition. Melodic movement is 
        indicated by arrows.
        """
        if self._pretty_contour:
            return self._pretty_contour
        arrow_dict = {'N'     : 'x',
                      '='     : '=',
                      '=-A'   : '≠',
                      'UP-G'  : '≤',
                      'UP'    : '↗',
                      'DN-A'  : '⇘',
                      'DN'    : '↘',
                      'CIRC-DN': '★↘',
                      'CIRC-X' : '★x',
                     }
                       #Other arrow options I could sub in: '→', '⇗'
        pretty_contour = arrow_dict[self.contour]
        self._pretty_contour = pretty_contour
        return pretty_contour
    
    @property
    def match_status (self):
        """Categorizes the relationship of the syllable contours in different 
        responding stanzas in the following scheme:
            CIRC:All have a circumflex
            M1 : All have a post-accentual fall (acute/circumflex)
            M2 : Post-accentual fall and downward motion
            M3 : All rising or all falling
            M4 : Compatible via a word break (see note below)
            C1 : Post-accentual fall paired with UP or UP-G
            C2 : UP and DN
            C3 : UP-G and DN
        Note: BUILT TO ANALYZE STANZA PAIRS, rather than Pindar, etc.  If multiple 
        stanzas were being analyzed together, it would be better to distinguish
        the percentage of stanzas that agree at a level, rather than just a binary.
        
        :return str status: a code indicating the level of alignment.
        """
        if self._match_status:
            return self._match_status
        status = ''
        contours = self.all_contours
        #Check for matches:
        if all(a == 'C' for a in self.all_accents):
            status = 'CIRC'
        elif all(c == 'DN-A' for c in contours):
            status = 'M1'
        elif all(c in ['DN-A', 'DN'] for c in contours):
            status = 'M2'
        elif all(c in ['UP', 'UP-G'] for c in contours):
            status = 'M3'
        elif all(c == 'DN' for c in contours):
            status = 'M3'
        elif all(c in ['DN-A', 'DN', 'N'] for c in contours):
            status = 'M4'
        elif all(c in ['UP', 'UP-G', 'N'] for c in contours):
            status = 'M4'
        elif all(c == 'N' for c in contours):
            status = 'M4'
        else:
            #Check for and sort conflicts:
            if 'DN-A' in contours:
                status = 'C1'
            elif 'UP' in contours:
                status = 'C2'
            elif 'UP-G' in contours:
                status = 'C3'
            else:
                assert False, 'Missing Stat Category for syl {}'.format(self.number)
        self._match_status = status
        return status
    
    def is_match (self):
        return self.match_status in ['M1', 'CIRC']
    
    def is_repeat (self):
        return self.contour in ['=', '=-A']
    
    def is_clash (self):
        return self.match_status == 'C1'
        
        
    def add_tag (self, tag):
        self.tags.append(tag)