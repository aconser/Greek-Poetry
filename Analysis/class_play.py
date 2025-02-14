# -*- coding: utf-8 -*-
"""
CLASS PLAY

@author: Anna Conser, University of Cincinnati, anna.conser@uc.edu
@license: MIT


"""
import re

from Utilities.stanza_utilities import import_csv, CORPUS_DIR
from .class_stanza import Stanza
from .class_StanzaGroup import StanzaGroup
from Greek_Prosody import prosody

#%%

class Play ():
    def __init__ (self, name, file, directory, author='Author Name'):
        self.name = name
        self.author = author
        self.file = file
        self.raw_csv = import_csv(file, directory)
        self.pairs=self._stanza_pairs()
        self._meter_dict = {}
        self._graph_data = None
        self._all_data = None
        
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
                        'CSV file ({}) has incorrect number of columns ({}).'.format(self.file, len(row)))
            name = self.name + '-' + song_num + '-' + stanza_name
            #print(name)
            st = Stanza(name, st_raw, author=self.author)
            an = Stanza(name, an_raw, author=self.author)
            pair = StanzaGroup(name, [st, an], author=self.author, play=self.name)
            if meter:
                pair._line_meters = [prosody.pretty_scansion(l) for l in meter.splitlines()]
                clean_meter = meter.replace('\n', '')
                pair._meter = prosody.pretty_scansion([m for m in clean_meter])
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

# COMPILE AND ACCESS DATA FOR ENTIRE PLAY

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
            for p in self.pairs:
                matched_circ_count += p.secure_circ_match_count
                all_match_count += p.secure_match_count
                matched_peak_count += p.secure_matched_peak_count
                compatible_count += p.secure_compatible_count
                syl_count += p.secure_syl_count
                peak_count+= p.secure_peak_count
                circ_count+= p.secure_circ_count
                str_circ_count+= p.secure_str_circ_count
                ant_circ_count+= p.secure_ant_circ_count
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
    

# DISPLAY DATA FOR THE PLAY AND ITS PAIRS
    
    def display (self):
        """Compiles data for all the syllables in a whole play."""
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
        for p in self.pairs:
            print(template.format(p.name, 
                                  display_percent(p.secure_compatible_percentage),
                                  display_percent(p.secure_match_percentage),
                                  display_percent(p.secure_matches_per_peaks),
                                  display_percent(p.secure_circ_percentage),
                                  display_percent(p.secure_str_circ_percentage),
                                  display_percent(p.secure_ant_circ_percentage),
                                  display_percent(p.secure_circ_match_percentage)))

