"""
Parson's Code Display

@author: Charles Pletcher, expanded by Anna Conser
@license: MIT

"""
import re

def parsons_to_ascii(s: str):
    strophes = [l for l in s.split("\n") if l != ""]
    for strophe in strophes:
        y_coords = get_y_coords(strophe)
        max_height = max(y_coords)
        max_depth = min(y_coords)

        with open("parsons_out.txt", "w") as f:
            for row in reversed(range(max_depth, max_height + 1)):
                for c in y_coords:
                    if c == row:
                        f.write("* ")
                    else:
                        f.write("  ")

                f.write("\n")


def get_y_coords(notes: str) -> list[int]:
    notes = [n for n in notes if n != " "]

    y_coords = []

    for note in notes:
        if note == "*":
            y_coords.append(0)
        elif note.lower() == "u":
            y_coords.append(y_coords[-1] + 1)
        elif note.lower() == "d":
            y_coords.append(y_coords[-1] - 1)
        elif note.lower() == "r":
            y_coords.append(y_coords[-1])

    return y_coords


def test_parsons_to_ascii():
    parsons_to_ascii("* R U U R D D D D R U U R D R")


if __name__ == "__main__":
    test_parsons_to_ascii()

def arrow_to_parsons (contour_symbols: str):
    """Takes a string of Anna's accentual contour symbols and turns it into a 
    string of Parsons Code.  Removes whitespace and marks melisms as 'm', 
    to be taken in addition to contours"""
    
    new = "".join(contour_symbols.split())
    dictionary = {'*' : 'm',
                  'x' : '*',
                  '=' : 'r',
                  '≠' : 'r',
                  '≤' : 'u',
                  '↗' : 'u',
                  '⇘' : 'd',
                  '↘' : 'd'}
    for arrow, parsons in dictionary.items():
        new = new.replace(arrow, parsons)
    parsons = '*' + new[:-1]
    return parsons

def arrow_to_ascii(contour_symbols:str):
    parsons = arrow_to_parsons (contour_symbols)
    parsons_to_ascii(parsons)
    