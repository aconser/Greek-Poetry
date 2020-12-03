#  process_OCT 2.1
#  
#  New in 2.0: Removed unused tools.
#  Check 1.0 for a function to export stanzas as formatted text (.txt) files.
#
#  This is collection of tools for importing and processing the text of 
#  antistrophic pairs in Greek tragedies.  I am working with text copied and 
#  pasted from PDFs downloaded from Oxford Scholarly Editions Online.
#
#  Note: Euripides PDFs (at least Medea) are encoded differently, and won't 
#  process. Missing paragraph breaks, and str/ant marks are at end of page. :(
#
#  See below for the actual execution.

import re
import unicodedata

def load_text (file_name, directory_name, utf_type='utf-8-sig'):
    """
    Loads Greek from a .txt file and returns a string.
    Text files made in Windows Notepad require utf_type='utf-8-sig'. 
    
    :param str file_name: name of the file to load
    :param str directory_name: directory where the file is located
    :param str utf_type: type of encoding 
        -- 'utf-8-sig'(default) or 'utf8' (non-Windows Notepad)
    :return: raw Greek text
    :rtype: string
    """
    with open(directory_name+file_name, encoding=utf_type) as f:
        raw_string = f.read()
    return raw_string

def _get_footer (raw_text, pdf_date = 'December 2017'):
    """Extracts the text of the footer.
    
    :param str raw_text: the raw text, copied and pasted from the pdf
    :param str pdf_date: the last text of the footer, default = 'December 2017'.
    """
    text = raw_text[:4000]
    footer = re.findall(r'DOI[\s\S]+? ' + pdf_date + r'[ ]?\n', text)[0]
    assert footer, 'No footer found. Supply a pdf_date= value ?'
    return footer

def clean_OCT (raw_text):
    """ Remove non-textual elements from PDFs downloaded from Oxford Scholarly 
    Editions Online. Current version removes endnotes, but leaves title 
    information and hypothesis.
    NOTE: Sigmas are standardized as lunate, which means they have to be converted to be 
    compatible with the CLTK and a number of other tools.
    
    :param str raw_oct: text as copied and pasted from the pdf.
    :param str footer_text: the unique text copy-pasted from the PDF footer (default = '')
    :return: clean text
    :rtype: str
    """
    text = raw_text
    footer = _get_footer(raw_text)
    text = text.replace(footer, '\n')    #remove footer
    text = unicodedata.normalize('NFC', text) #normalize diacriticals to combined
    text, _, _ = text.partition('NOTES')    #remove endnotes

    removal_list = [
        r'\.\.+\n*',          #dots at page breaks
        r'(PG|pg) \d+\n*',    #page numbers
        r'Page \d+ of \d+\n', #page number footers
        u'\u200e',            #formatting markers
        r'\d+ (?!BC)',        #line numbers (exception for play date, ending BC)
#        u'\xa0',             #indentations -- leaving these in for now
#        r'  +',              #extra spaces -- leaving these in for now
    ]
    sub_list = [
        (r'[σς]', r'ϲ'),      #standardize sigmas as LUNATE (I found one non-lunate in Aesch. Lib.)
        ("\"", "'"),          #replace double quotes with single quotes
        (r'ἄντ\.', r'ἀντ.'),  #correct false accent (I found one in Aesch. Seven)
        (r'\[ϲτρ ', r'[ϲτρ. '),     #add missing period (I found this in Aesch. Supp.)
        (r'ϲτρ\. ά', r'ϲτρ. α'),    #correct accent on label (I found this in Soph. Phil.)
        (r'\n̔', r' ́'),              #a weird accent on linebreak issue
        (r'ϲτρ\.(\w)', r'ϲτρ. \1'),  #fix missing space (I found this in Aesch. Eum.)
        (r'ἀντ\.(\w)', r'ἀντ. \1'),
        (r'ϲτρ\. (\w) *[ˊ′ʹ ́]', r'[ϲτρ. \1'),  #standardize stanza labels across editions
        (r'ἀντ\. (\w) *[ˊ′ʹ ́]', r'[ἀντ. \1'),
        #(r'\[\s+ϲτρ\.', r'\[ϲτρ\.'),   #weird linebreak between [ and label (Soph, Ajax)
        #(r'\[\s+ἀντ\.', r'\[ἀντ\.'),
        (r'\nϲτρ\.\n', r'\n[ϲτρ.\n'),  #standardize for non-lettered stanzas
        (r'\nἀντ\.\n', r'\n[ἀντ.\n'),
        (r'\n+\w\n+', '\n'),  #remove extra lines
        (r'\n +', '\n')       #remove extra whitespace
    ]
    for regex in removal_list:
        text = re.sub(regex, '', text)
    for old, new in sub_list:
        text = re.sub(old, new, text)
    return text

