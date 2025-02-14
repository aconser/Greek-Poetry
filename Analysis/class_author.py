#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLASS AUTHOR

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""

import Analysis.class_play as CP
from Utilities.stanza_utilities import CORPUS_DIR

#Ag = CP.load_play('Agamemnon', 'Aesch-Ag')
#Ag.display()

"""
TOTALS
   Circs:       1%
   Matched:     13%
   Non-Repeat:  80%
"""

#Ch = CP.load_play('Choephori', 'Aesch-Lib')
#Ch.display()

"""
TOTALS
   Circs:       1%
   Matched:     14%
   Non-Repeat:  82%
"""

#Eu = CP.load_play('Eumenides', 'Aesch-Eum')
#Eu.display()

"""
TOTALS
   Circs:       1%
   Matched:     13%
   Non-Repeat:  82%
"""

PLAY_LIST_DICT = {'Aeschylus' : [('Persae', 'Aesch-Pers'),
                                 ('Septem', 'Aesch-Seven'),
                                 ('Suppliants', 'Aesch-Supp'),
                                 ('Agamemnon', 'Aesch-Ag'),
                                 ('Choephori', 'Aesch-Lib'),
                                 ('Eumenides', 'Aesch-Eum'),
                                 ('Prometheus', 'Aesch-PB'),
                                 ],
                    'Sophocles' : [('Trachiniae', 'Soph-Trach'),
                                   ('Antigone', 'Soph-Ant'),
                                   ('Ajax', 'Soph-Ajax'),
                                   ('Oedipus Rex', 'Soph-OT'),
                                   ('Electra', 'Soph-El'),
                                   ('Philoctetes', 'Soph-Phil'),
                                   ('Oedipus Coloneus', 'Soph-OC')
                                   ],
                    'Euripides' : [('Alcestis', 'Eur-Alc'),
                                   ('Medea', 'Eur-Med'),
                                   ('Hippolytus', 'Eur-Hipp'),
                                   ('Andromache', 'Eur-Andr'),
                                   ('Hecuba', 'Eur-Hec'),
                                   #('Troades', 'Eur-Tro'),
                                   ('Orestes', 'Eur-Orest'),
                                   ('Bacchae', 'Eur-Ba'),
                                   # Additional files, based on performance texts rather than OCT
                                   #('Heracles', 'Eur-Her-newest'), # Performance text - Loeb based
                                   #('Iphigenia in Aulis', 'Eur-IA'), #   Performance Text -- Loeb based (?)
                                   ],
                    'Control' : [('Trimeter', 'Soph-Ant-Trimeter'),
                                 ('Prose', 'Lysias'),
                                 ('Anapests', 'AgAnapests'),
                                 ],
                    }

# =============================================================================
# NOTE ON EXCLUSIONS:
#     I have excluded stanza pairs which are identical in the strophe and antistrophe,
#     namely the following:
#         -- Agamemnon 5a (part of Cassandra's monody)
#         -- Suppliants 7g 
# =============================================================================
#%%

class Author:
    def __init__ (self, Author_Name):
        self.name = Author_Name
        self.plays = [CP.load_play(name, play, author=self.name) \
                      for name, play in PLAY_LIST_DICT[self.name]]
        self._all_data = None

# COMPILE DATA
     
    @property
    def all_data (self):
        if not self._all_data:
            compatible_count = 0
            all_match_count = 0
            matched_peak_count = 0
            syl_count = 0
            peak_count = 0
            circ_count = 0
            str_circ_count = 0
            ant_circ_count = 0
            matched_circ_count = 0
            for play in self.plays:
                compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = play.all_data
                compatible_count += compatible
                all_match_count += all_matches
                matched_peak_count += matched_peaks
                syl_count += syls
                peak_count+= peaks
                circ_count+= circs
                str_circ_count+= str_circs
                ant_circ_count+= ant_circs
                matched_circ_count += matched_circs

            self._all_data = (compatible_count, 
                              all_match_count,
                              matched_peak_count,
                              syl_count, 
                              peak_count, 
                              circ_count, 
                              str_circ_count, 
                              ant_circ_count, 
                              matched_circ_count)
        return self._all_data
    
    @property
    def syl_count (self):
        compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = self.all_data
        return (syls)
    
    @property
    def percent_match (self):
        compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = self.all_data
        return (all_matches/syls)

    @property
    def percent_repeat (self):
        compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = self.all_data
        return (1-compatible/syls)
    
    @property
    def percent_compatible (self):
        compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = self.all_data
        return (compatible/syls)

    @property
    def percent_matched_circ (self):
        compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = self.all_data
        return (matched_circs/syls)
                
    @property
    def percent_matched_peaks (self):
        compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = self.all_data
        return (all_matches*2/peaks)
                    
    @property
    def percent_circs (self):
        compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = self.all_data
        return (circs/syls)
                    
    @property
    def percent_str_circs (self):
        compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = self.all_data
        return (str_circs/syls)
    
    @property
    def percent_ant_circs (self):
        compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = self.all_data
        return (ant_circs/syls)
    

