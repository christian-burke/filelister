import os
import Filelist as fs

def read_filelist(infile):
    with open(infile) as f:
        first_byte = f.read(1)
        if first_byte == '/':
            with open(infile) as cocks:
                return [line.rstrip() for line in cocks]
            # fpaths = [line.rstrip() for line in open(infile)]
        else:
            with open(infile) as cocks:
                # working directory of the infile
                return [os.path.abspath(os.path.join(infile, line.rstrip())) for line in cocks]
                # return [line.rstrip() for line in cocks]
            # fpaths = [os.path.abspath(os.path.join(infile, line.rstrip())) for line in open(infile)]
        raise
        # return fpaths
        # ../../../data.txt
        # /Users/simon/files/data.txt
        # flist.save()


def check_duplicate_path(fpaths):
    fpath_set = set(fpaths)
    if len(fpath_set) != len(fpaths):
        raise Error


if __name__ == "__main__":
    flist = read_filelist('../tests/filelists/rel_filelist.txt')
    print(flist)
