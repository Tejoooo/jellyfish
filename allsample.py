import curses
import sys

def editor(stdscr, filename):
    # Read file into list of lines
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        lines = [""]  # empty new file

    current_line = 0
    current_col = 0
    scroll_offset = 0  # for scrolling

    curses.curs_set(1)  # show cursor
    stdscr.keypad(True)  # enable arrow keys

    while True:
        stdscr.clear()

        # Get terminal size
        height, width = stdscr.getmaxyx()

        # Adjust scroll to keep cursor visible
        if current_line < scroll_offset:
            scroll_offset = current_line
        elif current_line >= scroll_offset + height:
            scroll_offset = current_line - height + 1

        # Display visible lines
        for idx, line in enumerate(lines[scroll_offset:scroll_offset+height]):
            stdscr.addstr(idx, 0, line[:width-1])

        # Place cursor
        cursor_y = current_line - scroll_offset
        cursor_x = min(current_col, len(lines[current_line]))
        stdscr.move(cursor_y, cursor_x)

        stdscr.refresh()

        # Wait for key
        key = stdscr.getch()

        if key == curses.KEY_UP:
            if current_line > 0:
                current_line -= 1
                current_col = min(current_col, len(lines[current_line]))
        elif key == curses.KEY_DOWN:
            if current_line < len(lines) - 1:
                current_line += 1
                current_col = min(current_col, len(lines[current_line]))
        elif key == curses.KEY_LEFT:
            if current_col > 0:
                current_col -= 1
        elif key == curses.KEY_RIGHT:
            if current_col < len(lines[current_line]):
                current_col += 1
        elif key == curses.KEY_BACKSPACE or key == 127:
            if current_col > 0:
                lines[current_line] = lines[current_line][:current_col-1] + lines[current_line][current_col:]
                current_col -= 1
        elif key == 10:  # Enter key -> insert new line
            new_line = lines[current_line][current_col:]
            lines[current_line] = lines[current_line][:current_col]
            lines.insert(current_line+1, new_line)
            current_line += 1
            current_col = 0
        elif key == ord('q'):  # quit
            break
        elif key == ord('y'):  # save
            with open(filename, "w") as f:
                f.write("\n".join(lines))
        elif 32 <= key <= 126:  # printable chars
            lines[current_line] = (
                lines[current_line][:current_col] + chr(key) + lines[current_line][current_col:]
            )
            current_col += 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python allsample.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    curses.wrapper(editor, filename)
