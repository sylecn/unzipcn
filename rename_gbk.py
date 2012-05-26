#!/usr/bin/env python
# coding=utf-8

"""rename gbk file in given dir.

use it with find like this:

find . -exec rename_gbk {} \;

"""


import sys
import os


def out(msg, newline=True):
    """Prints a unicode message to stdout."""
    sys.stdout.write(msg.encode('utf-8'))
    sys.stdout.write('\n')


def warn(msg, newline=True):
    """Prints a unicode message to stderr."""
    sys.stderr.write(msg.encode('utf-8'))
    sys.stderr.write('\n')


def err(msg, newline=True):
    """Prints a unicode message to stderr and flush buffer."""
    warn('Error: ' + msg, newline)
    sys.stderr.flush()


fn = sys.argv[1]

# when unzip happen, the filename is already in a bad unknown encoding that is
# not the same as gbk?

# if this line can print the correct utf-8 filename, then this script will
# work.
print fn.decode('gbk').encode('utf-8')
sys.exit(0)

basename = os.path.basename
dirname = os.path.dirname
pathjoin = os.path.join

basefn = basename(fn)
basefn_cn = basefn.decode('gbk')
dir_ = dirname(fn)
if basefn != basefn_cn:
    warn(u'rename %s to %s\n' % (fn.decode('gbk'), basefn_cn))
    os.rename(fn, pathjoin(dir_, basefn_cn.encode('utf-8')))
