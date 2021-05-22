#!/usr/bin/env python3

import curses
import time
import unicornhathd

from   random  import randint

# ----------------------------------------------------------------------

# Inverted because of the display etc
_UP    = ( 0, -1)
_DOWN  = ( 0,  1)
_LEFT  = ( 1,  0)
_RIGHT = (-1,  0)
_DIRECTIONS = (_UP, _DOWN, _LEFT, _RIGHT)

_CONTROLS = {
    ord('w')        : _UP   ,
    ord('s')        : _DOWN ,
    ord('a')        : _LEFT ,
    ord('d')        : _RIGHT,
    curses.KEY_UP   : _UP   ,
    curses.KEY_DOWN : _DOWN ,
    curses.KEY_LEFT : _LEFT ,
    curses.KEY_RIGHT: _RIGHT
}

# The Gird:
_EMPTY = 0
_WALL  = 1
_PILL  = 2
_EATER = 3
_EXIT  = 4
_GRID  = (
  #  0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1
  #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
    (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), # 00
    (1,2,2,2,2,2,2,1,1,2,2,2,2,2,2,1), # 01
    (1,2,1,1,1,1,2,2,2,2,1,1,1,1,2,1), # 02
    (1,2,3,2,2,1,2,1,1,2,1,2,2,3,2,1), # 03
    (1,1,1,1,2,2,2,1,1,2,2,2,1,1,1,1), # 04
    (1,2,2,2,2,1,1,1,1,1,1,2,2,2,2,1), # 05
    (1,1,2,1,2,2,2,2,2,2,2,2,1,2,1,1), # 06
    (0,0,2,1,1,2,1,4,4,1,2,1,1,2,0,0), # 07
    (0,0,2,2,1,2,1,0,0,1,2,1,2,2,0,0), # 08
    (1,2,1,1,1,2,1,0,0,1,2,1,1,1,2,1), # 09
    (1,2,2,1,2,2,2,1,1,2,2,2,1,2,2,1), # 10
    (1,1,2,1,2,1,2,1,1,2,1,2,1,2,1,1), # 11
    (1,2,2,2,2,1,2,1,1,2,1,2,2,2,2,1), # 12
    (1,2,1,1,1,1,2,0,0,2,1,1,1,1,2,1), # 13
    (1,2,3,2,2,2,2,1,1,2,2,2,2,3,2,1), # 14
    (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), # 15
)

# How long ghosts can be eaten for (in seconds)
_GHOST_EAT_TIME   = 10
_GHOST_EAT_REVERT =  3

# How many seconds between ghost steps
_GHOST_STEP_TIME = 0.3

# The locations where the pacman and ghosts start
_PACMAN_STARTS = (
    (7, 13), (8, 13),
)
_GHOST_STARTS = (
    (7, 8), (8, 8),
    (7, 9), (8, 9),
)

# Colours of things
_PACMAN_COLOUR    =  (255, 255,   0)
_GHOST_COLOURS    = ((255,   0, 255),
                     (255,   0, 255),
                     (255,   0, 255),
                     (255,   0, 255),)
_GHOST_EAT_COLOUR = (  0, 255, 255)
_GRID_COLOURS     = ((  0,   0,   0),  # Empty
                     (  0,   0, 255),  # Wall
                     (127,   0,   0),  # Pill
                     (255, 255, 255),  # Ghost eating pill
                     (  0,   0, 127),) # Ghost start exit

# ----------------------------------------------------------------------

