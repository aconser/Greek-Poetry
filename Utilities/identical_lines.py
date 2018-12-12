#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIND IDENTICAL LINES
This tool checks for identical lines, and prints a summary.  
Note that this only works for groups of TWO, not polystrophic situations.
This was used to identify locations in the texts, which were then manually marked
with '@' in the csv spreadsheets.

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT@author: anna
"""

def find_identical_lines (stanza_group):
    
    for line_group in stanza_group.lines:
        found_identical = False
        if lines_identical(line_group):
            if not found_identical:
                print()
                print(stanza_group.name)
                found_identical = True
            print(line_group.texts)
        
def lines_identical (line_group):
    PUNCTUATION = ".,;·:'<>[]{}()=+\u037e\u0387\u00B7⟨⟩†—@"
    text_1, text_2 = line_group.texts
    list_1 = [ch for ch in text_1 if not(ch.isspace() or ch in PUNCTUATION)]
    list_2 = [ch for ch in text_2 if not(ch.isspace() or ch in PUNCTUATION)]
    return list_1 == list_2

def check_play(play):
    for pair in play.pairs:
        find_identical_lines(pair)

def check_author(author):
    for play in author.plays:
        check_play(play)