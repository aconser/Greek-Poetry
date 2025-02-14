#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLASS GENRE 

@author: Dr. Anna Conser, University of Cincinnati, anna.conser@uc.edu
@license: MIT

This is the top class, created as a means to compile all data.

"""


import Analysis.class_author as CA
from Utilities.stanza_utilities import CORPUS_DIR

AUTHOR_LIST = ['Aeschylus', 'Sophocles', 'Euripides']

class Genre:
    def __init__ (self, Genre_Name, authors=AUTHOR_LIST):
        self.name = Genre_Name
        self.authors = [CA.Author(auth) for auth in authors]
        self._all_data = None
     
        
     
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
            for auth in self.authors:
                compatible, all_matches, matched_peaks, syls, peaks, circs, str_circs, ant_circs, matched_circs = auth.all_data
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
    

#DATA EXPORT
    
    HEADINGS = ['Author',
                'Play', 
                'Pair', 
                'Compatible', 
                'Matches/Syls', 
                'Matched Peaks/Peaks', 
                'Circs/Syls',
                'Str Circs/Syls',
                'Ant Circs/Syls',
                'Matched Circs']
    
    def genre_data (self, headings=True):
        data = ["All Authors",
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
            data = headings + data
        return data
    
        
    #EXPORT EVERYTHING!!!
    def export_all_data (self):
        directory_name = CORPUS_DIR
        with open(directory_name+'FULL_genre_data.csv', "w", encoding='utf-8') as output:
            
            output.write(','.join(self.HEADINGS) +'\n')
            output.write('\n')

            output.write('OVERALL STATISTICS FOR GENRE')
            output.write('\n')
            output.write(','.join([str(x) for x in self.genre_data(headings=False)]) + '\n')
            output.write('\n')

            output.write('BY AUTHOR')
            output.write('\n')
            for a in self.authors:
                output.write(','.join([str(x) for x in a.author_data(headings=False)]) + '\n')
            output.write('\n')
            
            output.write('BY PLAY')
            output.write('\n')
            for a in self.authors:
                for p in a.plays:
                    output.write(','.join([str(x) for x in p.play_data(headings=False)]) + '\n')
            output.write('\n')

            output.write('BY PAIR')
            output.write('\n')
            for a in self.authors:
                for p in a.plays:
                    for pair in p.pairs:
                        output.write(','.join([str(x) for x in pair.pair_data]) + '\n')
        print('Hooray! Data exported to {}'.format(CORPUS_DIR))

#%% Scripts to call these functions

import Analysis.class_genre as CG
Tragedy = CG.Genre('Tragedy')
Tragedy.export_all_data()

import Analysis.class_author as CA

Aeschylus = CA.Author ('Aeschylus')
Sophocles = CA.Author ('Sophocles')
Euripides = CA.Author ('Euripides')
Control_Groups = CA.Author ('Control')

for play in Sophocles.plays:
    for pair in play.pairs:
        print(pair.secure_syl_count)

