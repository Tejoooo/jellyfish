# fvi converts file buffer into a 2D array of characters
# runs operations on this 2D array to edit buffer
# and finally save this buffer to a file.

import sys
import tty
import termios
import os
import copy
from string import printable

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

banner = """
-------------------------------------------------
fvi text editor : {}
-------------------------------------------------
"""

footer = """
-------------------------------------------------
Ln {}, Col {}  
-------------------------------------------------
"""

if len(sys.argv) == 1:
    filename = 'untitled.txt'
    buffer = ' '
else:
    filename = sys.argv[-1]
    if os.path.exists(filename):
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                buffer = f.read()
                f.close()
    else:
        buffer = ' '

# cursor
# map buffer into a graph area
class graph:
    def __init__(self, buffer):
        self.data = [list(l) for l in buffer.splitlines()]
        self.cursor_pos = 0, 0

    def draw(self):
        os.system('clear')
        print(banner.strip().format(filename))
        screen_data = self.insert_char('|')
        for row in screen_data:
            row_str = ''.join(row)
            print(row_str)
        print(footer.strip().format(*self.cursor_pos))

    def navigate(self, key_stroke):
        row_idx, col_idx = self.cursor_pos
        max_row = len(self.data)-1
        max_col = len(self.data[row_idx])
        if key_stroke ==  '\x1b[C': # right
            if col_idx == max_col:
                if row_idx == max_row:
                    pass 
                else:
                    # next line
                    row_idx += 1
                    col_idx = 0
            else:
                col_idx += 1
        elif key_stroke == '\x1b[D': # left
            if col_idx == 0:
                if row_idx == 0:
                    pass
                else:
                    row_idx -= 1
                    col_idx = len(self.data[row_idx])
            else:
                col_idx -= 1
        elif key_stroke == '\x1b[B': # down
            if row_idx == max_row:
                pass 
            else:
                row_idx += 1
                col_idx = min(len(self.data[row_idx]), col_idx)
        elif key_stroke == '\x1b[A': # up
            if row_idx == 0:
                pass
            else:
                row_idx -= 1
                col_idx = min(len(self.data[row_idx]), col_idx)
        self.cursor_pos = row_idx, col_idx

    def insert_char(self, char):
        screen_data = copy.deepcopy(self.data)
        row_idx, col_idx = self.cursor_pos
        screen_data[row_idx].insert(col_idx, char)
        return screen_data

    def insert(self, char):
        row_idx, col_idx = self.cursor_pos
        if key == '\x7f': # backspace
            if col_idx == 0:
                if row_idx == 0:
                    pass
                else:
                    prev_row_len = len(self.data[row_idx-1])
                    current_row = self.data[row_idx]
                    self.data.pop(row_idx)
                    self.data[row_idx-1] += current_row
                    row_idx -= 1
                    col_idx = prev_row_len
            else:
                self.data[row_idx].pop(col_idx-1)
                col_idx -= 1
        elif key == '\r': # enter
            left = self.data[row_idx][:col_idx]
            right = self.data[row_idx][col_idx:]
            
            self.data[row_idx] = left 
            self.data.insert(row_idx+1, right)
            row_idx = row_idx+1
            col_idx = 0
            pass
        elif key in printable[:-4]:
            self.data = self.insert_char(char)
            col_idx += 1
        self.cursor_pos = row_idx, col_idx

    def get_buffer(self):
        return '\n'.join([''.join(row) for row in self.data])

paper = graph(buffer)

paper.draw()
while True:
    key = get_key()
    if key == '\x03':
        break
    if key in dirs:
        paper.navigate(key)
    else:
        paper.insert(key)
    paper.draw()

sys.stdout.write('Save file? (y/n): ')
key = get_key()
print(key)
if key in ['Y', 'y']:
    with open(filename, 'w') as f:
        f.write(paper.get_buffer())
        f.close()
        print(filename + ' saved')
    
