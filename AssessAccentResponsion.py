"""
Assess Accentual Responsion

This module contains tools for testing whether syllables paired in responding
stanzas are significantly more compatible than other syllables in metrically
identical contexts.  For example, do two instances of metrical lekythia (LSLSLSL) 
which were sung to a single melody have more accentual alignment than that which
occurs by chance between other lekythia found in a given corpus?


@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""
import re
import Analysis.class_syllable as class_syllable
import Greek_Prosody.prosody as prosody
import itertools
    
def get_indices (pattern, string, regex=True):
    """Returns (start, end) indices for every match of a pattern within a
    string, including overlapping matches.  Return is a list of tuples."""    
    
    search_term = '(?=' + pattern + ')'
    starts = [m.start() for m in re.finditer(search_term, string)]
    if regex:
        bare_pattern = re.sub(r'\[(.+?)\]', r'X', pattern)
        bare_pattern = re.sub(r'[\[\]\(\)\|\^\$]', '', bare_pattern)
        offset = len(bare_pattern)
    else:
        offset = len(pattern)
    return [(s, s+offset) for s in starts]

#def get_matching_syllables (syl_list, indices):
#    """Given a list of syllables and a list of indices tuples (start, end),
#    returns a list of lists, each containing the indexed syllables."""
#    return [syl_list[start, end] for start, end in indices]

def find_meter_instances (pattern, syl_list, anceps=False):
    """Finds all the syllables in a list of SylGroup Objects which match a given
    metrical pattern. Returns a list of lists, each containing the syllables of
    a match.
    
    :param string pattern: the metrical pattern to be matched
    :param list syl_list: the list of SylGroup obects to be searched
    :return list matches: a list of metrical matches, each of which is a list
    of SylGroup Objects
    """
    scansion_pattern = ''.join(prosody.pretty_scansion(pattern))
    if anceps:
        scansion_pattern = re.sub(r'(.)', r'[\1⏒]', scansion_pattern)
    print(scansion_pattern)
    indices = get_indices(scansion_pattern, ''.join(s.meter for s in syl_list))
    return [syl_list[start:end] for start, end in indices] 

def unpair_syl_groups (syl_group_list):
    """Separates a list of SylGroup objects into two lists of Syllable objects.
    [Updates the metrical data on each Syllable.] Returns a tuple containing 
    both Syllables."""
    
    syl_list_a = []
    syl_list_b = []
    for syl_group in syl_group_list:
        syl_a, syl_b = syl_group.syllables
        #syl_a.prosody = syl_group.prosody
        #syl_b.prosody = syl_group.prosody
        syl_list_a.append(syl_a)
        syl_list_b.append(syl_b)
    return (syl_list_a, syl_list_b)
    
#def all_meter_instances (paired_instances):
#    """Separate the paired SylGroup instances out into a list of all instances of the
#    two separate lists of
#    matches by single syllables."""
#    
#    unpaired_matches = [syl_list for syl_group_list in paired_instances 
#                        for syl_list in unpair_syl_groups(syl_group_list)]
#    return unpaired_matches

def all_possible_pairings (paired_instances):
    """Separate the paired SylGroup instances out into a list of all instances of the
    two separate lists of
    matches by single syllables."""
    
    unpaired_instances = []
    for syl_group_list in paired_instances:
        syl_lists = unpair_syl_groups(syl_group_list)
        unpaired_instances.extend(syl_lists)
    
    all_possible_tuples = itertools.combinations(unpaired_instances, 2)
 
    all_possible_pairings = []
    for syl_list_a, syl_list_b in all_possible_tuples:
        syl_pairs = zip(syl_list_a, syl_list_b)
        syl_group_list = [class_syllable.SylGroup(pair) for pair in syl_pairs]
        all_possible_pairings.append(syl_group_list)
        
    return all_possible_pairings

def syl_comp_match_count (syl_list, secure=True):
    """Iterates through a list of SylGroup objects and counts the total, number
    of compatibles, and number of matches.  Returns a tuple with three ints.
    """
    if secure:
        syl_list = [s for s in syl_list if not s.corrupt]
    syl_count = len(syl_list)
    compatible_count = 0
    match_count = 0
    for syl in syl_list:
        if not syl.is_repeat():
            compatible_count += 1
            if syl.is_match(): match_count += 1
    return (syl_count, compatible_count, match_count)

