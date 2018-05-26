# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:45:02 2018

@author: Anna
"""
#%%
import class_play as CP
import class_StanzaGroup as SG
from importlib import reload

A_directory = '..//Corpus/Aeschylus/'
Ag_file = 'Aesch-Ag.csv'
Ag = CP.Play('Agamemnon', Ag_file, A_directory)

#%%
total = 0
cap_contours = []
for pair in Ag.pairs:
    for i, tags in enumerate(pair.syl_tags):
        if 'cap' in tags:
            total += 1
            cap_contours.append(pair.contours[i])
            
#%%
percent_clash = len([s for s in cap_contours if s == '=']) / total
print ( "Clash: {}%".format(percent_clash) )

percent_match = len([s for s in cap_contours if s == 'DN-A']) / total
print ( "Match: {}%".format(percent_match) )

#%%
cap_words = []
for pair in Ag.pairs:
    for i, tags in enumerate(pair.syl_tags):
        if 'cap' in tags:
            cap_words.append([s.syllables[i].word for s in pair.stanzas])

#%%
repeats = []
matched = []
for i, s in enumerate(cap_words):
    if cap_contours[i] == '=':
        repeats.append(s)
    else:
        matched.append(s)

#%%
real_matched = []
for w in matched:
    if w not in repeats:
        real_matched.append(w)
#%%
def check_cap_effect (stanza):
    cap = []
    not_cap = []
    for i, tags in enumerate(stanza.syl_tags):
        if not stanza.corrupt_list[i]:
            if 'cap' in tags:
                cap.append(stanza.contours[i])
            else:
                not_cap.append(stanza.contours[i])
    word_list = []
    for s in stanza.stanzas:
        word_list.extend([w.text for w in s.words if 'cap' in w.tags])
        word_list.append('/')
    if cap:
        cap_repeat_perc = len([s for s in cap if s == '=']) / len(cap)
        not_cap_repeat_perc = len([s for s in not_cap if s == '=']) / len(not_cap)
        print(stanza.name)
        print('Overall rep percent: {}%'.format(int(stanza.repeat_percentage*100)))
        print('Capitalized rep percent: {}%'.format(int(cap_repeat_perc*100)))
        print('Rep percent excluding Cap: {}%'.format(int(not_cap_repeat_perc*100)))
        print()
        print('Cap syl count: {}'.format(len(cap)))
        print(word_list)
        print()
        print()
    else:
        print(stanza.name)
        print('No capitalized words')
        print()
        