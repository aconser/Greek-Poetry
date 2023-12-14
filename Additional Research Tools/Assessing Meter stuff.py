#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT

Planning:
    
Add scansion for all of Aeschylus

Build a list of all lines in Aeschylus (excluding corruption)
-- Pickle this?  Export as CSV file?

Build a list of most common line meters in Aeschylus (excluding corruption)

Check accentual responsion by line type

Check accentual responsion between responding lines vs. non-responding lines.

Methodology:
- don't allow for meter crossing line breaks. This increases sample size, but 
could reduce reliability since colometry is based on where word breaks align 
between stanzas.
- choose the top 10 most common line types in Aeschylus.
- exclude any lines with corruption

"""

import Analysis.class_author as CA
A = CA.Author('Aeschylus')
for p in A.plays:
    print (p.name)
    print (p.pairs[0].meter[:20])