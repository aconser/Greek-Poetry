# -*- coding: utf-8 -*-
"""
CLASS PLAY

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT

NOTE: Display functions at the play level are currently broken.

"""
import re

from Utilities.stanza_utilities import import_csv
from .class_stanza import Stanza
from .class_StanzaGroup import StanzaGroup

#%%
class Play ():
    def __init__ (self, name, file, directory):
        self.name = name
        self.raw_csv = import_csv(file, directory)
        self.pairs=self._stanza_pairs()
        self._meter_dict = {}
        self._graph_data = None
        self._matches_repeats_syls = ()
        
    def _stanza_pairs (self):
        stanza_pairs = []
        for row in self.raw_csv:
            if len(row) == 6:
                song_num, stanza_name, st_raw, an_raw, meter, notes = row
                meter_ids = None
            elif len(row) == 7:
                song_num, stanza_name, st_raw, an_raw, meter, meter_ids, notes = row
            elif len(row) == 5:
                song_num, stanza_name, st_raw, an_raw, notes = row
                meter = None
                meter_ids = None
            else:
                raise ValueError(
                        'CSV file ({}) has incorrect number of columns.'.format(self.file))
            name = self.name + '-' + song_num + '-' + stanza_name
            st = Stanza(name, st_raw)
            an = Stanza(name, an_raw)
            pair = StanzaGroup(name, [st, an])
            if meter:
                pair._line_meters = meter.splitlines()
                clean_meter = meter.replace('\n', '')
                pair._meter = [m for m in clean_meter]
            if meter_ids:
                pair._meter_ids = meter_ids
            pair.notes = notes
            pair.song_number = int(song_num)
            stanza_pairs.append(pair)
        return stanza_pairs
    
    def tagged_words (self, tag):
        tagged = []
        for p in self.pairs:
            tagged.extend(p.tagged_words(tag))
        return tagged
    
    def word_tag_stats (self, tag):
        match_total = 0
        repeat_total = 0
        syl_total = 0
        for p in self.pairs:
            matches, repeats, syls = p.word_tag_stats(tag)
            match_total += matches
            repeat_total += repeats
            syl_total += syls
        return (match_total, repeat_total, syl_total)
    
    def word_tag_analysis (self, tag):
        matches, repeats, syls = self.word_tag_stats(tag)
        percent_match = int(matches/syls*100)
        percent_repeat = int(repeats/syls*100)
        play_match, play_repeat = self.percent_match_repeat
        print("""
              Analysis of tag '{}' :
              percent match:  {}
              percent repeat: {}
              total syllables: {}
              
              play match % : {}
              play repeat% : {}
              """.format(tag, percent_match, percent_repeat, syls,
              int(play_match*100), int(play_repeat*100)))
    
    def meter_dict (self):
        if not self._meter_dict:
            meter_dict = {}
            for p in self.pairs:
                for l in p.lines:
                    meter = ''.join(l.meter) #translate list into string
                    if meter in meter_dict:
                        meter_dict[meter].append(l.stats)
                    else:
                        meter_dict[meter] = [l.stats]
            self._meter_dict = meter_dict
        return self._meter_dict
    
    @property
    def circs_matches_repeats_syls (self):
        if not self._matches_repeats_syls:
            match_count = 0
            repeat_count = 0
            syl_count = 0
            for p in self.pairs:
                circ_count += p.secure_circ_match_count
                match_count += p.secure_match_count
                repeat_count += p.secure_repeat_count
                syl_count += p.secure_syl_count
            self._matches_repeats_syls = (match_count, repeat_count, syl_count)
        return self._matches_repeats_syls
    
    @property
    def percent_match_repeat(self):
        matches, repeats, syls = self.matches_repeats_syls
        return (matches/syls, repeats/syls)
    
    @property
    def percent_matched_circ (self):
        circ_count = 0
        syl_count = 0
        for p in self.lays:
            circ_count += p.secure_circ_match_count
            syl_count += p.secure_syl_count
        return circ_count/syl_count
            
    def full_stats (self):
        for p in self.pairs:
            p.print_stats()

    def print_pair_stats_OLD (self):
        comp_list = []
        rep_list = []
        for s in self.pairs:
            included_syls = s.syl_count
            total_matches = s.M1 + s.M2 + s.M3
            total_cons = s.C1 + s.C2 + s.C3
            comp_number = int((total_matches - total_cons)/included_syls * 100)
            comp_list.append(comp_number)
            rep_number = int(s.repeat_percentage *100)
            rep_list.append(rep_number)
            print (s.name)
            print("NUM: " +str(comp_number))
            print("REP: " +str(rep_number))
        #    print(s.repeat_count)
            print()
        print('COMP LIST')
        print(comp_list)
        print('REP LIST')
        print(rep_list)
    
    def display (self):
        """Compiles data for all the syllables in a whole play."""
        if not self.compiled_data:
            
        syls = 0
        all_matches = 0
        matched_circs = 0
        non_repeats = 0
        
        
    def displayOLD (self):
        syl_count = 0
        match_total = 0
        repeat_total = 0
        for s in self.pairs:
            s.add_stats()
            syl_count += s.syl_count
            match_total += s.M1
            repeat_total += s.repeat_count
            percent_match = int(s.M1/s.syl_count * 100)
            percent_repeat = int(s.repeat_count/s.syl_count * 100)
            print()
            print (s.name)
            if percent_match > 14:
                print("    M1 %  : "+str(percent_match)+ '-- GOOD')
            elif percent_match < 10:
                print("    M1 %  : "+str(percent_match)+ '-- BAD')
            else:
                print("    M1 %  : "+str(percent_match))
            if percent_repeat > 20:
                print("    Rep % : "+str(percent_repeat)+ '-- BAD')
            elif percent_repeat < 14:
                print("    Rep % : "+str(percent_repeat)+ '-- GOOD')
            else:
                print("    Rep % : "+str(percent_repeat))
        match_average = int(match_total/syl_count * 100)
        repeat_average = int(repeat_total/syl_count * 100)
        print()
        print('Average Percent Match: ' + str(match_average))
        print('Average Percent Repetition: ' + str(repeat_average))
   
    def add_stats (self):
        M1 = 0    # All contours are 'DN-A'
        M2 = 0       # All contours are 'DN-A' or 'DN'
        M3 = 0           # All contours are 'UP' or all are 'DN'
        C1 = 0 # Position contains 'DN-A' and 'UP' or '='
        C2 = 0    # Position contains 'UP' and 'DN'
        C3 = 0   # Position contains '=' and 'UP or 'DN'
        M4 = 0    # All other combinations (weak match, since compatible)
        repeats = 0
        syl_count = 0
        for p in self.pairs:
            p.add_stats()
            M1 += p.M1
            M2 += p.M2
            M3 += p.M3
            M4 += p.M4
            C1 += p.C1
            C2 += p.C2
            C3 += p.C3
            repeats += p.repeat_count
            syl_count += p.syl_count
        self.M1 = M1
        self.M2 = M2
        self.M3 = M3
        self.M4 = M4
        self.C1 = C1
        self.C2 = C2
        self.C3 = C3
        self.repeat_count = repeats
        self.syl_count = syl_count
        self.repeat_percentage = repeats/syl_count
        self.match_percentage = M1/syl_count
        
    def print_stat_totals (self):
        self.add_stats()
        print (self.name)
        print("""
              M1 [DN-A]          : {}
              CIRC               : {}
              M2 [DN-A, DN]      : {}
              M3 [DN], [UP,UP-G] : {}
              M4 (contains 'N')  : {}
              C3 DN / UP-G       : {}
              C2 DN / UP         : {}
              C1 DN-A /[UP, UP-G]: {}
              
              Repeats : {}
              Repeats/Syls : {}
              
              Matches/Syls : {}""".format(
              self.M1, self.CIRC, self.M2, self.M3, self.M4, self.C3, self.C2, self.C1, 
              self.repeat_count, self.repeat_percentage, (self.M1/self.syl_count)))
    
    def graph_data (self, short_name=False):
        if self._graph_data:
            return self._graph_data
        else:
            self.add_stats()
            rows = []
            for p in self.pairs:
                if short_name:
                    stanza_name = p.name.replace(self.name+'-', '')
                else:
                    stanza_name = p.name
                row = [self.name, p.song_number, stanza_name, p.syl_count, p.repeat_percentage, p.match_percentage]
                rows.append(row)
            self._graph_data = rows
            return rows
        
    def display_graph (self):
        for row in self.graph_data():
            pass
        
    def export_graph_csv (self, directory_name, short_name=False):
        with open(directory_name+self.name+'-graphdata.csv', "w", encoding='utf-8') as output:
            for row in self.graph_data():
                row_text = ','.join([str(x) for x in row]) + '\n'
                output.write(row_text)
    
    def print_graph_csv (self, short_name=False):
        for row in self.graph_data():    
            row_text = ','.join(["\""+str(x)+"\"" for x in row])
            print(row_text)
        
    def export_stats (self, directory_name):
        """Exports the play statistics as a .csv file in the specified directory.
        """
        export_name = self.name
        if export_name.endswith('csv'):
            export_name = export_name[:-4]
        export_name = export_name + '-stats.csv'
        with open(directory_name+export_name, "w", encoding='utf-8') as output:
            for i, s in enumerate(self.pairs):
                quoted_notes = "\"" + s.notes + "\""
                row = [s.name, str(s.secure_syl_count), str(s.secure_match_count), str(s.secure_repeat_count), quoted_notes]
                row_text = ','.join(row) + '\n'
                output.write(row_text)
    
    def export_analysis (self, directory_name):
        """Exports the readable display of the entire play to a text file in the
        specified directory.
        """
        export_name = self.name
        if export_name.endswith('csv') or export_name.endswith('txt'):
            export_name = export_name[:-4]
        export_name = export_name + '-analysis.txt'
        with open(directory_name+export_name, "w", encoding='utf-8') as output:
            output.write(self.name + '- Musical Analysis\n')
            for i, s in enumerate(self.pairs):
                output.write('\n\n{}. {}\n\n'.format(i, s.name))
                data = s.display_data()
                for (widths, attributes) in data:
                    for a in attributes:
                        items = [str(i).ljust(width) for width, i in zip(widths, a)]
                        output.write(''.join(items)+'\n')
                    total_length = sum(widths)
                    output.write('-'*total_length + '\n')
        print("Added file '{}' to directory '{}'".format(export_name, directory_name))
        
    def export_graph_data (self, directory = '/Users/anna/Documents/Dissertation/Graphs/'):
        rows = [['PAIR NAME', 'MATCHED CIRCS', 'MATCHED ACCENTS', 'OTHER NON-REPEAT']]
        for pair in self.pairs:
            name = re.sub(r'^\w+-', '', pair.name)
            circ_match = pair.secure_circ_match_percentage
            other_match = (pair.secure_match_percentage - circ_match)
            other_non_repeat = (1 - pair.secure_repeat_percentage) - (circ_match +other_match)
            rows.append([name, circ_match, other_match, other_non_repeat])
        with open(directory+self.name+'-graphdata.csv', "w", encoding='utf-8') as output:
            for row in rows:
                row_text = ','.join([str(x) for x in row]) + '\n'
                output.write(row_text)
        
            
###########################
        
def load_play (name, csv_name, author = 'Aeschylus'):
    Corpus_Dir = '/Users/anna/Documents/Python Scripts/Corpus/'
    play = Play(name, csv_name +'.csv', Corpus_Dir + author +'/')
    return play

def quick_export_analysis (name, csv_name, author='Aeschylus'):
    play = Play(name, csv_name +'.csv', '..//Corpus/' + author +'/')
    play.export_analysis('.//Corpus/' + author + '/Analyses/')
    return play
