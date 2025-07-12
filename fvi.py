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

from string import printable
allowed_keys = [ord(c) for c in printable[:-4]]

def appService(app_front):
    # type: (app) -> None
    app_front.stdscr.move(TOP_PAD, LFT_PAD+1)
    while True:
        if app_front.key_inputs:
            key = app_front.key_inputs.pop(0)
            if key == curses.KEY_CLOSE:
                # ask to save
                break

            if True:
                # ch = chr(key) if key < 256 else str(key)
                if key == ord('\n'):
                    app_front.content.append('')

                elif key == curses.KEY_BACKSPACE:
                    # if the content is empty, dont do shit
                    if not len(app_front.content):
                        continue
                    # if there is a line but it has width
                    if len(app_front.content[-1]):
                        app_front.content[-1] = app_front.content[-1][:-1]
                    # if there is a line but it has no width
                    else:
                        app_front.content.pop()
                    # then 
                    pass

                # utf charset
                elif key in allowed_keys:
                    ch =  chr(key)
                    if len(app_front.content):
                        app_front.content[-1] += ch
                    else:
                        app_front.content = [ch]
                elif (key not in allowed_keys) and key < 256:
                    ch =  '[' + str(key) + ']'
                    if len(app_front.content):
                        app_front.content[-1] += ch
                    else:
                        app_front.content = [ch]
                else:
                    continue
                app_front.update()
                # app_front.stdscr.refresh()
                
                if not key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:   
                    app_front.stdscr.move(
                        TOP_PAD + max(len(app_front.content) - 1, 0),
                        LFT_PAD + (len(app_front.content[-1]) if len(app_front.content) else 0) + 1
                    )
                else:
                    y, x = app_front.stdscr.getyx()
                    
                    pass

def s_button_click():
    with open(filepath, 'w') as f:
        for line in myApp.content:
            f.write(line + '\n')
    myApp.exit_log += filepath + ' saved'
    # schedule a close
    myApp.key_inputs.append(curses.KEY_CLOSE)
    pass

myApp = app(
    'fvi [' + filepath + ']', 
    appService, 
    buttons=[('S', s_button_click)],
    content=file_content
)

myApp.activate()