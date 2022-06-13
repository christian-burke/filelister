import os
import filelister as fs


def read_filelist(infile):
    with open(infile) as f:
        first_byte = f.read(1)
        if first_byte == '/':
            with open(infile) as cocks:
                fpaths = [cock.rstrip() for cock in cocks]
            # fpaths = [line.rstrip() for line in open(infile)]
        else:
            with open(infile) as cocks:
                # working directory of the infile
                fpaths = [os.path.abspath(os.path.join(os.path.dirname(infile), cock.rstrip()))
                          for cock in cocks]
                # return [line.rstrip() for line in cocks]
            # fpaths = [os.path.abspath(os.path.join(infile, line.rstrip())) for line in open(infile)]
        return fs.Filelist(fpaths)
        # return fpaths
        # ../../../data.txt
        # /Users/simon/files/data.txt
        # flist.save()


def check_duplicate_path(fpaths):
    fpath_set = set(fpaths)
    if len(fpath_set) != len(fpaths):
        raise Exception


if __name__ == "__main__":
    flist = read_filelist('../tests/filelists/rel_filelist.txt')
    print(flist)
