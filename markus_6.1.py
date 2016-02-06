#!/usr/bin/env python
# -*- coding: utf-8 -*-


###############################################################
#                                                             #
#                          marcus_6.1                         #
#                                                             #
###############################################################

import os
import random
import time



#--------------------------------#
#           Variables            #
#--------------------------------#


# numbers of generations until reset of grid
GENERATIONS = 3000

# symbol to be used (utf8 encoding)
SYM = "▇"

# delay between generations
DELAY = 0.05

# points to be calculated outside of visible area
# in every direction
CALC = 40



#--------------------------------#
#           Functions            #
#--------------------------------#

def generate_grid(COLS, ROWS, gen):
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            if random.randint(0,3) == 0:
                row += [1]
            else:
                row += [0]
        gen += [row]
    return gen


def print_generation(COLS, ROWS, gen, SYM="▇"):
    DEAD = True
    for i in range(CALC,ROWS-CALC):
        for j in range(CALC,COLS-CALC):
            if gen[i][j] == 1:
                print(SYM),
                DEAD = False
            else:
                print(" "),
        print("\n")
    return DEAD


def generate_nextgen(COLS, ROWS, current, next):
    for i in range(ROWS):
        for j in range(COLS):
            next[i][j] = check_neighbours(i, j, COLS, ROWS, current)


def check_neighbours(x, y, COLS, ROWS, gen):
    NEIGHBOURS = 0
    for j in range(max(0,y-1),min(y+2,COLS)):
        for i in range(max(0,x-1),min(x+2,ROWS)):
            NEIGHBOURS += gen[i][j]
    NEIGHBOURS -= gen[x][y]
    if gen[x][y] == 1 and (NEIGHBOURS < 2 or NEIGHBOURS > 3):
        return 0
    elif gen[x][y] == 0 and NEIGHBOURS == 3:
        return 1
    else:
        return gen[x][y]



#--------------------------------#
#            Script              #
#--------------------------------#

DOUBLE_CALC = CALC*2

while True:
   
    # get terminal size
    term_size = os.popen('stty size', 'r').read().split()
    ROWS_str, COLS_str = term_size
    COLS = int(COLS_str)/2 + DOUBLE_CALC
    ROWS = int(ROWS_str)/2 + DOUBLE_CALC
    
    # generate initial random grid
    current = []
    next = []
    generate_grid(COLS, ROWS, current)
    generate_grid(COLS, ROWS, next)

    # play game of life until:
    #   * grid empty
    #   * terminal size change
    #   * defined number of generations reached
    for _ in range(GENERATIONS):
        term_size = os.popen('stty size', 'r').read().split()
        if [ROWS_str, COLS_str] != term_size:
            break
        if print_generation(COLS, ROWS, current, SYM):
            break
        generate_nextgen(COLS, ROWS, current, next)
        time.sleep(DELAY)
        current, next = next, current
