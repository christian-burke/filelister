"""
functions to read filelists from text file and store in Filelist class
"""


import os
import filelister as fs
import zlib


def read_filelist(infile, check_exists=True, compressed=False, check_exts=False):
    try:
        check_infile(infile)
        if compressed:
            flist = read_compressed(infile)
        else:
            flist = read_uncompressed(infile)
        fpaths = []
        exts = set()
        for fname in flist:
            exts.add(os.path.splitext(fname)[1].rstrip())
            fpaths.append(os.path.abspath(os.path.join(os.path.dirname(infile),
                                                       fname.rstrip())))
        return fs.Filelist(fpaths, allowed_exts=list(exts),
                           check_exists=check_exists)
    except Exception as e:
        raise e


def read_compressed(infile):

    """
    reads a compressed filelist
    """
    with open(infile, 'rb') as f:
        zdict = f.readline().strip()
        data = f.read()
    obj = zlib.decompressobj(zdict=zdict)
    data = obj.decompress(data)
    data += obj.flush()

    data = data.decode('utf-8').split(',')
    return data


def read_uncompressed(infile):
    """
    reads an uncompressed filelist
    """
    with open(infile, encoding='utf-8') as f:
        return f.read().split('\n')


def check_duplicate_path(fpaths):
    """
    checks if there is a duplicate filepath in filelist
    """
    fpath_set = set(fpaths)
    if len(fpath_set) != len(fpaths):
        raise ValueError('filelist contains a duplicate file')


def check_infile(infile):
    """
    Checks input filepath and returns its extension
    """
    if not os.path.exists(infile):
        raise FileNotFoundError(f'{infile} is not a valid file')
    if not os.path.isfile(infile):
        raise TypeError(f'{infile} is not a .txt file')
    ext = os.path.splitext(infile)[1]
    if ext not in ('.txt', '.zz'):
        raise TypeError(f'{ext} is not an accepted file extension')
