# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:44:55 2018

@author: Anna
"""

#from class_Play import Play

import matplotlib.pyplot as plt
from class_play import Play

#%%
def graph_play (Play, y_limit=23, x_limit=33):
    """Displays the songs from a play graphically according to their degree of
    accentual responsion. The result is a color-coded bubble graph using the 
    following variables:
        x-axis: percentage of repeated notes
        y-axis: percentage of matched accentual falls
        bubble-size: syllable count of stanza
        color: song in which stanza occurs
    """
    color_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'grey']
    data = Play.graph_data(short_name=True)
    #Organize data by song
    #  Each song is a list of rows, which are each as list as follows:
    # [name, song_num, stanza_name, syl_count, repeat_percentage, match_percentage]    
    song_list = []
    current_song = []
    current_song_num = 1
    for row in data:
        song_num = row[1]
        if song_num != current_song_num:
            song_list.append(current_song)
            current_song = []
            current_song.append(row)
            current_song_num = song_num
        else:
            current_song.append(row)
    #Graph by song
    fig, ax = plt.subplots()
#    plt.figure(figsize=(13.33, 7.5), dpi=300)
    for song in song_list:
        x = [row[4]*100 for row in song]  # repeat percentages
        y = [row[5]*100 for row in song]  # match percentages
        size = [row[3]*2 for row in song]  # syllable count
        color = color_list[song[0][1]-1] #song number
        song_name = 'Song ' + str(song[0][1])
        ax.scatter(x, y, s=size, c=color, label=song_name, alpha=0.3, edgecolors='none')
    # Format graph
    plt.ylim(0,y_limit)
    plt.xlim(0,x_limit)
    
    #Add graph labels
    ax.legend()
    ax.grid(True)
    plt.xlabel('% Repeats')
    plt.ylabel('% Matches')
    plt.title(Play.name + ': Stanza Pairs by Ode')
    #Add point labels
    for _, _, label, _, x, y in data:
        plt.annotate(label, xy=(x*100, y*100), xytext=(3, 3),
            textcoords='offset points', ha='left', va='bottom',
            #bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            #arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0')
            )
    #Set Style
    #plt.style.use('')
    #Save Graph
    plt.savefig(Play.name+'-GRAPH.png', dpi=600)
    #Display graph
    plt.show()
    

#%%%  TESTING
def Test_graphing ():
    A_directory = '..//Corpus/Aeschylus/'
    Ag_file = 'Aesch-Ag.csv'
    Ag = Play('Agamemnon', Ag_file, A_directory)
    graph_play(Ag)
    return Ag
#%%
#from class_play import Play
#from os import listdir
#A_directory = '..//Corpus/Aeschylus/'
#file_list = listdir(A_directory)
#play_list = []
#for file in file_list:
#    print('Adding {} to list'.format(file))
#    p = Play(file[6:-4], file, A_directory)
#    play_list.append(p)
#for p in play_list:
#    graph_play(p)
    