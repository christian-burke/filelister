"""
Class build to handle Filelists
"""
import os
import zlib

from termcolor import colored


class Filelist:
    """
    Filelist class for creating, manipulating, comparing, and exporting filelists.

    # TODO: UPDATE DOCS
    # _data for program always abs, view_data which can be abs or rel for programmer
    Main organizational issues:
        - multiprocessing as a solution to inefficient code FIXED
        - extraneous printing (even if its colorful :'( )
        - os.path can be very slow if you're running it 3 mil times FIXED
        - order of class methods?
        - make sure our imports are done correctly
        - lookup dict without impacting runtime? FIXED
        - too many optional args

     Bonus features:
         - write_filelist would be a nice command line function
         - set ops w order
         - improve validation runtime
         - dev version for lightweight filelist ops

    """
    # flist = Filelist("...")
    # flist.validate()

    def __init__(
        self,
        input_data=None
    ):
        self._curr_commpfx  # default common prefix (path)
        self._abs_commpfx = ""  # absolute common prefix (path)
        self._rel_commpfx = ""  # relative common prefix (path)

        self._data = []  # uncommon postfixes
        self._lookup_table = {}  # lookup table: uncommon postfix -> num occurrences

        if isinstance(input_data, Filelist):
            raise TypeError(f"{input_data} is already a Filelist")

        if not isinstance(input_data, (list, set, tuple, str, type(None))):
            raise TypeError(f"Invalid input type: {type(input_data)}")

        if isinstance(input_data, (list, set, tuple)):
            self.__build_internal(input_data)

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
        if not self._curr_commpfx == "":
            self._abs_commpfx = os.path.abspath(self._curr_commpfx)
            self._rel_commpfx = os.path.relpath(self._curr_commpfx, start=os.getcwd())
        for filename in input_data:
            # trimmed_filename = filename[len(self._curr_commpfx) :]
            self._data.append(filename)
            self.__add_entry_to_lookup(self.__truncate(filename))

    def __add_entry_to_lookup(self, filename):  # lazy lookup table
        if filename not in self._lookup_table:
            self._lookup_table[filename] = 1
        else:
            self._lookup_table[filename] += 1

    def __remove_entry_from_lookup(self, filename):  # lazy lookup table
        if filename not in self._lookup_table:
            pass
        else:
            self._lookup_table[filename] -= 1
            if self._lookup_table[filename] == 0:
                self._lookup_table.remove(filename)

    def __truncate(self, filepath):
        return filepath[len(self._curr_commpfx) :]

    def to_abs(self): # Should work... probably
        if self.is_abs():
            return # raise?
        abs_flist = Filelist()
        abs_flist._data = [self._abs_commpfx + fname[self._curr_commpfx :] for fname in self._data]
        abs_flist._curr_commpfx = self._abs_commpfx
        abs_flist._abs_commpfx = self._abs_commpfx
        abs_flist._rel_commpfx = self._rel_commpfx
        return abs_flist

    @property
    def data(self):
        """
        data property getter method
        """
        return self._data

    def is_abs(self):
        return self._curr_commpfx[0] == "/"

    def is_rel(self):
        return not self.is_abs()

    def __add__(self, input_data):
        try:
            if isinstance(input_data, str):
                raise TypeError(f"Cannot add a string to a Filelist")
            if not isinstance(input_data, Filelist):
                input_data = Filelist(input_data)
            
            op1 = self.data if self.is_abs() else self.to_abs().data
            op2 = input_data.data if input_data.is_abs() else input_data.to_abs().data

            return Filelist(op1 + op2)
        except Exception as e:
            raise e

    def __iadd__(self, other):
        try:
            other_data = check_and_format_operand_input(other)
            curr_idx = len(self._data) - 1
            for idx, filename in enumerate(other_data):
                self.__add_entry_to_lookup(filename, idx + curr_idx)
                curr_idx += 1
            self._data += other_data
            return self
        except Exception as e:
            raise e

    def __sub__(self, other):
        try:
            other_data = check_and_format_operand_input(other)
            return Filelist([fname for fname in self._data if fname not in other_data])
        except Exception as e:
            raise e

    # def __isub__(self, other):
    #     try:
    #         other_data = check_and_format_operand_input(other)
    #         new_flist = self - other
    #         self._data = new_flist.data
    #         self._lookup_table = new_flist._lookup_table
    #         return self
    #     except Exception as e:
    #         raise e

    def __iter__(self):
        return iter(self.data)  # TODO: best practices for using self.data vs. self._data

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
            # str_out = colored("printing filelist...", "blue")
            for fname in self.data:
                str_out += colored("\n" + fname, "cyan")
            return str_out
        return "Empty Filelist"

    # def __sorted__(self):
    #     return Filelist(self._data).sort()

    # def sort(self):
    #     """
    #     Sorts a filelist
    #     """
    #     self._data.sort()

    def tolist(self):
        """returns filelist as python list"""
        return self.data

    def contains(self, filename):
        """
        Returns True if the filelist contains a given filename.
        """
        if not isinstance(filename, str):
            raise TypeError("Invalid input: filename must be a string")
        # if filename[0] != "/":
        #     filename = relative_to_abs(filename)
        return filename in self._lookup_table

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
        # check if relative
        # normalize data
        # save compressed/uncompressed
        data = self._data.copy()  # necessary?

        if self.is_abs():
            pass

        if relative:
            data = abs_to_rel_list(data, os.path.dirname(outfile))
        if compressed:
            with open(outfile, "wb") as f:
                data = compress(self.data)
                f.write(data)

        else:
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(os.linesep.join(data))

    def view(self, relative=True):
        """Prints data"""
        if relative:
            read_data = [abs_to_rel(path) for path in self.data]
        else:
            read_data = self.data
        for path in read_data:
            print(path)

    def compare(self, other):
        """
        Compares two filelists, returning the differences between the lists
        """
        set_diff = {}
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            set_diff["+"] = set(self.data).difference(set(other.data))
            set_diff["-"] = set(other.data).difference(set(self.data))
            for diff in set_diff["+"]:
                print(colored(f"[ + ] {diff}", "green"))
            for diff in set_diff["-"]:
                print(colored(f"[ - ] {diff}", "red"))
            return set_diff
        except Exception as e:
            raise e

    def union(self, other):
        """
        Finds union of two filelists
        """
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            return set(self.data).union(set(other.data))
        # NOTE: order not guaranteed
        except Exception as e:
            raise e

    def difference(self, other):
        """
        Finds difference between two filelists
        """
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            return set(self.data).difference(set(other.data))
        except Exception as e:
            raise e

    def intersection(self, other):
        """
        Finds intersection of two filelists
        """
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            return set(self.data).intersection(set(other.data))
        except Exception as e:
            raise e

    def isdisjoint(self, other):
        """
        Finds intersection of two filelists
        """
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            return set(self.data).isdisjoint(set(other.data))
        except Exception as e:
            raise e

    def issubset(self, other):
        """
        Finds intersection of two filelists
        """
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            return set(self.data).issubset(set(other.data))
        except Exception as e:
            raise e

    def issuperset(self, other):
        """
        Finds intersection of two filelists
        """
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            return set(self.data).issuperset(set(other.data))
        except Exception as e:
            raise e

    def symmetric_difference(self, other):
        """
        Finds intersection of two filelists
        """
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            return set(self.data).symmetric_difference(set(other.data))
        except Exception as e:
            raise e