## DATA SUMMARIES (for graphing or passing up the chain)

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
    
    def all_pairs_data (self, headings=True):
        data = [p.pair_data for p in self.pairs]
        if headings:
            data.insert(0, self.HEADINGS)
        return data
    
    def play_data (self, headings=True):
        data = [self.author,
                self.name,
                "All Pairs",
                self.percent_compatible,
                self.percent_match,
                self.percent_matched_peaks,
                self.percent_circs,
                self.percent_str_circs,
                self.percent_ant_circs,
                self.percent_matched_circ]
        if headings:
            data.insert(0, self.HEADINGS)
        return data
        
    def display_graph (self):
        """Non-functional"""
        for row in self.graph_data():
            pass
        
    def export_graph_csv (self, directory_name=CORPUS_DIR, short_name=False):
        """Non-functional"""
        with open(directory_name+self.name+'-graphdata.csv', "w", encoding='utf-8') as output:
            for row in self.graph_data():
                row_text = ','.join([str(x) for x in row]) + '\n'
                output.write(row_text)
    
    def print_graph_stats (self, stacking=True):
        """Prints onscreen the data to make a csv with a stacked bar graph. 
        I need to add a CSV export option, but don't have time now."""
        
        if stacking:
            print ("Stanza Pair#Matched Circumflexes#Other Matched Accents#Other Compatible Syllables")
            for p in self.pairs:
                circs = p.secure_circ_match_percentage
                other_matched = p.secure_match_percentage - circs
                other_compatible = 1-p.secure_repeat_percentage-other_matched
                print ("#".join([str(n) for n in [p.name, circs, other_matched, other_compatible]]))
                
        else:
            print ("Stanza Pair#Matched Circumflexes#All Matched Accents#All Compatible Syllables")
            for p in self.pairs:
                compatible = 1-p.secure_repeat_percentage
                matched = p.secure_match_percentage
                circs = p.secure_circ_match_percentage
                print ("#".join([str(n) for n in [p.name, circs, matched, compatible]]))
            
        
    def export_stats (self, directory_name=CORPUS_DIR):
        """Exports the play statistics as a .csv file in the specified directory.
        NOTE: I am not updating this for now, on the assumption that data will 
        be exported at the Author level and chunked out from there.
        """
        export_name = self.name
        if export_name.endswith('csv'):
            export_name = export_name[:-4]
        export_name = export_name + '-stats.csv'
        with open(directory_name+export_name, "w", encoding='utf-8') as output:
            Labels = ['Stanza', 'Secure Syl Count', 'Secure Match Count', 'Secure Repeat Count', 'Notes']
            output.write(','.join(Labels) + '\n')
            for i, s in enumerate(self.pairs):
                quoted_notes = "\"" + s.notes + "\""
                row = [s.name, str(s.secure_syl_count), str(s.secure_match_count), str(s.secure_repeat_count), quoted_notes]
                row_text = ','.join(row) + '\n'
                output.write(row_text)
    
    def export_analysis (self, directory_name=CORPUS_DIR, numbers=False):
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
                    if not numbers:
                        attributes = attributes[1:]
                    for a in attributes:
                        items = [str(i).ljust(width) for width, i in zip(widths, a)]
                        output.write(''.join(items)+'\n')
                    total_length = sum(widths)
                    output.write('-'*total_length + '\n')
        print("Added file '{}' to directory '{}'".format(export_name, directory_name))
    
#    def export_analysis_pretty (self, directory_name):
#        """Exports the readable display of the entire play to a text file in the
#        specified directory.
#        """
#        export_name = self.name
#        if export_name.endswith('csv') or export_name.endswith('txt'):
#            export_name = export_name[:-4]
#        export_name = export_name + '-analysis.txt'
#        with open(directory_name+export_name, "w", encoding='utf-8') as output:
#            output.write(self.name + '- Musical Analysis\n')
#            for i, s in enumerate(self.pairs):
#                output.write('\n\n{}. {}\n\n'.format(names[i]))
#                data = s.display_data()
#                for (widths, attributes) in data:
#                    for a in attributes[1:]:
#                        items = [str(i).ljust(width) for width, i in zip(widths, a)]
#                        output.write(''.join(items)+'\n')
#                    total_length = sum(widths)
#                    output.write('-'*total_length + '\n')
#        print("Added file '{}' to directory '{}'".format(export_name, directory_name))
        
    def export_graph_data (self, directory = CORPUS_DIR):
        rows = [['PAIR NAME', 'MATCHED CIRCS', 'OTHER MATCHED ACCENTS', 'OTHER NON-REPEAT', 'ALL MATCHED', 'ALL COMPATIBLE']]
        for pair in self.pairs:
            name = re.sub(r'^\w+-', '', pair.name)
            circ_match = pair.secure_circ_match_percentage
            other_match = (pair.secure_match_percentage - circ_match)
            other_non_repeat = (1 - pair.secure_repeat_percentage) - (circ_match +other_match)
            all_matched = pair.secure_match_percentage
            all_compatible = 1 - pair.secure_repeat_percentage
            rows.append([name, circ_match, other_match, other_non_repeat, all_matched, all_compatible])
        with open(directory+self.name+'-graphdata.csv', "w", encoding='utf-8') as output:
            for row in rows:
                row_text = ','.join([str(x) for x in row]) + '\n'
                output.write(row_text)
        
            
###########################


def load_play (name, csv_name, author='Aeschylus'):
    play = Play(name, csv_name +'.csv', CORPUS_DIR + author +'/', author=author)
    return play

def quick_export_analysis (name, csv_name, author='Aeschylus'):
    play = Play(name, csv_name +'.csv', CORPUS_DIR + author +'/')
    play.export_analysis(CORPUS_DIR + author + '/Analyses/')
    return play
