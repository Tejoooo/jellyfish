import curses
import os
import sys

def get_line(filename, lineno):
    """Read a specific line (0-based)."""
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            if i == lineno:
                return line.rstrip("\n")
    return ""

def get_all_lines(filename):
    """Read entire file into a list of lines."""
    with open(filename, "r") as f:
        return f.read().splitlines()

def write_all_lines(filename, lines):
    """Write list of lines back to file."""
    with open(filename, "w") as f:
        f.write("\n".join(lines))

def line_editor(stdscr, filename):

    curses.start_color()  # Enable color functionality
    # curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(1)
    stdscr.keypad(True)

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("")

    lines = get_all_lines(filename)
    if not lines:
        lines = [""]

    total_lines = len(lines)
    current_line_no = total_lines - 1
    current_line = lines[current_line_no]
    x = len(current_line)

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        prompt = ">>> "

        # Show prev line
        if current_line_no > 0:
            stdscr.addstr(height//2 - 1, 0, lines[current_line_no - 1][:width-1])

        # Show current line with >>> prefix
        stdscr.addstr(height//2, 0, prompt + current_line[:width - len(prompt) - 1], curses.A_BOLD)

        # Show next line
        if current_line_no < len(lines) - 1:
            stdscr.addstr(height//2 + 1, 0, lines[current_line_no + 1][:width-1])

        # Status bar
        status = f"Line {current_line_no+1}/{len(lines)} | Press y to Save | q to Quit"
        stdscr.addstr(height-1, 0, status[:width-1], curses.A_REVERSE)
        
        stdscr.move(height//2, len(prompt) + min(x, width - len(prompt) - 1))
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_line_no > 0:
            lines[current_line_no] = current_line
            current_line_no -= 1
            current_line = lines[current_line_no]
            x = min(x, len(current_line))

        elif key == curses.KEY_DOWN and current_line_no < len(lines)-1:
            lines[current_line_no] = current_line
            current_line_no += 1
            current_line = lines[current_line_no]
            x = min(x, len(current_line))

        elif key == curses.KEY_LEFT and x > 0:
            x -= 1
        elif key == curses.KEY_RIGHT and x < len(current_line):
            x += 1
        elif key in (curses.KEY_BACKSPACE, 127):
            if x > 0:
                current_line = current_line[:x-1] + current_line[x:]
                x -= 1
            elif x == 0 and current_line_no > 0:
                # Join with previous line
                prev_len = len(lines[current_line_no - 1])
                lines[current_line_no - 1] += current_line
                del lines[current_line_no]
                current_line_no -= 1
                current_line = lines[current_line_no]
                x = prev_len

        elif key == 10:  # Enter → insert new line
            lines[current_line_no] = current_line[:x]
            new_line = current_line[x:]
            lines.insert(current_line_no + 1, new_line)
            current_line_no += 1
            current_line = lines[current_line_no]
            x = 0

        elif key == ord('y'):  # Save
            lines[current_line_no] = current_line
            write_all_lines(filename, lines)

        elif key == ord('q'):  # Quit
            break

        elif 32 <= key <= 126:  # Printable chars
            current_line = current_line[:x] + chr(key) + current_line[x:]
            x += 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python allsample.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    curses.wrapper(line_editor, filename)
