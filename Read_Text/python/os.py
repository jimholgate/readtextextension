#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
OS - system commands
====================

Use python to access operating system commands.

Python is an interpreted, interactive, object-oriented programming language.

Read Selection... Dialog setup:
-------------------------------

External program:

    /usr/bin/python

Command line options (default):

    "(OS_PY)" --c "espeak -f '(TMP)'"

See the manual page for `python` for more detailed information

[Read Text Extension](http://sites.google.com/site/readtextextension/)

Copyright (c) 2011 - 2018 James Holgate

'''
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
    )
import getopt
import os
import sys
import readtexttools


def usage():
    sA = ' ' + os.path.split(sys.argv[0])[1]
    print ('')
    print ('Usage')
    print (sA + ' --c "string" ')
    print ("")


def playscript(s1):
    try:
        print ('> ' + s1)
        readtexttools.myossystem(s1)
    except IOError as err:
        print ('I was unable to do the command!')
        usage()
        sys.exit(2)


def main():
    s1 = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc', ['help', 'command='])
    except getopt.GetoptError as err:
        # print help information and exit:
        print ('option -a not recognized')
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif o in ('-c', '--command'):
            s1 = a
        else:
            assert False, 'unhandled option'
    if (s1 == ''):
        s1 = sys.argv[-1]
    s2 = s1
    playscript(s2)
    sys.exit(0)


if __name__ == '__main__':
    main()
