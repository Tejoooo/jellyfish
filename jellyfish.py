# from looks import app, TOP_PAD, LFT_PAD
# import curses
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

# index line offset bytes from file
# so that you can read only parts of the file cached into memory

with open(filepath, 'r') as f:
    line_end_indices = [idx for idx, c in enumerate(f.read()) if c=='\n']

def getLine(line_number):
    with open(filepath, 'r') as f:
        if line_number==0:
            start_idx = 0
        else:
            start_idx = line_end_indices[line_number-1] + 1
        end_idx = line_end_indices[line_number]
        f.seek(start_idx)
        line = f.read(end_idx - start_idx)
    return '[' + str(line_number) + ']:\t' + line

############################################################################
# TEST CODE - to be removed
import sys
import tty
import termios

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        if key == '\x1b':
            key += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

#       Up          Down        Right       Left
dirs = ['\x1b[A',   '\x1b[B',   '\x1b[C',   '\x1b[D']
############################################################################

line_number = 0
line = getLine(0)
sys.stdout.write('\r' + line)
clear_space = len(line)

key_strokes = []

while True:
    key = get_key()
    key_strokes.append(key)
    if key == dirs[0]:
        line_number = max(0, line_number-1)
    if key == dirs[1]:
        line_number = min(len(line_end_indices)-1, line_number+1)
    if key == 'q':
        print('')
        break
    
    line = getLine(line_number)
    sys.stdout.write('\r' + clear_space*' ')
    sys.stdout.write('\r' +line)
    clear_space = len(line)

print('\n')
print(key_strokes)