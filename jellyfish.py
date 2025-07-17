# from looks import app, TOP_PAD, LFT_PAD
# import curses

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
    if start_line_num not in line_hash_map:
        cache_index(filepath, start_line_num)
    
    byte_offset = line_hash_map[start_line_num]
    with open(filepath, 'rb') as f:
        f.seek(byte_offset)
        for i in range(rows):
            print(f.readline())


############################################################################
# TEST CODE - to be removed

input_str = '0'
while input_str:
    try:
        input_str = input('>>> ')
        input_idx = int(input_str)-1
    except:
        print(line_hash_map)
        break
    read_lines(filepath, input_idx, 5)
    
