#! /usr/bin/env python3

import curses

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()
curses.curs_set(0)

if curses.has_colors():
    curses.start_color()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

stdscr.addstr("hello there")
stdscr.chgat(-1)

stdscr.addstr(curses.LINES-1,0, "Menu at bootom")

stdscr.chgat(curses.LINES-1,7,1,curses.A_BOLD | curses.color_pair(2))

quote_window = curses.newwin(curses.LINES-2,curses.COLS,1,0)

quote_text_window = quote_window.subwin(curses.LINES-6, curses.COLS-4, 3,3)

quote_text_window.addstr("HELLO MAIN TEXT")

quote_window.box()

stdscr.noutrefresh()
quote_window.noutrefresh()

curses.doupdate()

while True:
    c = quote_window.getch()

    if c == ord('r') or c == ord('R'):
        quote_text_window.clear()
        quote_text_window.addstr('You pressed' + str(c), curses.color_pair(3))
        quote_text_window.refresh()
        quote_text_window.clear()
        quote_text_window.addstr("done...")

    elif c == ord('q') or c == ord('Q'):
        break

    # Refresh the windows from the bottom up
    stdscr.noutrefresh()
    quote_window.noutrefresh()
    quote_text_window.noutrefresh()
    curses.doupdate()

#Restore terminal
curses.nocbreak()
curses.echo()
curses.curs_set(1)

curses.endwin()
