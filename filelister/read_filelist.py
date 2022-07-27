"""
functions to read filelists from text file and store in Filelist class
"""

import os
import zlib

from termcolor import colored

from .Filelist import Filelist


def read_filelist(infile, compressed=False):
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
        if data[0][0] == "/":
            data = [fpath.rstrip() for fpath in data]
        else:
            dirname = os.path.dirname(infile)
            in_comm_pfx = os.path.dirname(os.path.commonprefix(data))
            out_comm_pfx = os.path.relpath(
                os.path.abspath(os.path.join(dirname, in_comm_pfx)),
                start=os.getcwd(),
            )
            if out_comm_pfx == ".":
                out_comm_pfx = ""
            if not in_comm_pfx and out_comm_pfx:

                data = [
                    (out_comm_pfx + "/" + fpath[len(in_comm_pfx) :]).rstrip()
                    for fpath in data
                ]
            data = [
                (out_comm_pfx + fpath[len(in_comm_pfx) :]).rstrip() for fpath in data
            ]
        return Filelist(data)

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
        return f.read().rstrip().split(os.linesep)


def check_infile(infile):
    """
    Checks input filepath and returns its extension
    """
    if not os.path.exists(infile):
        raise FileNotFoundError(colored(f"{infile} not found", "red"))
    if not os.path.isfile(infile):
        raise TypeError(colored(f"{infile} is not a valid file", "red"))
    ext = os.path.splitext(infile)[1]
    if ext not in (".txt", ".zz"):
        raise TypeError(colored(f"{ext} is not an accepted file extension"))
