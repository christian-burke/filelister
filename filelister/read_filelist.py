"""
functions to read filelists from text file and store in Filelist class
"""


import os
import filelister as fs


def read_filelist(infile):
    """
    reads a filelist from a text file and stores it in Filelist class
    """
    with open(infile, encoding='utf-8') as f:
        first_byte = f.read(1)
        f.seek(0,0)
        if first_byte == '/':
            fpaths = [fpath.rstrip() for fpath in f]
            # fpaths = [line.rstrip() for line in open(infile)]
        else:
            # working directory of the infile
            fpaths = [os.path.abspath(os.path.join(os.path.dirname(infile), fpath.rstrip()))
                for fpath in f]
                # return [line.rstrip() for line in cocks]
            # fpaths = [os.path.abspath(os.path.join(infile, line.rstrip())) for line in open(infile)]
        return fs.Filelist(fpaths)


def check_duplicate_path(fpaths):
    """
    checks if there is a duplicte filepath in filelist
    """
    fpath_set = set(fpaths)
    if len(fpath_set) != len(fpaths):
        raise Exception


if __name__ == "__main__":
    flist = read_filelist('../tests/filelists/rel_filelist.txt')
    print(flist)
