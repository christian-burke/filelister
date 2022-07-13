"""
functions to read filelists from text file and store in Filelist class
"""

import time
import os
from .Filelist import Filelist, validate_data
import zlib
from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing import Pool



def process_data(dirname, fname, relative=False):
    # if check_exts:
        # exts.add(os.path.splitext(fname)[1].rstrip())
    #if relative:

        return os.path.abspath(os.path.join(dirname, fname.rstrip()))




def read_filelist(infile, check_exists=False, compressed=False, allowed_exts=None):
    try:
        check_infile(infile)
        if compressed:
            flist = read_compressed(infile)
        else:
            flist = read_uncompressed(infile)
        dirname = os.path.abspath(os.path.dirname(infile))

        with Pool(cpu_count()) as pool:
            data = pool.starmap(process_data, zip(repeat(dirname), flist))
        data = validate_data(data, allowed_exts, check_exists, False)
        out = Filelist(None, allowed_exts=allowed_exts,
                           check_exists=check_exists)
        out._data = data
        return out
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
        return f.read().rstrip().split('\n')


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
