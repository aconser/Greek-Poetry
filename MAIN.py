# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 15:13:35 2018

@author: Anna
"""

#%%
from Analysis.class_play import Play
#%%
### PROSE CONTROL (LYSIAS)
l_directory = '..//Corpus/Control/'
l_file = 'Lysias.csv'
Lysias = Play('Lysias', l_file, l_directory)
Lysias.display()

# MATCH %  :  5
# REPEAT % : 26
#%%
### TRIMETER CONTROL (ANTIGONE)
t_directory = '..//Corpus/Control/'
t_file = 'Soph-Ant-trimeter.csv'
T = Play('trimeter', t_file, t_directory)
T.display()
# MATCH %  :  8
# REPEAT % : 23
#%%
### ANTIGONE
s_directory = '..//Corpus/Sophocles/'
s_file = 'Soph-Ant.csv'
Antigone = Play('Antigone', s_file, s_directory)
Antigone.display()

# MATCH %  :  12
# REPEAT % : 17
#%%
### AGAMEMNON
A_directory = '..//Corpus/Aeschylus/'
Ag_file = 'Aesch-Ag.csv'
Ag = Play('Agamemnon', Ag_file, A_directory)
Ag.display()

# MATCH %  :  11
# REPEAT % : 19
#%%
### ALL AESCHYLUS
from os import listdir
A_directory = '..//Corpus/Aeschylus/'
file_list = listdir(A_directory)
play_list = []
for file in file_list:
    print('Adding {} to list'.format(file))
    p = Play(file[6:-4], file, A_directory)
    play_list.append(p)

#%%
for p in play_list[:3]:
    p.display()
#%%
for p in play_list[3:]:
    p.display()
    
#Ag: 11 / 19
#Eu: 12 / 17
#Li: 13 / 17
#PB: 14 / 16
#Pe: 10 / 21
#Se: 9 / 21
#Su: 11 / 20

#%%
#TOTALS for AESCHYLUS:
match_total = 0
repeat_total = 0
syl_count = 0
for p in play_list:
    print(p.name)
    p.add_stats()
    match_total += p.M1
    repeat_total += p.repeat_count
    syl_count += p.syl_count
    print(match_total)
    print(repeat_total)
    print(syl_count)
    print(p.syl_count)
    print()
match_average = int(match_total/syl_count * 100)
repeat_average = int(repeat_total/syl_count * 100)
print('Average Percent Match: ' + str(match_average))
print('Average Percent Repetition: ' + str(repeat_average))

# MATCH %  :  11
# REPEAT % : 19


#%%
# Euripides, Heracles
from Analysis.class_play import Play
E_directory = '..//Corpus/Euripides/'
Heracles = Play('Heracles', 'Eur-Her-NEW.csv', E_directory)
Heracles.export_analysis(E_directory)
#%%
rows = []    
for play in play_list:
    play.add_stats()
    for p in play.pairs:
        stanza_name = p.name
        row = [play.name, stanza_name, p.syl_count, (p.M1/p.syl_count), (p.repeat_count/p.syl_count)]
        rows.append(row)
with open('..//Corpus/'+'Aeschylus'+'-graphdata.csv', "w", encoding='utf-8') as output:
    for row in rows:
        row_text = ','.join([str(x) for x in row]) + '\n'
        output.write(row_text)