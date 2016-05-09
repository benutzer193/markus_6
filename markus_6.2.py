#!/usr/bin/env python
# -*- coding: utf-8 -*-


###############################################################
#                                                             #
#                          markus_6.2                         #
#                                                             #
###############################################################

import pickle
import os.path
import sys
import signal
import time


#--------------------------------#
#           Variables            #
#--------------------------------#

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
file_path = sys.argv[0]
if os.path.isfile(os.path.join(__location__, "markus_6.2-primes.bin")):
    pfile = open(os.path.join(__location__, "markus_6.2-primes.bin"), "rb")
    Primes = sorted(list(set(pickle.load(pfile))))
    pfile.close()
    n = Primes[-1]
else:
    Primes=[2]
    n=2

if os.path.isfile(os.path.join(__location__, "markus_6.2-lastnum.txt")):
    pfile = open(os.path.join(__location__, "markus_6.2-lastnum.txt"), "r")
    n = int(pfile.read())
    pfile.close()

CSI="\x1B["
RESET=CSI+"m"
RED=CSI+"31;1m"
GREEN = CSI + "32;1m"
BLUE = CSI + "34;1m"
BLUE_BG = CSI + "30;44;1m"
WHITE_BG = CSI + "30;47m"

#--------------------------------#
#           Functions            #
#--------------------------------#

def signal_handler(signal, frame):
    pfile = open(os.path.join(__location__, "markus_6.2-primes.bin"), "wb")
    pickle.dump(Primes,pfile)
    pfile.close()
    pfile = open(os.path.join(__location__, "markus_6.2-lastnum.txt"), "w")
    pfile.write(str(n))
    pfile.close()
    os.system( "cls" if os.name == "nt" else "clear")
    print("Current Prime list saved in ./markus_6.2-primes.bin")
    print("Last tested number saved in ./markus_6.2-lastnum.txt")
    sys.exit(0)

def print_cli(n,factor,Primes,n_sqroot,is_prime=None):

    if is_prime is None:
        print_is_prime = ""
        print_factor = ""
    else:
        if is_prime:
            print_is_prime = GREEN + "YES" + RESET
            print_factor = BLUE + "NONE" + RESET
        else:
            print_is_prime = RED + "NO" + RESET
            print_factor = BLUE + "{1}  ( {0} = {1} ".format(n,factor)
            print_factor += "* {2} )".format(n,factor,n//factor)
            print_factor += RESET



    print_txt  = "#"*62
    print_txt += "\n#{}#".format(" "*60)
    print_txt += "\n#{0}".format(" "*25)
    print_txt += CSI + "1m" + "markus_6.2" + RESET
    print_txt += "{}#".format(" "*25)
    print_txt += "\n#{}#\n".format(" "*60)
    print_txt += "#"*62
    print_txt += "\n\n\n"

    print_txt += BLUE_BG
    print_txt += " Testing {} ".format(n)
    print_txt += RESET + "\n\n"
    print_txt += " Is Prime: {}".format(print_is_prime)
    print_txt += "\n Found Factor: {}".format(print_factor)

    print_txt += "\n\n Testing if divisible by:\n\n  "
    print_txt += WHITE_BG + " "

    FINDEX = Primes.index(factor)
    m = 8
    for prime in Primes[max(0,FINDEX-8):FINDEX]:
        print_txt += "{} ".format(prime)
        m -= 1
    print_txt += BLUE_BG + "{}".format(factor)
    print_txt += WHITE_BG
    for prime in Primes[FINDEX+1:min(FINDEX+8+m,len(Primes))]:
        if prime > n_sqroot:
            break
        print_txt += " {}".format(prime)
    print_txt += " " + RESET

    print_txt += "\n" * ROWS

    print(print_txt)

def is_prime(n,Primes):
    P_LAST = 2
    n_sqroot = n**0.5
    for p in Primes:
        if p > n_sqroot:
            break
        P_LAST = p
        if n%p == 0:
            print_cli(n,p,Primes,n_sqroot,False)
            return False
        print_cli(n,p,Primes,n_sqroot)
        time.sleep(0.6)
    print_cli(n,P_LAST,Primes,n_sqroot,True)
    Primes.append(n)
    return True


#--------------------------------#
#            Script              #
#--------------------------------#

signal.signal(signal.SIGINT, signal_handler)


while True:
    term_size = os.popen('stty size', 'r').read().split()
    ROWS, COLS = term_size
    ROWS = int(ROWS) - 16

    is_prime(n,Primes)
    time.sleep(4)
    n += 1

signal.signal(signal.SIGINT, signal_handler)
