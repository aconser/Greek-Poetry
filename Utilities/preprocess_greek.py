# -*- coding: utf-8 -*-
"""
FILL GREEK ELISIONS

This program contains tools for completing Greek words ending with elisions 
(marked with an apostrophe), so that they can be processed by a lemmatizer. The
current version will not allow for parsing, as it simply aims to produce a valid
form of the lemma, without acknowledging competing variants (e.g. -ατο vs. -ατε).

Endings are completed in the following steps:
    1. Commonly elided words are identified and replaced (replace_dict)
    2. Remaining words are completed based on their final letters (ending_dict)
    3. All remaining words are ended with epsilon

Next steps for improvement:
I developed the lists of predicted completions by looking at the ellided forms
in Euripides' Orestes. The function "extract ellisions" included in this file
will helpfully extract ellided words and sort them according to their ending.
The lists of predicted completions would be greatly improved by analyzing more 
texts and identifying the (many) errors and omissions.

Eventually, it would be better to use machine learning to build a more complete
(and empirically tested) list of completion predictions. I imagine this could 
be done by searching a large corpus for instances of the ellided string with 
the addition of [ειαο] (taking into account roughening of π, κ, and τ).

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT

"""
import re

# List of commonly elided words, to be replaced whole. Note that these do not
# need to be in any special order, since they must be a precise match.
# It would be good to make the list more systematic. though....
replace_dict = {'τ' : 'τε',
                'θ' : 'τε',
                'δ' : 'δέ',
                'γ' : 'γε',
                'μ' : 'με',
                'δι' : 'δια',
                'ἀπ' : 'ἀπό', #REVISION
                'ἀφ' : 'ἀπό', #REVISION
                'παρ' : 'παρά',
                'ἀμφ' : 'ἀμφί',
                'ἐπ' : 'ἐπί',
                'ἐφ' : 'ἐπί',                
                'μετ' : 'μετά',
                'μεθ' : 'μετά',
                'ὑπ' : 'ὑπο',
                'ὑφ' : 'ὑπο',
                'κατ' : 'κατά',
                'καθ' : 'κατά',
                'ἀν' : 'ἀνά',
                'ἀλλ' : 'ἁλλά',
                'ἄλλ' : 'ἄλλα',
                'ὅσ' : 'ὅσα',
                'σ' : 'σε',
                'ἐνθάδ' : 'ἐνθάδε',
                'λέγ' : 'λέγε',
                'μέγ' : 'μέγα',
                'τάδ' : 'τάδε',
                'τοῦτ' : 'τοῦτο',
                #'τῆιδ' : 'τῆιδε', # to avoid 'ιδα’ replacements, but accent is different
                #'τῶιδ' : 'τῶιδε',
                #'αἵδ' : 'αἵδε',
                #'οἶδ' : 'οἶδε',
                'Ἑλλάδ' : 'Ἑλλάδα',
                'παῖδ' : 'παῖδα', # Ambiguous
                'φροῦδ' : 'φροῦδα',
                'ἔπειθ' : 'ἔπειτα',
                'ἔνθ' : 'ἔνθα',
                'ποτ' : 'ποτε',
                'ποθ' : 'ποτε',
                'αὔθ' : 'αὔτε',
                'οὐκέθ' : 'οὐκέτι',
                'ταῦθ' : 'ταῦτα',
                'ἐνταῦθ' : 'ἐνταῦθα',
                'τοῦθ' : 'τοῦτο',
                'οὕνεκ' : 'οὕνεκα',
                'ἡνίκ' : 'ἡνίκα',
                'αὐτίκ' : 'αὐτίκα',
                'μάλ' : 'μάλα',
                'κἄμ' : 'κἄμε',
                'ἔμ' : 'ἔμε',
                'ἵν' : 'ἵνα',
                'μέν' : 'μένε',
                'τίν' : 'τίνα',
                'ἄρ' : 'ἄρα',
                'ἆρ' : 'ἆρα','δεῦρ' : 'δεῦρο',
                'ἔπειτ' : 'ἔπειτα',
                'τότ' : 'τότε',
                'ἐϲτ' : 'ἐϲτι',
                'ὥϲτ' : 'ὥϲτε',
                'ἔτ' : 'ἔτι',
                'ὅτ' : 'ὅτε',
                'οὐκέτ' : 'οὐκέτι',
                'δῆτ' : 'δῆτα',
                'τοῦτ' : 'τοῦτο',
                'ϲάφ' : 'ϲάφα',
                'οὕνεχ' : 'οὕνεκα',
                'εἷ' : 'εἷα',
                'οὖσ' : 'οὖσα',
                'ϲτιν' : 'ἐϲτιν',  # I'm not sure if these proelisions will process
                'γώ' : 'ἐγώ',
                'γὼ' : 'ἐγώ'
                }

