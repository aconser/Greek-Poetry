# -*- coding: utf-8 -*-
"""
CLASS WORD

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""

from Greek_Prosody.characters import PUNCTUATION
from Greek_Prosody.accents import get_accent
from Greek_Prosody.syllables import get_syllables, has_vowel
import re

NORMAL_ENCLITICS = ['μου', 'μοι', 'με', 'μευ', 'σου', 'σοι', 'σε',
             'οὑ', 'οἱ', 'ἑ', 'σευ', 'σεο', 'τοι', 'νιν',                #pronouns
             
             'τις', 'τι', 'τινος', 'του', 'τινι', 'τῳ', 'τινα',          #indefinite singulars
             'τινε', 'τινοιν', 'τινες', 'τινων', 'τισι', 'τινας',        #indefinite plurals (unaccented)
             'τινός', 'τοῦ', 'τινί', 'τινά', 'τινέ',                     #indefinite (acute)
             'τινοῖν', 'τινές', 'τινῶν', 'τισί', 'τινάς',
             'τινὸς', 'τινὶ', 'τινὰ', 'τινὲ', 'τινὲς', 'τισὶ', 'τινὰς',  #indefinite (grave)
             'τινʼ', 'τισʼ',
             
             'που', 'ποθι', 'ποθί', 'ποθὶ', 'ποθεν', 'ποθέν', 'ποθὲν',   #indefinite adverbs 
             'ποτε', 'ποτέ', 'ποτὲ', 'ποτʼ', 'ποθʼ', 'πω', 'πως', 'πῃ', 'ποι', 
             
             'εἰμι', 'ἐστι', 'ἐστον', 'ἐσμεν', 'ἐστε', 'εἰσι',           #'to be' (unaccented)
             'εἰμί', 'ἐστί', 'ἐστόν', 'ἐσμέν', 'ἐστέ', 'εἰσί',           #        (acute)
             'εἰμὶ', 'ἐστὶ', 'ἐστὸν', 'ἐσμὲν', 'ἐστὲ', 'εἰσὶ',           #        (grave)
             'φημι', 'φησι', 'φατον', 'φαμεν', 'φατε', 'φασι',           #'to say' (unaccented)
             'φημί', 'φησί', 'φατόν', 'φαμέν', 'φατέ', 'φασί',           #         (acute)
             'φημὶ', 'φησὶ', 'φατὸν', 'φαμὲν', 'φατὲ', 'φασὶ',            #         (grave)
             
             'γε', 'τε', 'τοι', 'περ', 'κε', 'θην', 'ῥα', 'νυ', 'νυν'    #particles
             ]

NORMAL_PROCLITICS = ['ὁ', 'ἡ', 'οἱ', 'αἱ', 'ἐν', 'εἰς', 'ἐς',  #traditional enclitics
              'ἐξ', 'ἐκ', 'εἰ', 'αἰ', 'ὡς', 'οὐ', 'οὐκ', 'οὐχ',
              
              'ἀμφʼ', 'ἀμφί', 'ἀμφίς', 'ἀμφὶ', 'ἀμφὶς', #prepositions accented on ultima
              'ἀνʼ', 'ἀνά', 'ἀνὰ', 
              'ἀντί', 'ἀντὶ', 
              'ἀπʼ', 'ἀπό', 'ἀπύ', 'ἀπὸ', 'ἀπὺ', 
              'διʼ', 'διά', 'διὰ', 
              'ἐκτός', 'ἐκτὸς', 'ἐνί', 'ἐνὶ', 
              'ἐπʼ', 'ἐπί', 'ἐπὶ', 'ἐφʼ',
              'καθʼ', 'κατʼ', 'κατά', 'κατὰ', 
              'μεθʼ', 'μετʼ', 'μετά', 'μετὰ', 
              'παρʼ', 'παρά', 'παρὰ', 
              'περί', 'περὶ', 
              'πλήν', 'πλὴν', 'πλάν', 'πλὰν',
              'πρός', 'πρὸς', 'ποτί', 'ποτὶ', 'προτί', 'προτὶ',
              'πρό', 'πρὸ',
              'σύν', 'σὺν', 
              'ὑπό', 'ὑπὸ', 'ὑφʼ', 'ὑπʼ', 
              'ὑπέρ', 'ὑπὲρ',
              'ὑποπρό', 'ὑποπρὸ', 'ὑππρό', 'ὑππρὸ',
              'χωρίς', 'χωρὶς',
              
              'ὁ', 'ἡ', 'τό', 'τὸ', 'τοῦ', 'τῆς',       #def articles
              'τῷ', 'τῇ', 'τόν', 'τὸν', 'τήν', 'τὴν',   #(redundant forms removed)
              'οἱ', 'αἱ', 'τά', 'τὰ', 'τῶν', 'τοῖς', 'ταῖς', 
              'τούς', 'τοὺς', 'τάς', 'τὰς',
              'τώ', 'τὼ', 'τᾱ́', 'τᾱ̀', 'τοῖν', 'ταῖν',
              'τάν', 'τὰν', 'τᾷ', 'ἁ', 'τᾶς',   #doric forms....
              
              'οὐ', 'οὐκ', 'οὐχ', 'οὐδ’',
              
              'ἠδʼ', 'ἀλλʼ'
              ]

OCT_ENCLITICS = [re.sub('ς|σ', 'ϲ', w) for w in NORMAL_ENCLITICS if re.search('ς|σ', w)]
OCT_PROCLITICS = [re.sub('ς|σ', 'ϲ', w) for w in NORMAL_PROCLITICS if re.search('ς|σ', w)]

ENCLITICS = NORMAL_ENCLITICS + OCT_ENCLITICS
PROCLITICS = NORMAL_PROCLITICS + OCT_PROCLITICS
                 
APOSTROPHE = u'\u02bc',  #MODIFIER LETTER APOSTROPHE

def _clean (text):
    """Removes whitespace and punctuation from edges of a string.  Punctuation
    does not include apostrophes marking elision."""
    return text.strip().strip(PUNCTUATION)

def is_enclitic (word):
    """Checks whether a word is one of the Greek enclitics. For forms with an 
    acute, I have included both the acute and the grave form.  Elided forms are
    also included.
    
    :param str word: a Greek word
    :rtype: bool
    """
    return _clean(word) in ENCLITICS

def is_proclitic (word):
    """Checks whether a word is one of the Greek proclitics. In addition to the 
    traditional (unaccented) proclitics, I have included prepositions accented 
    on the ultima, and all definite articles.  For forms with an acute, I have 
    included both the acute and the grave form, as well as elided (and roughened)
    forms. I am also including as proclitic any word which has lost its accent
    through elision but is not one of the enclitics.
    
    Note: I should check this against Devine and Stevens when I have the chance.
    They might include even more forms.
    
    :param str word: a Greek word
    :rtype: bool
    """
    w = _clean(word)
    if w in PROCLITICS:
        return True
    if w.endswith(APOSTROPHE) and get_accent(w) == None and not is_enclitic(w):
        return True
    else:
        return False
    
###############################################################################
        
class Word ():
    """A class to create and hold data concerning a single word."""
    def __init__ (self, text, POS=''):
        self.text = text
        self.initial_resolution = text.startswith('|')
        self._syl_count = None
        self.syllables = get_syllables(self.text)
            # Note: if first syl starts with a pipe (indicating resolution), 
            # it is included here, but isn't really a 'syllable' in the full sense.
        self.POS = POS
        self.tags = []
        self.number = None
        self.lemma = '' # ONCE CLTK IS WORKING, ADD LEMMA
        if self.text[0].isupper():
            if self.POS.startswith('N'):
                self.tags.append('prop_n')
            else:
                self.tags.append('cap')
        if is_proclitic(self.text):
            self.tags.append('proclitic')
        if is_enclitic(self.text):
            self.tags.append('enclitic')
    
    @property
    def syl_count (self):
        if not self._syl_count:
            if not has_vowel(self.text):
                #placeholder syllable (for corruption)
                if '$' in self.text:
                    self._syl_count = self.text.count('$')
                #non-syllable word (e.g. δ’)
                else:
                    self._syl_count = 0
            elif self.initial_resolution:
                # word starts with a resolution, so that syl doesn't count
                self._syl_count = len(self.syllables) - 1
            else:
                self._syl_count = len(self.syllables)
        return self._syl_count
    
    def is_enclitic (self):
        return is_enclitic(self.text)
    
    def is_proclitic (self):
        return is_proclitic(self.text)

###############################################################################

class Complex_Word ():
    """A class to create and hold data concerning a single word, which has had
    musical data added from the surrounding stanza_group context."""
    
    def __init__ (self, word, syllables):
        """Parameters are a Word object and the corresponding Syllable objects.
        """
        self.text = word.text
        self.syllables = syllables
            # Note: if first syl starts with a pipe (indicating resolution), 
            # it is included here, but isn't really a 'syllable' in the full sense.
        self.syl_count = len(self.syllables)
        self.POS = word.POS
        self.word_tags = word.tags
        self.number = word.number
        self.lemma = word.lemma
        self.corrupt = any(s.corrupt for s in self.syllables)
        self._meter = []
        self._contours = []
        self._pretty_contours = []
        self._match_statuses = []
        self._repeat_count = None
        self._match_count = None
        
    @property
    def meter (self):
        """Metrical prosody based on the combined stanzas."""
        if not self._meter:
            self._meter = [syl.prosody for syl in self.syllables]
        return self._meter
    
    @property
    def contours (self):
        """The merged contour data for responding stanzas, excluding the contour 
        of the final syllable, which does not affect the musical setting of the word.
        """
        if not self._contours:
            all_contours = [s.contour for s in self.syllables]
            self._contours = all_contours[:-1]
        return self._contours

    @property    
    def match_statuses (self):
        """Just the match statuses relevant to the musical setting of the word 
        itself, that is, excluding the final contour.
        """
        if not self._match_statuses:
            all_statuses = [s.match_status for s in self.syllables]
            self._match_statuses = all_statuses[:-1]
        return self._match_statuses
    
    @property
    def pretty_contours (self):
        """Contours as needed for display / composition. Melodic movement is 
        indicated by arrows.
        """
        if not self._pretty_contours:
             self._pretty_contours = [s.pretty_contour for s in self.syllables]
        return self._pretty_contours
    
    @property
    def measured_syl_count (self):
        """The number of syllables with qualities that affect the setting of
        the word. For example, Σωκράτης has three syllables, but only two melodic
        note changes, so only two measured syls."""
        return max(len(self.syllables)-1, 0)
    @property
    def match_count (self):
        """The total number of matched post-accentual falls."""
        return self.match_statuses.count('M1')
    
    @property
    def contra_count (self):
        """The number of post-accentual falls that cannot be accomodated in 
        by conflicting contours in responding stanzas."""
        return self.match_statuses.count('C1')
    
    @property
    def repeat_count (self):
        """The number of repeated notes required by a stanza"""
        return self.contours.count('=')
    
    @property 
    def repeat_percentage (self):
        return self.repeat_count / self.measured_syl_count

    @property
    def match_percentage (self):
        return self.match_count / self.measured_syl_count

    