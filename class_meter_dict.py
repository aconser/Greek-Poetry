# -*- coding: utf-8 -*-
"""
CLASS METER_DICT

Compiles statistics extracted from a group of LineGroup objects.

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""
from operator import itemgetter

class Meter_Dict:
    
    def __init__(self, line_groups):
        self.meter_dict = {}
        self._lines = []
        self.add_lines(line_groups)
        self._consolidated = {}

    @property
    def corrupt (self):
        return any(l.corrupt for l in self._lines)
    
    def add_lines (self, line_groups):        
        for l in line_groups:
            meter = ''.join(l.meter) #translate list into string
            if meter in self.meter_dict:
                self.meter_dict[meter].append(l.stats)
            else:
                self.meter_dict[meter] = [l.stats]
        self._lines.extend(line_groups)
        self._consolidated =  {}
    
    @property
    def consolidated (self):
        if not self._consolidated:
            consolidated = {}
            for key, entries in self.meter_dict.items():
                count = len(entries)
                match_av = sum([match for match, repeat in entries])/count
                repeat_av = sum([repeat for match, repeat in entries])/count
                consolidated [key] = (count, match_av, repeat_av)
            self._consolidated = consolidated
        return self._consolidated
            
    def most_common (self, top=10):
        tuples = [(key, entry[0]) for key, entry in self.consolidated.items()]
        tuples.sort(key=itemgetter(1))
        return tuples[:top]
    
    def most_matches (self, top=10):
        tuples = [(key, entry[1], entry[0]) for key, entry in self.consolidated.items()]
        tuples.sort(key=itemgetter(1), reverse=True)
        return tuples[:top]
            
    def most_repeats (self, top=10):
        tuples = [(key, entry[2], entry[0]) for key, entry in self.consolidated.items()]
        tuples.sort(key=itemgetter(1))
        return tuples[:top]
    

