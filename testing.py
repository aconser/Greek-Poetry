# -*- coding: utf-8 -*-
"""
Created on Wed May 30 17:17:37 2018

@author: Anna
"""
#%%
reload (CSyl)
reload(CW)
reload(GP)
reload(CS)
reload(SG)
reload(CP)

Agamemnon = CP.load_play('Agamemnon', 'Aesch-Ag')

stanza = Agamemnon.pairs[0]

#for p in Agamemnon.pairs:
#    print(p.word_tag_stats('cap'))
#    print(', '.join( [w.text for w in p.tagged_words('cap')] ))

#%%
Agamemnon.word_tag_analysis('cap')

#print([w.text for w in Agamemnon.tagged_words('proclitic')])

# EXCLUDE CORRUPT WORDS
