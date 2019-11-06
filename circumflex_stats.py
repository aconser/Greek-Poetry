#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Circumflex Testing in Aeschylus, Agamemnon

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT

This contains a few rough-and-quick tools for analyzing the rate of circumflexes 
in iambic vs. lyric, and comparing the circumflex rates within different stanza pairs.  
I have also created a function to compile word length information, which should 
eventually be broken into its own module.

"""
from Greek_Prosody.accents import count_circs
from Greek_Prosody.syllables import count_syllables
from Greek_Prosody.characters import alnum_syl, basic_chars
from Utilities.stanza_utilities import load_text
from Utilities.stanza_utilities import CORPUS_DIR
import Analysis.class_play as CP
from Analysis.class_word import is_proclitic

def percent_circ(text):
    circs = count_circs(text)
    words = len(text.split())
    return circs/words

def circ_per_syls(stanza):
    circs = count_circs(stanza.raw_text)
    return circs/stanza.syl_count

def pr_per (number, mark=True):
    num = str(int(1000*number)/10)
    if mark:
        num+='%'
    return num

def pair_circs (pair):
    circs= count_circs(pair.strophe.raw_text)+count_circs(pair.antistrophe.raw_text)
    syl_count = count_syllables(pair.strophe.raw_text+'\n'+pair.antistrophe.raw_text)
    return circs/syl_count

def circs_in_play (play, print_all=True, clean_entries=False, exclude=False, str_ant=False):
    clean_name = play.file[:-4]
    full_text = load_text(clean_name+'-CLEAN.txt', CORPUS_DIR+'clean_OCTs/')
    full_circs = count_circs(full_text)
    full_chars = len(full_text)
    full_words = len(full_text.split())
    full_percent = full_circs/full_chars

    if exclude:
        exclusion_list = ['Agamemnon-1-δ-A', 'Agamemnon-5-ζ-B', 'Agamemnon-6-γ']
        pairs = [p for p in play.pairs if p.name not in exclusion_list]
    else:
        pairs = play.pairs
        
    strophes = [pair.strophe.raw_text for pair in pairs]
    antistrophes = [pair.antistrophe.raw_text for pair in pairs]
    
    strophe_circs = sum([count_circs(s) for s in strophes])
    strophe_chars = sum([len(s) for s in strophes])
    strophe_words = sum([len(s.split()) for s in strophes])
    
    antistrophe_circs = sum([count_circs(a) for a in antistrophes])
    antistrophe_chars = sum([len(a) for a in antistrophes])
    antistrophe_words = sum([len(a.split()) for a in antistrophes])
    
    str_syl_count = sum([count_syllables(p.strophe.raw_text) for p in pairs])
    ant_syl_count = sum([count_syllables(p.antistrophe.raw_text) for p in pairs])
    song_syl_count = str_syl_count + ant_syl_count
    full_syl_count = count_syllables(full_text)
    
    song_circs = strophe_circs+antistrophe_circs
    song_words = strophe_words+antistrophe_words
    song_percent = song_circs/song_words
    
    prose_circs = full_circs-song_circs
    prose_words = full_words-song_words
    prose_percent = prose_circs/prose_words
    
    full_per_syl = full_circs/full_syl_count
    song_per_syl = song_circs/song_syl_count
    str_per_syl = strophe_circs/str_syl_count
    ant_per_syl = antistrophe_circs/ant_syl_count

    if not clean_entries:
        print()
        print(play.name)
        print()
        print('Full text:\t' + pr_per(full_per_syl, mark=True))
        print('Strophic pairs:\t' + pr_per(song_per_syl, mark=True))
        print('  Str: ' + pr_per(str_per_syl, mark=True))
        print('  Ant: ' + pr_per(ant_per_syl, mark=True))
        
    if print_all:
        for pair in pairs:
            Stanza_p = pair_circs(pair)
            entry = pair.name + '#'+ pr_per(Stanza_p, mark=False)
            if (Stanza_p > song_per_syl*1.5):
                entry+='#XX'
            print(entry)
    if str_ant:
        for pair in pairs:
            Stanza_p = pair_circs(pair)
            entry = pair.name + '#'+ pr_per(Stanza_p, mark=False)
            if (Stanza_p > song_per_syl*1.5):
                entry+='#XX'
            print(entry)
    return (full_circs, full_syl_count, song_circs, song_syl_count, strophe_circs, antistrophe_circs)

def Str_Ant_circs (play, diff): 
    print()
    total_str_higher = 0
    total_ant_higher = 0
    for pair in play.pairs:
        St_p = circ_per_syls(pair.strophe)
        An_p = circ_per_syls(pair.antistrophe)
        print(pair.name)
        print('    Str: ' + pr_per(St_p))
        print('    Ant: ' + pr_per(An_p))
        print('     ?syls?: {}'.format(pair.total_syl_count))
        #print('Ratio: ' + str(ratio))
        if (St_p > (An_p*diff)):
            print('                SSS')
            total_str_higher += pair.total_syl_count
        elif (An_p > (St_p*diff)):
            print('                AAA')
            total_ant_higher += pair.total_syl_count
    print()
    print('Total syls in str-weighted pairs: {}'.format(total_str_higher))
    print('Total syls in ant-weighted pairs: {}'.format(total_ant_higher))
     
     
def all_circ_data(Author, print_all=False, clean_entries=False, str_ant=False):
    total_full_syl_count = 0
    total_full_circs = 0
    total_song_syl_count = 0
    total_song_circs = 0
    total_str_circs = 0
    total_ant_circs =0
    
    print("Circumflexes/Syllable in the plays of {}".format(Author.name))
    for play in Author.plays[:-1]:     #EXCLUDING PROMETHEUS
        stats = circs_in_play(play, print_all, clean_entries, str_ant)
        (full_circs, full_syl_count, song_circs, song_syl_count, str_circs, ant_circs) = stats
        total_full_syl_count += full_syl_count
        total_full_circs += full_circs
        total_song_syl_count += song_syl_count
        total_song_circs += song_circs
        total_str_circs += str_circs
        total_ant_circs += ant_circs
        
        
    total_full_per_syl = total_full_circs/total_full_syl_count
    total_song_per_syl = total_song_circs/total_song_syl_count
    total_str_per_syl = total_str_circs/(total_song_syl_count/2)
    total_ant_per_syl = total_ant_circs/(total_song_syl_count/2)

    print()
    print("TOTAL STATS for {}".format(Author.name))
    print('Full text:\t' + pr_per(total_full_per_syl))
    print('Strophic Pairs:\t' + pr_per(total_song_per_syl))
    print('  Str: ' + pr_per(total_str_per_syl))
    print('  Ant: ' + pr_per(total_ant_per_syl))

#%%
def get_lines(play, position, len_limit):
    lines = []
    for p in play.pairs:
        if len(p.lines) > len_limit:     # exclude short stanzas
            lines.append(p.lines[position])
    return lines

def circs_in_line(play, position, len_limit=3):
    lines = get_lines(play, position, len_limit)
    str_circs = 0
    ant_circs = 0
    str_syls = 0
    ant_syls = 0
    for l in lines:
        str_circs += count_circs(l.texts[0])
        ant_circs += count_circs(l.texts[1])
        str_syls += count_syllables(l.texts[0])
        ant_syls += count_syllables(l.texts[1])
    
    total_circs = str_circs+ant_circs
    total_syls = str_syls+ant_syls
    
    str_percent = str_circs/str_syls
    ant_percent = ant_circs/ant_syls
    total_percent = total_circs/total_syls
    print('Str: {}'.format(str_percent))
    print('Ant: {}'.format(ant_percent))
    print('Total: {}'.format(total_percent))
    return (total_circs, total_syls, str_circs, ant_circs, str_syls, ant_syls)
    
def lines_in_author (author, position):
    total_all_circs = 0
    total_all_syls = 0
    total_str_circs = 0
    total_ant_circs = 0
    total_str_syls = 0
    total_ant_syls = 0
    for p in author.plays[:-1]:  #Exclude Prometheus
        print()
        print(p.name)
        all_circs, all_syls, str_circs, ant_circs, str_syls, ant_syls = circs_in_line(p, position)
        total_all_circs += all_circs
        total_all_syls += all_syls
        total_str_circs += str_circs
        total_str_syls += str_syls
        total_ant_circs += ant_circs
        total_ant_syls += ant_syls
        print
    print()
    print('TOTAL: {}'.format(total_all_circs/total_all_syls))
    print('Total Str: {}'.format(total_str_circs/total_str_syls))
    print('Total Ant: {}'.format(total_ant_circs/total_ant_syls))
    
        
        
        
        
#%%
def word_length (play, char_len, print_short=False):
    """Compiles and displays data comparing word lengths between the full text
    and strophic pairs of a tragedy.  This is functional, but not super accurate,
    because the OCT text has not been stripped of character names and str/an
    markers, which inflate the numbers for short (unaccented) words. The tools 
    for stripping these are in Utilities.reformat_csv_files (not the best place!), 
    but I don't want to spend time on this now.
    
    Parameters: 
        play is a Play object
        char_len is the character length cutoff defining 'long words' (int)
    """
    
    clean_name = play.file[:-4]
    full_text = load_text(clean_name+'-CLEAN.txt', CORPUS_DIR+'clean_OCTs/')
    lyric_text = ( '\n'.join([pair.strophe.raw_text for pair in play.pairs]) + 
                  '\n'.join([pair.antistrophe.raw_text for pair in play.pairs])
                  )
    full_words = [t for t in [alnum_syl(basic_chars(w)) for w in full_text.split()] if t]
    lyric_words = [t for t in [alnum_syl(basic_chars(w)) for w in lyric_text.split()] if t]
    full_mean = sum([len(w) for w in full_words])/len(full_words)
    lyric_mean = sum([len(w) for w in lyric_words])/len(lyric_words)
    print()
    print('Mean word lengths')
    print('Full text: {}'.format(full_mean))
    print('Lyric text: {}'.format(lyric_mean))
    
    full_big_words = [w for w in full_words if len(w)>char_len]
    lyric_big_words = [w for w in lyric_words if len(w)>char_len]
    full_big_rate = len(full_big_words)/len(full_words)
    lyric_big_rate = len(lyric_big_words)/len(lyric_words)
    full_big_mean = sum([len(w) for w in full_big_words])/len(full_big_words)
    lyric_big_mean = sum([len(w) for w in lyric_big_words])/len(lyric_big_words)
    
    print()
    print('Big word rates: Percent >{} char'.format(char_len))
    print('Full text: {}'.format(full_big_rate))
    print('Lyric text: {}'.format(lyric_big_rate))
    print()
    print('BIG mean word lengths')
    print('Full text: {}'.format(full_big_mean))
    print('Lyric text: {}'.format(lyric_big_mean))
    
    if print_short:
        full_short_words = [w for w in full_words if len(w)<(char_len+1)]
        print()
        print('Full words <= {} chars'.format(char_len))
        print(', '.join(full_short_words))
    
def bare_words (text):
    return [t for t in [alnum_syl(basic_chars(w)) for w in text.split()] if t]

def mean_len (word_list):
    return sum([len(w) for w in word_list])/len(word_list)

def big_words (word_list, char_len):
    return [w for w in word_list if len(w)>char_len]

def percent_big (text, char_len):
    words = bare_words(text)
    bigs = big_words(words, char_len)
    return len(bigs)/len(words)

def mean_word_len (text):
    words = bare_words(text)
    return mean_len(words)

def percent_proclitic (text):
    words = text.split()
    proclitics = [w for w in words if is_proclitic(w)]
    print (proclitics)
    return len(proclitics)/len(words)


#%%
        
# As a control for iambics, this is the Prologue (Ag. 1-39). 
# Line 25 (the exclamation ἰοὺ ἰού·') should be removed if I want only trimeter.
        
WATCHMAN = """θεοὺϲ μὲν αἰτῶ τῶνδʼ ἀπαλλαγὴν πόνων,
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
οὐχ ὡϲ τὰ πρόϲθʼ ἄριϲτα διαπονουμένου.
νῦν δʼ εὐτυχὴϲ γένοιτʼ ἀπαλλαγὴ πόνων
εὐαγγέλου φανέντοϲ ὀρφναίου πυρόϲ.
ὦ χαῖρε λαμπτὴρ νυκτόϲ, ἡμερήϲιον
φάοϲ πιφαύϲκων καὶ χορῶν κατάϲταϲιν
πολλῶν ἐν Ἄργει τῆϲδε ϲυμφορᾶϲ χάριν.
ἰοὺ ἰού·
Ἀγαμέμνονοϲ γυναικὶ ϲημαίνω τορῶϲ
εὐνῆϲ ἐπαντείλαϲαν ὡϲ τάχοϲ δόμοιϲ
ὀλολυγμὸν εὐφημοῦντα τῆιδε λαμπάδι
ἐπορθιάζειν, εἴπερ Ἰλίου πόλιϲ
ἑάλωκεν, ὡϲ ὁ φρυκτὸϲ ἀγγέλλων πρέπει·
αὐτόϲ τʼ ἔγωγε φροίμιον χορεύϲομαι,
τὰ δεϲποτῶν γὰρ εὖ πεϲόντα θήϲομαι
τρὶϲ ἓξ βαλούϲηϲ τῆϲδέ μοι φρυκτωρίαϲ·
γένοιτο δʼ οὖν μολόντοϲ εὐφιλῆ χέρα
ἄνακτοϲ οἴκων τῆιδε βαϲτάϲαι χερί.
τὰ δʼ ἄλλα ϲιγῶ· βοῦϲ ἐπὶ γλώϲϲηι μέγαϲ
βέβηκεν· οἶκοϲ δʼ αὐτόϲ, εἰ φθογγὴν λάβοι,
ϲαφέϲτατʼ ἂν λέξειεν· ὡϲ ἑκὼν ἐγὼ
μαθοῦϲιν αὐδῶ κοὐ μαθοῦϲι λήθομαι.
"""
def trim_control ():
    circs = count_circs(WATCHMAN)
    syls = count_syllables(WATCHMAN)
    return circs/syls

