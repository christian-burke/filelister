"""
functions to read filelists from text file and store in Filelist class
"""


import os
import filelister as fs


def read_filelist(infile, check_exists=True):
    """
    reads a filelist from a text file and stores it in Filelist class
    """
    try:
        check_infile(infile)
        fpaths = []
        exts = set()
        with open(infile, encoding='utf-8') as f:
            for fname in f:
                exts.add(os.path.splitext(fname)[1].rstrip())
                fpaths.append(os.path.abspath(os.path.join(os.path.dirname(infile),
                                                           fname.rstrip())))
            return fs.Filelist(fpaths, allowed_exts=list(exts), check_exists=check_exists)
    except Exception as e:
        raise e


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
    if ext != '.txt':
        raise TypeError(f'{ext} is not an accepted file extension')
