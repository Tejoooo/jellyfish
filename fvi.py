from looks import app, TOP_PAD, LFT_PAD
import curses
import sys 
def getArgs():
    arg_dict = {None:[]}
    switch = None 
    # scan args
    for arg in sys.argv:
        # you hit a switch
        if arg[0] == '-':
            switch = arg
            if switch not in arg_dict:
                arg_dict.update({switch: []})    
            pass
        # if you hit an argument
        else:
            arg_dict[switch].append(arg)
    return arg_dict

arg_dict = getArgs()

if arg_dict[None][1:]:
    filepath = arg_dict[None][1]
    with open(filepath, 'r') as f:
        file_content = f.read().splitlines()
else:
    filepath = 'untitled.txt'
    file_content = []

# load frame
# read n lines from 