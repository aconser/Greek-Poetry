# -*- coding: utf-8 -*-
"""
Created on Wed May 30 17:17:37 2018

@author: Anna
"""
#%%
from importlib import reload
import Analysis.class_StanzaGroup as SG
import Analysis.class_line as CL
import Analysis.class_play as CP
import Analysis.class_stanza as CS
import Analysis.class_syllable as CSyl
import Analysis.class_word as CW
import class_meter_dict as MD



#%%

reload (CSyl)
reload (CL)
reload(CW)
#reload(GP)
reload(CS)
reload(SG)
reload(MD)
reload(CP)


Antigone = CP.load_play('Antigone', 'Soph-Ant', author='Sophocles')

stanza = Antigone.pairs[0]

lines = [l for s in Antigone.pairs for l in s.lines]
md = MD.Meter_Dict(lines)
#%%
md.most_matches(top=20)

#for p in Agamemnon.pairs:
#    print(p.word_tag_stats('cap'))
#    print(', '.join( [w.text for w in p.tagged_words('cap')] ))

 #%%
Agamemnon.word_tag_analysis('cap')

#print([w.text for w in Agamemnon.tagged_words('proclitic')])

# EXCLUDE CORRUPT WORDS
