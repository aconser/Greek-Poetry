# -*- coding: utf-8 -*-
"""
Created on Thu May 10 13:09:38 2018

@author: Anna
"""

from class_play import Play
from class_StanzaGroup import StanzaGroup
E_directory = '..//Corpus/Euripides/'
Heracles = Play('Heracles', 'Eur-Her-NEW.csv', E_directory)
#%%
#
#A = Heracles.pairs[2].strophe
#B = Heracles.pairs[2].antistrophe
#C = Heracles.pairs[4].strophe
#D = Heracles.pairs[4].antistrophe
#E = Heracles.pairs[6].strophe
#F = Heracles.pairs[6].antistrophe

from class_stanza import Stanza
A = Stanza('Mes A', """πρῶτον μὲν Διὸϲ ἄλϲοϲ
ἠρήμωϲε λέοντοϲ,
πυρϲῶι δʼ ἀμφεκαλύφθη
$$$$$$$
ξανθὸν κρᾶτʼ ἐπινωτίϲαϲ
δεινοῦ χάϲματι θηρόϲ.""")
B = Stanza('Ep A', """τάν τε χρυϲοκάρανον
δόρκα ποικιλόνωτον
ϲυλήτειραν ἀγρωϲτᾶν
$$$$$$$
κτείναϲ θηροφόνον θεὰν
Οἰνωᾶτιν ἀγάλλει.""")
C = Stanza('Mes B', """ἄν τε Μηλιάδʼ ἀκτὰν
Ἀναύρου παρὰ παγὰϲ
Κύκνον ξεινοδαΐκταν
$$$$$$$
τόξοιϲ ὤλεϲεν, Ἀμφαναί–
αϲ οἰκήτορʼ ἄμεικτον.""")
D = Stanza('Ep B', """οὐρανοῦ θʼ ὑπὸ μέϲϲαν
ἐλαύνει χέραϲ ἕδραν,
Ἄτλαντοϲ δόμον ἐλθών,
$$$$$$$
ἀϲτρωπούϲ τε κατέϲχεν οἴ–
κουϲ εὐανορίαι θε|ῶν.""")
E = Stanza('Mes G', """τάν τε μυριόκρανον
πο|λύφονον κύνα Λέρνεϲ
ὕδραν ἐξεπύρωϲεν,
βέ|λεϲί τʼ ἀμφέβαλʼ⟨ἰόν⟩,
τὸν τριϲώματον οἷϲιν ἔ–
κτα βοτῆρʼ Ἐρυθείαϲ.""")
F = Stanza('Ep G', """εἰ δʼ ἐγὼ ϲθένοϲ ἥβων
δό|ρυ τʼ ἔπαλλον ἐν αἰχμᾶι
Καδμείων τε ϲύνηβοι,
τέ|κεϲιν ἂν προπαρέϲταν
ἀλκᾶι· νῦν δʼ ἀπολείπομαι
τᾶϲ εὐδαίμονοϲ ἥβαϲ.""")

stanza_list = [A, B, C, D, E, F]

raw_meter = """
LXLSSLL
RXLSSLL
LLLSSLL
RXLSSLL
LXLSSLSL
LXLSSLL
"""

meter = [ch for ch in raw_meter if ch !='\n']

#for s in stanza_list:
#    s.meter = meter
#%%    
from class_StanzaGroup import StanzaGroup
Refrain = StanzaGroup('Stasimon 1 Refrain', stanza_list)
Refrain.meter = meter
Refrain.display_readable()
