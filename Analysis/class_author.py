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
                    'Control' : [('Trimeter', 'Soph-Ant-Trimeter'),
                                 ('Prose', 'Lysias'),
                                 ('Anapests', 'AgAnapests'),
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
        self._cmrs = None

    @property
    def cmrs (self):
        if not self._cmrs:
            circ_count = 0
            match_count = 0
            repeat_count = 0
            syl_count = 0
            for p in self.plays:
                #print(p.name)
                circs, matches, repeats, syls = p.circs_matches_repeats_syls
                circ_count += circs
                match_count += matches
                repeat_count += repeats
                syl_count += syls
            self._cmrs = (circ_count, match_count, repeat_count, syl_count)
        return self._cmrs
    
    @property
    def percent_match (self):
        circs, matches, repeats, syls = self.cmrs
        return (matches/syls)

    @property
    def percent_repeat (self):
        circs, matches, repeats, syls = self.cmrs
        return (repeats/syls)

    @property
    def percent_matched_circ (self):
        circs, matches, repeats, syls = self.cmrs
        return (circs/syls)
                
    def display (self):
        """Compiles data for all the syllables in a whole play."""
        def display_percent(float_decimal):
            return(int(float_decimal*1000)/10)
        template = """
    {}
        Compatible Syllables:\t{}%
        Matched (non-grave):\t{}%
        Matched Circumflexes:\t{}%"""
        
        print()
        print(self.name)
        print(template.format('TOTALS', 
                              display_percent(1-self.percent_repeat),
                              display_percent(self.percent_match),
                              display_percent(self.percent_matched_circ)))
        for p in self.plays:
            print(template.format(p.name, 
                                  display_percent(1-p.percent_repeat),
                                  display_percent(p.percent_match),
                                  display_percent(p.percent_matched_circ)))
    
    def export_stats (self):
        directory_name = CORPUS_DIR
        with open(directory_name+self.name+'-stats.csv', "w", encoding='utf-8') as output:
            output.write('Author, Play, Compatible, Matched Accent, Matched Circumflex' +'\n')
            for p in self.plays:
                row_data =[self.name, p.name, (1-p.percent_repeat), 
                           p.percent_match, p.percent_matched_circ]
                row_text =','.join([str(x) for x in row_data]) + '\n'
                output.write(row_text)
            output.write('\n')
            output.write('AUTHOR, STANZA_NAME, SYL_COUNT, COMPATIBLE, MATCH, CIRC' + '\n')
            for play in self.plays:
                for p in play.pairs:
                    stanza_name = p.name.replace(self.name+'-', '')
                    row = [self.name, stanza_name, p.secure_syl_count, 
                           p.secure_compatible_percentage, 
                           p.secure_match_percentage, p.secure_circ_match_percentage]
                    row_text = ','.join([str(x) for x in row]) + '\n'
                    output.write(row_text)
        
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
           