def validate_user_inputs(data, exts, exists):
    """
    User input validation
    """
    accepted_data_types = [list, set, tuple, str, Filelist, type(None)]
    # remove None?
    if type(data) not in accepted_data_types:
        raise TypeError(f"Invalid input type: {type(data)}")
    if not isinstance(exts, list):
        raise TypeError("Invalid input type: allowed_exts must be of type list")
    # check file exts passed
    if not isinstance(exists, bool):
        raise TypeError("Invalid input type: check_exists must be of type bool")


def validate_data(data, exts, exists, check_exts):
    """
    converts data to acceptable list format
    """
    try:
        data = format_input(data)
        exts = {ext: None for ext in exts}
        if not data:
            return {"data": [], "dict": {}}  # should error instead?
        valid_data = []
        common_path = os.path.dirname(os.path.commonprefix(data))
        abs_common_path = os.path.abspath(os.path.join(os.getcwd(), common_path))
        lookup_dict = {}

        for idx, filename in enumerate(data):
            if exists:
                check_file_exists(filename)  # should be try-catch

            if check_exts:
                if os.path.splitext(filename)[1] not in exts:
                    raise TypeError(f"Bad file type: {filename}")

            if not filename[0] == "/":  # unexpected functionality -> input is intermixed abs + rel?
                filename = abs_common_path + filename[len(common_path) :]

            if filename not in lookup_dict:  # internal without validation -> filename: [idx0, idx1, ...]
                lookup_dict[filename] = idx
                valid_data.append(filename)

        return {"data": valid_data, "dict": lookup_dict}

    except Exception as e:
        raise e


def check_file_exists(fname):
    if not os.path.isfile(fname):
        raise FileNotFoundError(f"File Not Found: {fname}")


def is_ok_operand_type(input):
    """
    determines if the input is ok for operand types
    """
    if not isinstance(input, (list, set, tuple, Filelist)):
        return False
    return True

def check_and_format_operand_input(input_data):
    """
    formats user input for operand operations
    """
    if not is_ok_operand_type(input_data):
        raise TypeError(f"Invalid input type: {type(input_data)}")

    if isinstance(input_data, Filelist):
        return Filelist.data

    if isinstance(input_data, (list, set, tuple)):
        return list(input_data)

    # if isinstance(input_data, str):
    #     try:
    #         builder = Filelist(input_data)
    #         return builder.data
    #     except Exception as e:
    #         raise e


def read_dir(data):
    """
    Handles directory inputs for Filelist
    """
    try:
        data_out = []
        for path, _, files in os.walk(data):
            for filename in files:
                data_out.append(os.path.abspath(os.path.join(path, filename)))
        return data_out
    except Exception as e:
        raise e


def relative_to_abs(path):
    """
    Convert a relative path from cwd to an absolute path
    """
    return os.path.abspath(os.path.join(os.getcwd(), path))


def abs_to_rel(path):
    """
    Convert an absolute path to a relative path
    """
    return os.path.relpath(path, start=os.getcwd())


def write_filelist(
    dirname,
    outfile,
    relative=True,
    compressed=False,
    allowed_exts=None,
):
    """
    writes a filelist for a given directory
    """
    if allowed_exts is None:
        allowed_exts = [".jpg", ".png", ".txt"]
    flist = Filelist(dirname, allowed_exts=allowed_exts, check_exists=False)
    flist.save(outfile, relative=relative, compressed=compressed)


def compress(data):
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




def abs_to_rel_list(data, start):
    """converts absolute list to relative list for Filelist.save()"""

    common_path = os.path.dirname(os.path.commonprefix(data))
    rel_common_path = os.path.relpath(common_path, start=start)
    return [rel_common_path + fname[len(common_path) :] for fname in data]
