#!/usr/bin/env python
# -*- coding: utf-8 -*-


###############################################################
#                                                             #
#                          markus_6.2                         #
#                                                             #
###############################################################


import os
import signal

from pickle import load,dump
from sys    import exit
from time   import sleep



#--------------------------------#
#           Variables            #
#--------------------------------#


FILE_LOCATION = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

PFILE = os.path.join(FILE_LOCATION, "markus_6.2-primes.bin")
NFILE = os.path.join(FILE_LOCATION, "markus_6.2-lastnum.txt")

if os.path.isfile(PFILE):
    with open(PFILE, "rb") as pfile:
        prime_list = load(pfile)

    prime_list = sorted(list(set(prime_list)))
    NUM = prime_list[-1]

else:
    prime_list=[2]
    NUM = 3

if os.path.isfile(NFILE):
    with open(NFILE, "r") as nfile:
        NUM = nfile.read()
    NUM = int(NUM)



CSI   = "\x1B["
RESET = CSI+"m"

RED   = CSI + "31;1m"
GREEN = CSI + "32;1m"
BLUE  = CSI + "34;1m"

BLUE_BG  = CSI + "30;44;1m"
WHITE_BG = CSI + "0;30;47m"




#--------------------------------#
#           Functions            #
#--------------------------------#


def debug(DEBUG=""):
    print("I am here! {}".format(DEBUG))
    sleep(2)



def rows():
    return os.get_terminal_size().lines - 18



def signal_handler(signal, frame):
    with open(PFILE, "wb") as pfile:
        dump(prime_list,pfile,-1)

    with open(NFILE, "w") as nfile:
        nfile.write(str(NUM))

    os.system( "cls" if os.name == "nt" else "clear")
    print("Current Prime list saved in ./markus_6.2-primes.bin")
    print("Last tested number saved in ./markus_6.2-lastnum.txt")

    exit(0)



def print_cli(NUM,FACTOR,prime_list,NUM_SQROOT,is_prime=None):
    if is_prime is None:
        print_is_prime = ""
        print_factor = ""
    else:
        if is_prime:
            print_is_prime = GREEN + "YES" + RESET

            print_factor  = BLUE
            print_factor += "NONE"
            print_factor +=  RESET

        else:
            print_is_prime = RED + "NO" + RESET

            print_factor  = BLUE
            print_factor += "{}".format(FACTOR)
            print_factor += RESET + " "*5
            print_factor += "( {0} = {1} * {2} )".format(NUM,FACTOR,NUM//FACTOR)


    PRINT_TXT  = "\n "
    PRINT_TXT += "#"*62
    PRINT_TXT += "\n #{}#".format(" "*60)
    PRINT_TXT += "\n #{}".format(" "*25)
    PRINT_TXT += CSI + "1m" + "markus_6.2" + RESET
    PRINT_TXT += "{}#".format(" "*25)
    PRINT_TXT += "\n #{}#\n ".format(" "*60)
    PRINT_TXT += "#"*62
    PRINT_TXT += "\n\n\n\n    "


    PRINT_TXT += BLUE_BG
    PRINT_TXT += " Current number:  {} ".format(NUM)
    PRINT_TXT += RESET + "\n\n\n"
    PRINT_TXT += "      Is Prime:  {}".format(print_is_prime)
    PRINT_TXT += "\n  Found Factor:  {}".format(print_factor)


    PRINT_TXT += "\n\n\n  Testing if divisible by:  "# + "\n\n  "
    PRINT_TXT += WHITE_BG + " "

    FAC_INDEX = prime_list.index(FACTOR)
    m = 4

    for prime in prime_list[max(0,FAC_INDEX-4):FAC_INDEX]:
        PRINT_TXT += "{} ".format(prime)
        m -= 1

    PRINT_TXT += BLUE_BG
    PRINT_TXT += "{}".format(FACTOR)
    PRINT_TXT += WHITE_BG

    for prime in prime_list[FAC_INDEX+1:min(FAC_INDEX+5+m,len(prime_list))]:
        if prime > NUM_SQROOT:
            break
        PRINT_TXT += " {}".format(prime)

    try:
        next_prime = prime_list.index(prime)
        next_prime = prime_list[next_prime+1]
        if prime < NUM_SQROOT and next_prime <= NUM_SQROOT:
            PRINT_TXT += " …"
    except:
        pass

    PRINT_TXT += " " + RESET
    PRINT_TXT += "\n" * rows()

    print(PRINT_TXT)



def is_prime(NUM,prime_list):
    P_LAST = 2
    NUM_SQROOT = NUM**0.5
    for p in prime_list:
        if p > NUM_SQROOT:
            break
        P_LAST = p
        if NUM%p == 0:
            print_cli(NUM,p,prime_list, NUM_SQROOT, False)
            return False
        print_cli(NUM,p,prime_list, NUM_SQROOT)
        sleep(0.6)
    print_cli(NUM,P_LAST,prime_list,NUM_SQROOT,True)
    prime_list.append(NUM)
    return True



#--------------------------------#
#            Script              #
#--------------------------------#


signal.signal(signal.SIGINT, signal_handler)
os.system( "cls" if os.name == "nt" else "clear")

while True:

    is_prime(NUM,prime_list)
    sleep(4)
    NUM += 1

signal.signal(signal.SIGINT, signal_handler)
