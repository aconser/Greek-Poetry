# -*- coding: utf-8 -*-
"""
RESPONSION

This is a collection of tools for testing metrical responsion between stanzas 
of Greek poetry, with the aim of identifying instances of non-responsion, which
can be caused by textual issues or (unmarked) resolutions in the text.
    
If resolutions have already been marked with a '|' (between the syllables), then
they will be taken into account and will not produce non-responsion messages.

@author: Anna Conser, Columbia University, anna.conser@gmail.com
@license: MIT
"""

from greek_scansion import get_syllables, scan_line, \
UNKNOWN, EQUAL_LONG
import re

#%%
def textual_issues (line):
    """Checks whether the line contains characters indicating textual issues,
    and returns a boolean: True if there are issues, False if there are not.
    """
    if re.search(r'†|⟨|⟩|\[|\]', line):
        return True
    else:
        return False

def respond(st_pros, an_pros):
    #Check for an indeterminate prosody
    if st_pros == UNKNOWN or an_pros == UNKNOWN:
        return True
    #Check for matching prosody
    if st_pros == an_pros:
        return True
    #Check for compatible longs (in case of marked resolution)
    elif st_pros in EQUAL_LONG and an_pros in EQUAL_LONG:
        return True
    else:
        return False

def resp_check_line (line_number, st_line, an_line):
    """Compares two lines to identify instances of metrical non-responsion, by 
    checking (i) whether the number of syllables is the same, and (ii) whether
    there are clear contradictions in the prosodic scansion.  This can be used
    to identify textual issues or (unmarked) resolutions in the text.
    
    If resolutions have already been marked with a '|' (between the syllables)
    then the resulting bi-syllable is treated as a single syllable in the count,
    and is equivalent to one long syllable for the scansion check.
    
    The function returns a tuple containing a bool and a message (str).  When 
    lines don't respond, the bool is False and the message describes the issue.
    When the lines appear to resond, the bool is True and the message is empty.
    
    :param int line_number: the line number within the stanza (int or str)
    :param str st_line: a line from the strophe
    :param str an_line: the corresponding line from the antistrophe
    :return bool resp_check: boolean indicating whether the lines respond
    :return str message: describes the responsion issue, if any.
    """
    resp_check = True
    message = ''
    template = """{} issue in line {}{}:
    st: {}
        {}
    an: {}
        {}"""
    #Get syllables, line lengths, and meter (marked resolutions as a single syl) 
    st_syls = get_syllables(st_line.strip())
    an_syls = get_syllables(an_line.strip())
    st_len = len(st_syls)
    an_len = len(an_syls)
    st_meter = scan_line(st_line, final_anceps=True)
    an_meter = scan_line(an_line, final_anceps=True)
    #Check for textual issues
    if textual_issues(st_line) or textual_issues(an_line):
        message = template.format('TEXTUAL', line_number, '',
                                  ' - '.join(st_syls), st_meter, 
                                  ' - '.join(an_syls), an_meter)
        resp_check = False
    #Check whether they are the same number of syllables.
    elif st_len != an_len:
        message = template.format('SYL COUNT', line_number, '',
                                  ' - '.join(st_syls), st_meter, 
                                  ' - '.join(an_syls), an_meter)
        resp_check = False
    #If that worked, check whether the meters are compatible. Unknowns ('X') are
    #compatible with either length, leaving room for error. 
    else:
        for i in range(st_len):
            if not respond(st_meter[i], an_meter[i]):
                message = template.format('METER', line_number, ', syl '+str(i+1),
                                  ' - '.join(st_syls), st_meter, 
                                  ' - '.join(an_syls), an_meter)
                resp_check = False
    return (resp_check, message)
#%%
def resp_check_stanza (stanza1, stanza2):
    """Compares two stanzas to identify instances of metrical non-responsion,
    moving through the stanza line by line, calling resp_check_line() and
    compiling the messages.
    
    Returns a tuple containing a bool and a list of messages (each a str).  If 
    there are responsion issues, the bool is False.  If the stanzas appear to 
    respond, bool is True and the list will be empty.
    
    :param str stanza1: a stanza, formatted in lines (strophe)
    :param str stanza2: a corresponding stanza (antistrophe)
    :param str pair_name: a string identifying the pair for printouts
    :return bool resp_check: boolean indicating whether the stanzas respond
    :return list message_list: a list of strings describing responsion issues.
    """
    resp_check = True
    message_list = []
    st_lines = stanza1.split('\n')
    an_lines = stanza2.split('\n')
    assert len(st_lines) == len(an_lines), "Number of lines different."
    line_count = len(st_lines)
    for i in range(line_count):
        st_line = st_lines[i]
        an_line = an_lines[i]
        line_number = i+1
        line_check, message = resp_check_line(line_number, st_line, an_line)
        if line_check == False:
            message_list.append(message)
            resp_check = False
#    if resp_check == True:
#        print('No responsion issues found.')
    return (resp_check, message_list)

#%%
###############################################
# TESTING
###############################################

st = """ἰαλτὸϲ ἐκ δόμων ἔβαν
        χοὰϲ προπομποῦϲʼ ὀξύχειρι ϲὺν κόπωι.
        πρέπει παρὴιϲ φοίνιϲϲʼ ἀμυγ-
              μοῖϲ ὄνυχοϲ ἄλοκι νεοτόμωι,
        διʼ αἰῶνοϲ δʼ ἰυγ-
              μοῖϲι βόϲκεται κέαρ,
        λινοφθόροι δʼ ὑφαϲμάτων
        λακίδεϲ ἔφλαδον ὑπʼ ἄλγεϲιν,
        πρόϲτερνοι ϲτολμοὶ πέπλων ἀγελάϲτοιϲ
        ξυμφοραῖϲ πεπληγμένων."""
        
an = """τορὸϲ γὰρ ὀρθόθριξ δόμων
        ὀνειρόμαντιϲ ἐξ ὕπνου κότον πνέων
        ἀωρόνυκτον ἀμβόα-
              μα μυχόθεν ἔλακε περὶ φόβωι,
        γυναικείοιϲιν ἐν
              δώμαϲιν βαρὺϲ πίτνων·
        κριταί ⟨τε⟩ τῶνδʼ ὀνειράτων
        θεόθεν ἔλακον ὑπέγγυοι
        μέμφεϲθαι τοὺϲ γᾶϲ νέρθεν περιθύμωϲ
        τοῖϲ κτανοῦϲί τʼ ἐγκοτεῖν."""
        
def TEST():
    resp_check, messages = resp_check_stanza('Parodos-A', st, an)
    for m in messages:
        print(m)
    return resp_check
#%%
x = "       "