def get_pair_names (clean_text):
    """Go through clean text and get Greek label for each strophe and antistrophe. 
    Checks matches then replaces an. list with modified clone of st. list.
    This is a flabby solution, but I wanted to keep both sets of code.
    
    :param str raw_text: the raw text copy-pasted from an OCT PDF.
    :return: a list of tuples (strophe_name, antistrophe_name)"""
    st_names = re.findall('\[ϲτρ\. *\w*', clean_text)
    st_names = [st[1:] for st in st_names]    #remove the opening '['
    an_names = re.findall('\[ἀντ\. *\w*', clean_text)
    an_names = [an[1:] for an in an_names]    #remove the opening '[' 
    assert len(st_names) == len(an_names), 'missing strophe or antistrophe name in {}'.format(clean_text[:100])
    an_names = []    #replace actual antistrophe names with ones that match strophes in order
    for st in st_names:
        st_suffix = st[3:]
        an_name = 'ἀντ' + st_suffix
        an_names.append(an_name)
    return list(zip(st_names, an_names))

def raw_pair_names (clean_text):
    """Just for truoble-shooting!"""
    st_names = re.findall('\[ϲτρ\. *\w*', clean_text)
    st_names = [st[1:] for st in st_names]    #remove the opening '['
    an_names = re.findall('\[ἀντ\. *\w*', clean_text)
    an_names = [an[1:] for an in an_names]    #remove the opening '[' 
    return list(zip(st_names, an_names))

def get_music_structure (clean_text):
    """Extract a hierarchical list of stanza names according to song.
    
    :param list stanza_names: a list of tuples (strophe_name, antistrophe_name)
    :return: a list of songs, each of which is itself a list of tuples (st_name, an_name)
    """
    stanza_names = get_pair_names(clean_text)
    song_list = []
    current_song = []
    st_a_regex = re.compile(r'(?:ϲτρ\. α|ϲτρ\.$)')
    for i, names in enumerate(stanza_names):
        if re.search(st_a_regex, names[0]) and i !=0:
            song_list.append(current_song)
            current_song = []
        current_song.append(names)
    song_list.append(current_song)
    return song_list

def get_song_chunks (clean_text):
    """Break the text up into chunks at the start of each song.
    """
    song_chunks = re.split(r'\n(?=\[ϲτρ\. *α*\n)', clean_text)    #chunk text at start of each song.
    song_chunks = song_chunks[1:]    #delete first (pre-song) chunk
    return song_chunks

def get_stanzas (song_chunk, song_structure):
    """Identify and extract individual stanzas from song_chunks.
    
    :param str song_chunk: text of song, starting with strophe alpha and trailing until start of next song
    :param list song_structure: a list of tuples naming each pair (st_name, an_name)
    :return: a list of tuples containing the text for each stanza pait (st_text, an_text)
    
    Known bug: if there is non-stanza text following the strophe, it will not be removed, 
    leading to extra text at the end of both strophe and antistrophe.  I will have to remove these sections
    manually in the exported text files.
    """

    stanza_chunks = re.split(r'\n(?=\[.{4,10}\n)', song_chunk)    #break at start of each stanza
    song_texts = []
    for st, an in song_structure:
        strophe = ''
        antistrophe = ''
        for chunk in stanza_chunks:
            if re.match('\['+st, chunk):
                strophe = chunk
            if re.match('\['+an, chunk):
                antistrophe = chunk
        strophe_length = len(strophe.split('\n'))  # check number of lines in strophe and trim antistrophe to match
        antistrophe = antistrophe.split('\n')
        antistrophe = antistrophe[:strophe_length]
        antistrophe = '\n'.join(antistrophe)
        song_texts.append( (strophe, antistrophe) )
    return song_texts

