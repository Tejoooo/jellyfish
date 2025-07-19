import argparse
parser = argparse.ArgumentParser(description='A text editor')
parser.add_argument('file', help='filepath to edit.', default=None, nargs='?')
arg_dict = vars(parser.parse_args())

import os
filepath = arg_dict['file']
if filepath:
    if os.path.exists(filepath):
        pass

line_hash_map   = {0:0}      # map line# -> byte postion
session_changes = {}      # map line# -> edits

# note to myself
# read line by line
# if user wants to jump to a line, go the line by seeking the newline delims.
    # you may use this to index the file for those ... lines
# do not have to index all newlines -- thats just not optimized way

# debug tools
log = ''
def print_log(log_str):
    global log
    log += '\n' + log_str

def cache_index(filepath:str, line_num:int):
    # find the line less than but closest to line_num
    # then start seeking from there
    floor_line = max(line for line in line_hash_map if line < line_num)
    floor_byte = line_hash_map[floor_line] # this is start of floor_line
    lines_to_skip = line_num - floor_line
    with open(filepath, 'rb') as f:
        f.seek(floor_byte)
        # now to skip n lines
        for _ in range(lines_to_skip):
            f.readline()
        pos = f.tell()
    line_hash_map.update({line_num: pos})

def read_lines(filepath:str, start_line_num:int, rows:int):
    lines = []
    if start_line_num not in line_hash_map:
        cache_index(filepath, start_line_num)
    
    byte_offset = line_hash_map[start_line_num]
    with open(filepath, 'rb') as f:
        f.seek(byte_offset)
        for i in range(rows):
            lines.append(f.readline().decode())
    return lines

############################################################################
from looks import app, TOP_PAD, LFT_PAD
import curses

def app_service(app_front):
    # type: (app) -> None
    cursor_row = 0
    while True:
        if app_front.key_inputs:
            key = app_front.key_inputs.pop(0)
            if key == curses.KEY_CLOSE:
                break
            if key == curses.KEY_DOWN:
                cursor_row += 1
                n_rows, _ = app_front.get_current_size()
                app_front.content = read_lines(filepath, cursor_row, n_rows)
                app_front.update()
            if key == curses.KEY_UP:
                cursor_row = max(0, cursor_row-1)
                n_rows, _ = app_front.get_current_size()
                app_front.content = read_lines(filepath, cursor_row, n_rows)
                app_front.update()

app_front = app(
    'text reader', 
    app_service, 
    buttons=[]
)

app_front.activate()

print(log)