"""
functions to read filelists from text file and store in Filelist class
"""


import os
import filelister as fs


def read_filelist(infile, ext=[], exists=False):
    """
    reads a filelist from a text file and stores it in Filelist class
    """
    try:
        check_infile(infile)
        with open(infile, encoding='utf-8') as f:
            first_byte = f.read(1)
            f.seek(0,0)
            if first_byte == '/':
                fpaths = [fpath.rstrip() for fpath in f]
            else:
                # working directory of the infile
                fpaths = [os.path.abspath(os.path.join(os.path.dirname(infile),
                                                       fpath.rstrip()))
                    for fpath in f]
            check_duplicate_path(fpaths)
            return fs.Filelist(fpaths, ext=ext, exists=exists)
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

if __name__ == "__main__":
    flist = read_filelist('../tests/filelists/filelist.csv')
    print(flist)