def get_song_database (clean_text):
    """Identifies and extracts stanza pairs from raw OCT text, using the existing markers in the text.
    
    :param str raw_text: text copied and pasted from an OCT PDF. 
    :return: a list of songs, each itself a list of tuples containing the text (str) for stanza pairs
    :rtype: list
    
    Known issues: 
        - If the strophe is followed by dialogue (or anything except a bracket '['), 
          the strophe and antistrophe aren't trimmed properly (i.e. extra text is included).
    """
    music_structure = get_music_structure(clean_text)
    song_chunks = get_song_chunks(clean_text)
    song_database = []
    for i, song_structure in enumerate(music_structure):
        song = get_stanzas(song_chunks[i], song_structure)
        song_database.append(song)
    return song_database

def export_csv_pairs (song_database, file_name, directory_name):
    """Collapses the nested structure and exports the songs as a .csv
    """
    with open(directory_name+file_name, "w", encoding='utf-8') as output:
        for i, song in enumerate(song_database):
            for st, an in song:
                st_output = "\"" + st + "\""
                an_output = "\"" + an + "\""
                output_text = 'SONG ' + str(i+1) + ',' + st_output + ',' + an_output + '\n'
                output.write(output_text)

def process_OCT_csv (raw_file_name, raw_dir_name, export_dir_name):
    """Imports a file, processed it into a song database, and exports to a csv file with the same name,
    with the suffix '-SONGS'.
    
    :param str raw_file_name: name of the .txt file containing text copy/pasted from an OCT PDF.
    :param str directory_name: name of the directory where the file is located
    :param str export_dir_name: name of the directory where the export will go
    :return: none (exports database to a .csv file)
    """
    if raw_file_name.lower().endswith('txt'):
        raw_file_name = raw_file_name[:-4]
    raw_text = load_text(raw_file_name+'.txt', raw_dir_name)
    clean_text = clean_OCT(raw_text)
    database = get_song_database(clean_text)
    if raw_file_name.lower().endswith('-raw'):
        raw_file_name = raw_file_name[:-4]
    export_file_name = raw_file_name + "-SONGS.csv"
    export_csv_pairs(database, export_file_name, export_dir_name)
    print ('"{}" added to database as csv file'.format(raw_file_name))
    
def export_clean_play (raw_file_name, raw_dir_name, export_dir_name):
    """Imports a text file, cleans the excess OCT data, and exports to a new 
    text file with the same name, with the suffix '-CLEAN' instead of '-raw'.
    NOTE: This version keeps the title and edition information at the beginning,
    but removes end notes.
    
    :param str raw_file_name: name of the .txt file containing text copy/pasted from an OCT PDF.
    :param str directory_name: name of the directory where the file is located
    :param str export_dir_name: name of the directory where the export will go
    :return: none (exports clean text to a .txt file)
    """
    if raw_file_name.lower().endswith('txt'):
        raw_file_name = raw_file_name[:-4]
    raw_text = load_text(raw_file_name+'.txt', raw_dir_name)
    clean_text = clean_OCT(raw_text)
    if raw_file_name.lower().endswith('-raw'):
        raw_file_name = raw_file_name[:-4]
    export_file_name = raw_file_name + "-CLEAN.txt"
    with open(export_dir_name+export_file_name, "w", encoding='utf-8') as output:
        output.write(clean_text)