def main(stdscr):
    """
    The main loop of the program.
    """

    # Set-ups
    unicornhathd.rotation(270)
    unicornhathd.brightness(0.6)
    (width, height) = unicornhathd.get_shape()

    stdscr.nodelay(1)
    stdscr.addstr(2, 12, 'Unicorn HAT HD: Pacman')
    stdscr.addstr(4,  5, 'w = UP, s = DOWN, a = LEFT, d = RIGHT')
    stdscr.addstr(6, 12, 'Or use the arrow keys.')
    stdscr.addstr(8, 12, 'Press Ctrl+C to exit!')

    # Copy the grid in. We have to switch from row-major to column-major for
    # [x,y] access to work here.
    grid = [[0] * len(_GRID) for i in range(len(_GRID[0]))]
    for x in range(len(_GRID[0])):
        for y in range(len(_GRID)):
            grid[x][y] = _GRID[y][x]

    # These need to match
    if width != len(grid[0]) or height != len(grid):
        raise ValueError(
            "Sorry, wrong shape. Wanted %d x %d but had %d x %d" %
            (len(grid[0]), len(grid), width, height)
        )


    # State
    ghost_posns = [list(_GHOST_STARTS[i % len(_GHOST_STARTS)])
                   for i in range(len(_GHOST_COLOURS))]
    ghost_moves = [_DIRECTIONS[randint(0, len(_DIRECTIONS)-1)]
                   for i in range(len(ghost_posns))]
    ghost_times = [0 for i in range(len(ghost_posns))]
    pacman_posn = list(_PACMAN_STARTS[0])
    score       = 0

    running     = True
    eating_time = 0

    try:
        while running:
            # What is the time?
            now = time.time()

            # Draw the display
            unicornhathd.clear()

            # The static parts of the grid. And count any pills at the same time
            has_pill = False
            for x in range(len(grid)):
                for y in range(len(grid[x])):
                    try:
                        e = grid[x][y]
                        (r, g, b) = _GRID_COLOURS[e]
                        unicornhathd.set_pixel(x, y, r, g, b)
                        if e in (_PILL, _EATER):
                            has_pill = True
                    except IndexError:
                        pass

            # No pills means that we're done
            if not has_pill:
                running = False
                break

            # Now handle inputs
            (xd, yd) = (0, 0)
            key = 0
            while key != -1:
                key = stdscr.getch()
                if key in _CONTROLS:
                    (xd, yd) = _CONTROLS[key]

            # Move pacman?
            (px, py) = (pacman_posn[0] + xd,
                        pacman_posn[1] + yd)
            if px < 0:
                px += len(grid)
            elif px >= len(grid):
                px -= len(grid)
            elif py < 0:
                py += len(grid[0])
            elif py >= len(grid[0]):
                py -= len(grid[0])
            if grid[px][py] not in (_WALL, _EXIT):
                pacman_posn[0] = px
                pacman_posn[1] = py

            # What did pacman eat, if anything
            e = grid[pacman_posn[0]][pacman_posn[1]]
            if e == _PILL:
                score += 1
            elif e == _EATER:
                eating_time = now

            # Whether ghosts can be eaten
            eating = now - eating_time < _GHOST_EAT_TIME

            # Move the ghosts
            for i in range(len(ghost_posns)):
                # Too soon?
                if now - ghost_times[i] < _GHOST_STEP_TIME:
                    continue

                # Try to move the ghost
                while True:
                    # Current state
                    (px, py) = ghost_posns[i]
                    (dx, dy) = ghost_moves[i]

                    # First see if the ghost might want to change direction
                    # because of a junction
                    for d in _DIRECTIONS:
                        # See if it's a change and not a reversal
                        if ((d[0] == dx and d[1] == dy) and
                            (d[0] !=  0 and d[0] == -dx or
                             d[1] !=  0 and d[1] == -dy)):
                            continue

                        # See if it will hit the wall
                        nx = px + d[0]
                        ny = py + d[1]
                        if (nx < 0 or nx >= len(grid   ) or
                            ny < 0 or ny >= len(grid[0]) or
                            grid[nx][ny] == _WALL):
                            continue

                        # See if we want to choose it
                        if randint(0, 1):
                            ghost_moves[i] = d
                            (dx, dy)       = d
                            break

                    # Now move the ghost
                    nx = px + dx
                    ny = py + dy
                    if nx < 0:
                        nx += len(grid)
                    elif nx >= len(grid):
                        nx -= len(grid)
                    elif ny < 0:
                        ny += len(grid[0])
                    elif ny >= len(grid[0]):
                        ny -= len(grid[0])
                    # See if it will hit to wall (or, if can be eaten, the exit
                    # since we don't want them to leave in that case).
                    if (grid[nx][ny] != _WALL and
                        (not eating or grid[nx][ny] != _EXIT)):
                        ghost_posns[i][0] = nx
                        ghost_posns[i][1] = ny
                        ghost_times[i]    = now
                        break
                    else:
                        ghost_moves[i] = _DIRECTIONS[randint(0, len(_DIRECTIONS)-1)]

            # Whatever was there is now wiped out
            grid[pacman_posn[0]][pacman_posn[1]] = _EMPTY

            # Draw pacman and the ghosts
            for i in range(len(ghost_posns)):
                # The colour of the ghosts will be eatable if we are eating, but
                # we flash we as get close to reverting to normal
                if (eating and
                    (now - eating_time < (_GHOST_EAT_TIME - _GHOST_EAT_REVERT) or
                     (int(now * 10) % 2) == 0)):
                    (r, g, b) = _GHOST_EAT_COLOUR
                else:
                    (r, g, b) = _GHOST_COLOURS[i]
                (x, y) = ghost_posns[i]
                unicornhathd.set_pixel(x, y, r, g, b)
            (x, y)    = pacman_posn
            (r, g, b) = _PACMAN_COLOUR
            unicornhathd.set_pixel(x, y, r, g, b)

            # And display it all
            unicornhathd.show()
            time.sleep(0.01)

            # See if pacman met a ghost
            for (i, (x, y)) in enumerate(ghost_posns):
                if pacman_posn[0] == x and pacman_posn[1] == y:
                    if eating:
                        # The ghost was eaten, put it back to the start
                        score += 20
                        ghost_posns[i][0] = _GHOST_STARTS[i][0]
                        ghost_posns[i][1] = _GHOST_STARTS[i][1]
                    else:
                        # Oh dear, the ghost ate pacman
                        running = False
                        break

    except KeyboardInterrupt:
        pass

    # What did you get?
    curses.endwin()
    print('You scored: {}\n'.format(score))

    # And clear everything
    unicornhathd.clear()
    unicornhathd.off()

# ----------------------------------------------------------------------

if __name__ == '__main__':
    print("""\
Unicorn HAT HD: Pacman

Press Ctrl+C to exit!

""")

    curses.wrapper(main)
