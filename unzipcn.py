#!/usr/bin/env python
# coding=utf-8

"""unzip and convert filenames to utf-8 maybe.

dependencies:
# sudo pip install -U argparse

"""

import zipfile
import sys
import os
import argparse


def out(msg, newline=True):
    """Prints a unicode message to stdout."""
    sys.stdout.write(msg.encode('utf-8'))
    if newline:
        sys.stdout.write('\n')


def warn(msg, newline=True):
    """Prints a unicode message to stderr."""
    sys.stderr.write(msg.encode('utf-8'))
    if newline:
        sys.stderr.write('\n')


def err(msg, newline=True):
    """Prints a unicode message to stderr and flush buffer."""
    warn('Error: ' + msg, newline)
    sys.stderr.flush()


def get_filenames(zip_fn):
    """Returns a list of filenames in zip_fn."""
    if not zipfile.is_zipfile(zip_fn):
        err(u'Not a zip file.')
        raise RuntimeError(u'Not a zip file.')
    zf = zipfile.ZipFile(zip_fn)
    return zf.namelist()


def get_filenames_cn(zip_fn):
    return [x.decode('gbk') for x in get_filenames(zip_fn)]


def rename_files(filenames, target_dir=None):
    """Renames all files in filenames list."""
    filenames.sort(reverse=True)

    if target_dir:
        os.chdir(target_dir)

    basename = os.path.basename
    dirname = os.path.dirname
    pathjoin = os.path.join
    for f in filenames:
        if f[-1] == '/':
            fn = f[:-1]
        else:
            fn = f[:]

        basefn = basename(fn)
        basefn_cn = basefn.decode('gbk')
        dir_ = dirname(fn)
        if basefn != basefn_cn:
            # warn(u'rename %s to %s\n' % (fn.decode('gbk'), basefn_cn))
            if args.verbose:
                warn(u'renaming %s\n' % (fn.decode('gbk'),))
            os.rename(fn, pathjoin(dir_, basefn_cn.encode('utf-8')))


def unzip_cn(zip_fn, target_dir=None):
    """Unzips given zip file and rename all gbk filenames to utf-8
    filenames.

    """
    if not zipfile.is_zipfile(zip_fn):
        err(u'Not a zip file.')
        raise RuntimeError(u'Not a zip file.')
    zf = zipfile.ZipFile(zip_fn)
    zf.extractall(target_dir)

    # do rename maybe.
    filenames = zf.namelist()
    filenames_cn = [x.decode('gbk') for x in filenames]

    if filenames != filenames_cn:
        if args.verbose:
            out(u'unzip ok. rename files to utf-8 now...')
        # there could be nested directories. I need to do it level by
        # level. or generate all dirs that I need to rename *in order*.
        rename_files(filenames, target_dir)


def unzip():
    command = args.command
    zip_fn = args.zip_fn
    if command == 'list':
        for f in get_filenames_cn(zip_fn):
            out(f)
    elif command == 'unzip':
        unzip_cn(zip_fn, args.dir)
    else:
        parser.print_help()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=u'Unzip a zip file to current dir.')
    parser.add_argument('zip_fn', metavar='ZIP_FILE',
                        help=u'which zip file to act on.')
    parser.add_argument('-l', '--list', dest='command', action='store_const',
                        const="list", default="unzip",
                        help=u'list files in the zip file.')
    parser.add_argument('-d', '--dir', dest='dir', action='store',
                        help=u'unzip to this dir instead of current dir.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help=u'when enabled, show renaming progress.')
    args = parser.parse_args()

    unzip()