# DISPLAY DATA FOR THE AUTHOR
    
    def display (self):
        """Compiles data for all the syllables across a whole author."""
        def display_percent(float_decimal):
            return(int(float_decimal*1000)/10)
        template = """
    {}
        Compatible Syllables:\t{}%
        Syls w/Matched Peaks:\t{}%
        Peaks that Respond:\t{}%
        Syls with Circumflex:\t{}%
        Str Syls with Circ:\t{}%
        Ant Syls with Circ:\t{}%
        Matched Circumflexes:\t{}%"""
        
        print()
        print(self.name)
        print()
        
        print(template.format('TOTALS', 
                              display_percent(self.percent_compatible),
                              display_percent(self.percent_match),
                              display_percent(self.percent_matched_peaks),
                              display_percent(self.percent_circs),
                              display_percent(self.percent_str_circs),
                              display_percent(self.percent_ant_circs),
                              display_percent(self.percent_matched_circ)))
        for p in self.plays:
            print(template.format(p.name, 
                                  display_percent(p.percent_compatible),
                                  display_percent(p.percent_match),
                                  display_percent(p.percent_matched_peaks),
                                  display_percent(p.percent_circs),
                                  display_percent(p.percent_str_circs),
                                  display_percent(p.percent_ant_circs),
                                  display_percent(p.percent_matched_circ)))

# EXPORT DATA

    HEADINGS = ['Author',
                'Play', 
                'Pair', 
                'Compatible', 
                'Matches/Syls', 
                'Matches/Peaks', 
                'Circs/Syls',
                'Str Circs/Syls',
                'Ant Circs/Syls',
                'Matched Circs']
    
    def author_data (self, headings=True):
        data = [self.name,
                "All Plays",
                "All Pairs",
                self.percent_compatible,
                self.percent_match,
                self.percent_matched_peaks,
                self.percent_circs,
                self.percent_str_circs,
                self.percent_ant_circs,
                self.percent_matched_circ]
        if headings:
            data.prepend(headings)
        return data
    
        
    def export_all_data (self):
        #Set up csv file and add headings:
        directory_name = CORPUS_DIR
        with open(directory_name+self.name+'-all_data.csv', "w", encoding='utf-8') as output:
            output.write(','.join(self.HEADINGS) +'\n')
            output.write(','.join([str(x) for x in self.author_data(headings=False)]) +'\n')
            output.write('\n')

            output.write('ALL PLAYS')
            output.write('\n')
            for p in self.plays:
                output.write(','.join([str(x) for x in p.play_data(headings=False)]) + '\n')
            output.write('\n')
            output.write('ALL PAIRS')
            output.write('\n')
            for p in self.plays:
                for pair in p.pairs:
                    output.write(','.join([str(x) for x in pair.pair_data]) + '\n')

#NOT USED ANYMORE?
    def export_graph_data (self):
        directory_name = CORPUS_DIR
        with open(directory_name+self.name+'-graph.csv', "w", encoding='utf-8') as output:
            output.write('Author, Play, Matched Circumflex, Other Matched Accent, Other Compatible' +'\n')
            for p in self.plays:
                circ = p.percent_matched_circ
                other_accent = p.percent_match - p.percent_matched_circ
                other_compat = 1-p.percent_repeat-p.percent_match
                row_data =[self.name, p.name, circ, other_accent, other_compat]
                row_text =','.join([str(x) for x in row_data]) + '\n'
                output.write(row_text)
            output.write('\n')
           