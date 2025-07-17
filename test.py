import argparse

parser = argparse.ArgumentParser(description='A text editor')
parser.add_argument('file', help='filepath to edit.', default='untitled.txt', nargs='?')
args = parser.parse_args()

print(vars(args))