def get_instance_data (syl_group_list):
    text_a = ''
    text_b = ''
    for syl_a, syl_b in (s.syllables for s in syl_group_list):
        text_a += syl_a.join_text
        text_b += syl_b.join_text
    syl_comp_match = syl_comp_match_count(syl_group_list)
    
    data_tuple = ("\"" + text_a + "\"", "\"" + text_b + "\"") + tuple(
            str(i) for i in syl_comp_match)
    
    return data_tuple
    
    
def assess_responsion (metrical_pattern, corpus_list, anceps=False):
    """This function identifies all possible instances of a given metrical 
    pattern within a list of SylGroup objects (presumably a stanza or line pair),
    and then assesses the accentual alignment between responding instances vs.
    all metrically identical instances.  The return is a dictionary containing
    the totals.
    """
    syl_group_lists = [s.syllables for s in corpus_list]
    
    paired_instances = []
    for l in syl_group_lists:
        paired_instances.extend(find_meter_instances(metrical_pattern, l, anceps=anceps))
    
    all_possible_instances = all_possible_pairings(paired_instances)

    directory_name = '/Users/anna/Documents/Python Scripts/Statistics/'
    try:
        name = corpus_list.name
    except:
        try:
            name = str([c.name for c in corpus_list])
        except:
            name = "Unknown"
    with open(directory_name + metrical_pattern + '.csv', 
              "w", encoding='utf-8') as output:
        output.write("Analysis of {} in {} when Anceps={}\n".format(
                metrical_pattern, corpus_list.name, str(anceps)))
        output.write('RESPONDS, TEXT_A, TEXT_B, SYL_COUNT, COMPATIBLE, MATCH' +'\n')
        output.write('\n')
        for i in paired_instances:
            row = 'True,' + ','.join(get_instance_data(i)) + '\n'
            output.write(row)
        output.write('\n')
        for i in all_possible_instances:
            row = 'False,' + ','.join(get_instance_data(i)) + '\n'
            output.write(row)
        
    print('Exported data to {}{}.csv'.format(directory_name, metrical_pattern))
    return None
#%%
import Analysis.class_author as CA
Aeschylus = CA.Author('Aeschylus')
all_stanzas = [pair for play in Aeschylus.plays for pair in play.pairs]
assess_responsion("LSLSLSL", all_stanzas)
    

    
#%%
    
def assess_responsion_OLD (metrical_pattern, syl_list):
    """This function identifies all possible instances of a given metrical 
    pattern within a list of SylGroup objects (presumably a stanza or line pair),
    and then assesses the accentual alignment between responding instances vs.
    all metrically identical instances.  The return is a dictionary containing
    the totals
    """

    paired_matches = find_meter_matches(metrical_pattern, syl_list)
    
    # First, separate the matches by SylGroups out into two separate lists of
    # matches by single syllables. corrupt syllables are excluded.

    unpaired_matches = []
    for match in paired_matches:
        match_a = []
        match_b = []
        for syl_group in match:
            if not syl_group.corrupt:
                syl_a, syl_b = syl_group.syllables
                match_a.append(syl_a)
                match_b.append(syl_b)
        unpaired_matches.append(match_a)
        unpaired_matches.append(match_b)
        
    # Second, line up all the matches by syllable, and for each 'responding' 
    # position, create all the potential SylGroups. Itertools.combinations 
    # automatically avoids duplications, finding each unique pairing.
    
    possible_syl_groups = []
    for position_syls in zip(unpaired_matches):
        for pair in itertools.combinations(position_syls, 2):
            possible_syl_groups.append(class_syllable.SylGroup(pair))
    
    # Now, make a list of all the real SylGroups, made of responding syllables.
    # This just means flattening the list of matches, excluding corrupt syllables.
    
    real_syl_groups = [syl_group for match in paired_matches for syl in match \
                       if not syl.corrupt]
    
    # Compile the data as a dict, where the entries are the counts for 
    # (syls, comps, matches).
        
    stat_dict = {'responding' : syl_comp_match_count(real_syl_groups),
                 'non-responding' : syl_comp_match_count(possible_syl_groups)}
    
    return stat_dict
