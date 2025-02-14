# -*- coding: utf-8 -*-
"""
SCANNER

This program takes a line of Greek text, breaks it into syllables and returns
the scansion as a list of syllable markers: 
    LONG ('L'), SHORT ('S'), or UNKNOWN ('X').  
The module is appropriate for analyzing prose or poetry.

The Scanner module loads a Scansion_Dictionary and uses it to mark ambiguous
vowels to the extent possible.

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""

#%%
    
import scansion_dict as SD
import trimeter as ST
from characters import basic_chars
from syllables import get_syllables
from prosody import get_prosody, pretty_scansion

class Scanner:
    def __init__ (self, lunate=False):
        self.lunate = lunate
        self.dict = SD.Load_Dictionary()
        
    def scan (self, text):
        marked = self.dict.mark_length(text, lunate=self.lunate)
        return get_prosody(marked)
    
    def display_scansion (self, text):
        lines = text.splitlines()
        marked = [self.dict.mark_length(l, lunate=self.lunate) for l in lines]
        syllables = [get_syllables(m) for m in marked]
        scansion = [pretty_scansion(get_prosody(m)) for m in marked]
        for syls, scan in zip(syllables, scansion):
            widths = [len(basic_chars(s)) for s in syls]
            format_scan = [m.center(width) for m, width in zip(scan, widths)]
            print(''.join(format_scan))
            print(''.join(syls))
            
    def scan_trimeter(self, text):
        marked = self.dict.mark_length(text, lunate=self.lunate)
        return ST.scan_trimeter(marked)
            

#%%
################################################
# TESTING
################################################

def scanner_test():
    stanza = """θεοὺϲ μὲν αἰτῶ τῶνδʼ ἀπαλλαγὴν πόνων,
φρουρᾶϲ ἐτείαϲ μῆκοϲ, ἣν κοιμώμενοϲ
ϲτέγαιϲ Ἀτρειδῶν ἄγκαθεν, κυνὸϲ δίκην,
ἄϲτρων κάτοιδα νυκτέρων ὁμήγυριν
καὶ τοὺϲ φέρονταϲ χεῖμα καὶ θέροϲ βροτοῖϲ
λαμπροὺϲ δυνάϲταϲ, ἐμπρέπονταϲ αἰθέρι
ἀϲτέραϲ, ὅταν φθίνωϲιν ἀντολαῖϲ τε τῶν·
καὶ νῦν φυλάϲϲω λαμπάδοϲ τὸ ϲύμβολον,
αὐγὴν πυρὸϲ φέρουϲαν ἐκ Τροίαϲ φάτιν
ἁλώϲιμόν τε βάξιν· ὧδε γὰρ κρατεῖ
γυναικὸϲ ἀνδρόβουλον ἐλπίζον κέαρ·
εὖτʼ ἂν δὲ νυκτίπλαγκτον ἔνδροϲόν τʼ ἔχω
εὐνὴν ὀνείροιϲ οὐκ ἐπιϲκοπουμένην
ἐμήν· φόβοϲ γὰρ ἀνθʼ ὕπνου παραϲτατεῖ,
τὸ μὴ βεβαίωϲ βλέφαρα ϲυμβαλεῖν ὕπνωι·
ὅταν δʼ ἀείδειν ἢ μινύρεϲθαι δοκῶ,
ὕπνου τόδʼ ἀντίμολπον ἐντέμνων ἄκοϲ,
κλαίω τότʼ οἴκου τοῦδε ϲυμφορὰν ϲτένων
οὐχ ὡϲ τὰ πρόϲθʼ ἄριϲτα διαπονουμένου."""
    scanner = Scanner()
    scanner.display_scansion(stanza)
    
#%%
