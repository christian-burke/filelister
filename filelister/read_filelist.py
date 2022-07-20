"""
functions to read filelists from text file and store in Filelist class
"""

import os
import zlib

from .Filelist import Filelist


def process_data(dirname, fname):
    """
    process relative filepaths
    """
    return os.path.abspath(os.path.join(dirname, fname.rstrip()))


def read_filelist(infile, check_exists=False, compressed=False, allowed_exts=None):
    """
    reads filelist from a .txt or .zz file
    run with relative=False and validate=False to improve runtime
    """

    try:
        check_infile(infile)

        if compressed:
            data = read_compressed(infile)
        else:
            data = read_uncompressed(infile)

        dirname = os.path.dirname(infile)
        common_path = os.path.dirname(os.path.commonprefix(data))
        abs_common_path = os.path.abspath(os.path.join(dirname, common_path))

        def join_paths(fname):
            if fname[0] == "/":
                return fname
            return abs_common_path + fname[len(common_path) :]

        data = [join_paths(fname).rstrip() for fname in data]
        return Filelist(
            data,
            allowed_exts=allowed_exts,
            check_exists=check_exists,
        )

    except Exception as e:
        raise e


def read_compressed(infile):
    """
    reads a compressed filelist
    """
    with open(infile, "rb") as f:
        zdict = f.readline().strip()
        data = f.read()
    obj = zlib.decompressobj(zdict=zdict)
    data = obj.decompress(data)
    data += obj.flush()

    data = data.decode("utf-8").split(",")
    return data


def read_uncompressed(infile):
    """
    reads an uncompressed filelist
    """
    with open(infile, encoding="utf-8") as f:
        return f.read().rstrip().split("\n")


def check_infile(infile):
    """
    Checks input filepath and returns its extension
    """
    if not os.path.exists(infile):
        raise FileNotFoundError(f"{infile} is not a valid file")
    if not os.path.isfile(infile):
        raise TypeError(f"{infile} is not a .txt file")
    ext = os.path.splitext(infile)[1]
    if ext not in (".txt", ".zz"):
        raise TypeError(f"{ext} is not an accepted file extension")