# List of endings and the predicted completion. This was made by human estimation.
# Note that the longer (more precise) endings (e.g. -οιμ : -οιμι) must come 
# first in the list, so that they aren't preempted by the broader patterns 
# (e.g. -μ : -μα). 
# Endings typically followed by epsilon are omitted, as that is the default.
ending_dict = {'ουσ' : 'ουσι',
                 'οῦσ' : 'οῦσι',
                 'ῶσ' : 'ῶσι',  
                 'αιμ' : 'αιμι',
                 'οιμ' : 'οιμι',
                 'οῖμ' : 'οῖμι',
                 'οιτ' : 'οιτο', #Would epsilon be just as good here?
                 'αιτ' : 'αιτο',
                 'αιθ' : 'αιτο',
                 'ιϲτ' : 'ιϲτα',
                 'αῦτ' : 'αῦτα',
                 'εῖσ' : 'εῖσα',               
                 'μεθ' : 'μεθα',
                 'μεϲθ' : 'μεϲθα',
                 'τιν' : 'τινα',
                 'ίημ' : 'ίημι',
                 'ματ' : 'ματα',
                 'μαθ' : 'μαθα',
                 'δέκ' : 'δέκα',
                 'ντ' : 'ντα', #Could also be dative, dual OR VERB (-οντο)
                 'νθ' : 'ντα',
                 'ίδ' : 'ίδα', # Acute accent is key (e.g. ἐλπίδα)        
                 'οσ' : 'οσι', # some dative plurals
                 'ασ' : 'ασι', # This should catch aorist participles (as dat pl) and perfect verbs.
                 'ι' : 'ια',
                 'ί' : 'ία',
                 'μ' : 'μα',
                 'ν' : 'να',
                 'ρ' : 'ρα',
                 }

ELISION_MARK = 'ʼ' # U+02BC
PUNCTUATION = r',.;·?!\'\"\)\]\(\['
PUNCTUATION_RE = re.compile(r'[,.;·?!\'\"\)\]\(\[]')

#%%
                           
def standardize_sigmas (text, lunate=False):
    """Standardizes sigma characters within a string of text.  Word 
    internal sigma is 'σ'; word final sigma is 'ς'; capital sigma is Σ.  
    If the lunate flag is set to True, then all sigmas are set to 'ϲ' / 'Ϲ'. 
    (Lunate sigmas are standard in the OCT texts).
    
    :param str text: a string of greek text
    :return str t: a copy of the string with the sigmas standardized.
    """
    
    if lunate==True:
        t = re.sub(r'[σς]', r'ϲ', text)
        t = re.sub('Σ', 'Ϲ', t)        
    else:
        t = re.sub('ϲ', 'σ', text)
        t = re.sub('Ϲ', 'Σ', t)
        t = re.sub(r'σ\b', r'ς', t)
        return t

def fill_elisions (string):
    """Replaces all the elided words in a text with (guessed) complete forms.
    
    :param str string: a passage of greek text
    :return str text: a version of the passage with the elided forms completed.
    """
    #Standardize Sigmas
    text = standardize_sigmas(string)
    #Replace commonly elided words
    for old, new in replace_dict.items():               
        old_re = re.compile(r'\b' + old + ELISION_MARK)
        text = old_re.sub(new, text)
    #Complete remaining elisions based on ending 
    for old, new in ending_dict.items():
        old_re = re.compile(r'\B' + old + ELISION_MARK)
        text = old_re.sub(new, text)
    #Complete remaining elisions with an epsilon 
    text = re.sub(ELISION_MARK, 'ε', text)
    return text

def fill_elided_word (string):
    """Returns the (best-guess) complete form of a given elided word.
    """
    word = string.replace(ELISION_MARK, '')
    #Check for commonly elided words
    if word in replace_dict:
        return replace_dict[word]
    #Check for ending patterns
    for key, entry in replace_dict.items():
        if word.endswith(key):
            return entry
    #Complete unknown forms with epsilon
    return string.replace(ELISION_MARK, 'ε')

def full_word_list (string):
    text = standardize_sigmas(string) #standardize sigmas
    no_punct = PUNCTUATION_RE.sub('', text)
    words = no_punct.split()
    word_list = []
    for w in words:
        if ELISION_MARK in w:
            filled = fill_elided_word(w)
            word_list.append(filled)
        else:
            word_list.append(w)
    return word_list
    
def sorted_elisions (string):
    
    """Tokenizes a text providing the (best guess) full form for elided words.
    Returns a list of words which don't match the original text, but should
    fare better being processed by a lemmatizer.
    """
    text = standardize_sigmas(string) #standardize sigmas
    no_punct = PUNCTUATION_RE.sub('', text)
    words = no_punct.split()
    elisions = [w for w in words if ELISION_MARK in w]
    reverse = [w[::-1] for w in elisions]
    reverse.sort()
    sorted_list = [w[::-1] for w in reverse]
    return sorted_list