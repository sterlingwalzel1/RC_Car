import curses

def fart(stdscr):
    stdscr.clear()
    stdscr.addstr("Press any key to continue...")
    stdscr.refresh()
    key = stdscr.getch()
    stdscr.addstr(f"\nYou pressed: {int(key)}")
    stdscr.refresh()
    stdscr.getch()
    return key


try:
    while True:
        i = curses.wrapper(fart)
        print(i)


except KeyboardInterrupt:
    print('Got Keyboard Interript. Cleaning up an dexiting')
    GPIO.output(LED_O_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()