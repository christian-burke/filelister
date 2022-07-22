"""
Class to handle Filelists
"""
import os
import zlib

from termcolor import colored


class Filelist:
    """
    Filelist class for creating, manipulating, comparing, and exporting filelists.

    # TODO: UPDATE DOCS
    Main organizational issues:
        - order of class methods?
        - make sure our imports are done correctly

     Bonus features:
         - write_filelist would be a nice command line function
         - set ops w order
         - improve validation runtime
         - dev version for lightweight filelist ops
    """

    def __init__(self, input_data=None):
        self._curr_commpfx = ""  # default common prefix (path)
        self._abs_commpfx = ""  # absolute common prefix (path)
        self._rel_commpfx = ""  # relative common prefix (path)

        self._data = []  # uncommon postfixes
        self._lookup_table = {}  # lookup table: uncommon postfix -> num occurrences

        if isinstance(input_data, Filelist):
            raise TypeError(f"{input_data} is already a Filelist")

        if not isinstance(input_data, (list, set, tuple, str)):
            raise TypeError(f"Invalid input type: {type(input_data)}")

        if isinstance(input_data, (list, set, tuple)):
            self.__build_internal(list(input_data))

        if isinstance(input_data, str):
            try:
                if not os.path.isdir(input_data):
                    raise FileNotFoundError(f"{input_data} is not a directory")
                tmp = []
                for path, _, files in os.walk(input_data):
                    for filename in files:
                        tmp.append(path + os.sep + filename)
                self.__build_internal(tmp)
            except Exception as e:
                raise e

    def __build_internal(self, input_data):
        """builds the internals"""
        self._curr_commpfx = os.path.dirname(os.path.commonprefix(input_data))
        if not self._curr_commpfx == "":  # TODO: review
            self._abs_commpfx = os.path.abspath(self._curr_commpfx)
            self._rel_commpfx = os.path.relpath(self._curr_commpfx, start=os.getcwd())
        for filename in input_data:
            self._data.append(filename)
            self.__add_entry_to_lookup(self.__truncate(filename))

    @property
    def data(self):
        """
        data property getter method
        """
        return self._data

    def __iter__(self):
        return iter(
            self.data
        )  # TODO: best practices for using self.data vs. self._data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if not isinstance(idx, (int, slice)):
            raise TypeError(f"Don't do that")
        if isinstance(idx, int):
            return self.data[idx]  # TODO: catch idx out of range
        if isinstance(idx, slice):
            return Filelist(self.data[idx])

    def __str__(self):
        if self._data:
            str_out = ""
            for fname in self.data:
                str_out += "\n" + fname
            return colored(str_out, "cyan")
        return colored("Empty Filelist", "red")

    def __repr__(self):
        return colored(f"Filelist({str(self._data)})", "cyan")

    def to_list(self):
        """returns filelist as python list"""
        return self.data

    def is_abs(self):
        return self._curr_commpfx[0] == "/"

    def is_rel(self):
        return not self.is_abs()

    def to_abs(self):
        if self.is_abs():  # TODO: return self
            raise TypeError("Filelist is already absolute")
        copy_flist = self.__copy_self()
        copy_flist._change_curr_prefix(copy_flist._abs_commpfx)
        return copy_flist

    def to_rel(self):
        if self.is_rel():  # TODO: return self?
            raise TypeError("Filelist is already relative")
        copy_flist = self.__copy_self()
        copy_flist._change_curr_prefix(copy_flist._rel_commpfx)
        return copy_flist

    def __add_entry_to_lookup(self, filename):
        if filename not in self._lookup_table:
            self._lookup_table[filename] = 1
        else:
            self._lookup_table[filename] += 1

    def __truncate(self, filepath, prefix=None):
        if prefix is None:
            prefix = self._curr_commpfx
        return filepath[len(prefix) + 1 :]  # +1 for "/" TODO: broken if pfx ""?

    def __copy_self(self):
        copy_flist = Empty()
        copy_flist.__class__ = Filelist
        copy_flist.__dict__ = self.__dict__.copy()
        return copy_flist

    def _change_curr_prefix(self, prefix):
        self._data = [  # TODO: weird required input
            prefix + fpath[len(self._curr_commpfx) :] for fpath in self._data
        ]
        self._curr_commpfx = prefix

    def contains(self, filename):
        """
        Returns True if the filelist contains a given filename.
        """
        if not isinstance(filename, str):
            raise TypeError("Invalid input: filename must be a string")

        def check_abs_in():
            return filename.startswith(self._abs_commpfx)

        def check_rel_in():
            return filename.startswith(self._rel_commpfx)

        if self.is_abs():
            if check_abs_in():
                return self.__truncate(filename) in self._lookup_table
            if check_rel_in():
                return (
                    self.__truncate(filename, self._rel_commpfx) in self._lookup_table
                )
        else:
            if check_rel_in():
                return self.__truncate(filename) in self._lookup_table
            if check_abs_in():
                return (
                    self.__truncate(filename, self._abs_commpfx) in self._lookup_table
                )
        return False

    def save(self, outfile="filelist.txt", relative=False, compressed=False):
        """
        functionality:
        `abs`: save outpaths as abspaths
        `rel`: save outpaths as relpaths, relative to outfile unless otherwise specified
        `nopath`: save outpaths with no context

        Writes a filelist to a txt file
        outfile: the output filename
        relative (resolve): whether or not to resolve the filepaths to originate from the outfile location
            errors with no context
            warns + converts to relpath with abspath
            resolves with relpath
        compressed (compress): whether or not to compress the outfile
        """
        out_data = (
            self.normalize_paths("abs", outfile)
            if not relative
            else self.normalize_paths("rel", outfile)
        )

        if compressed:
            with open(outfile, "wb") as f:
                out_data = self.compress(out_data)
                f.write(out_data)
        else:
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(os.linesep.join(out_data))

    def normalize_paths(self, output_type, outfile):
        """
        normalize filepaths
        output_type: abs or rel filepath
        outfile: path to output file
        """
        if output_type == "abs":
            # if absolute output, compute abs pfx, strip commpfx and strcat abspfx and truncated fpath
            if self.is_abs():
                return (
                    self._data
                )  # not necessary but nice to insta return if abs to abs
            return [
                self._abs_commpfx + fname[len(self._curr_commpfx) :]
                for fname in self._data
            ]

        # if rel output, compute rel pfx from deisred start location, strip commpfx, strcat relpfx and truncated fpath
        if output_type == "rel":
            out_pfx = os.path.relpath(
                self._curr_commpfx,
                start=os.path.dirname(outfile),
            )
            return [out_pfx + fname[len(self._curr_commpfx) :] for fname in self._data]
        # return self._data

    def compress(self, data):
        """
        compresses a filelist to be written to a text file
        """
        zdict = os.path.commonprefix(data).encode("utf-8")
        obj = zlib.compressobj(level=1, memLevel=9, zdict=zdict)
        data = ",".join(data).encode("utf-8")
        data_zip = obj.compress(data)
        data_zip += obj.flush()
        data_zip = zdict + b"\n" + data_zip
        return data_zip


class Empty:
    """Empty class used for copying a new Filelist"""

    pass
