"""
Class build to handle Filelists
"""

import os
from termcolor import colored


class Filelist:
    """
    Filelist class for creating, manipulating, comparing, and exporting filelists.

    # TODO: Idea, make a view() that can be set to abs or relative
    # _data for program always abs, view_data which can be abs or rel for programmer
    # add list methods with maintained order (no cast to set)?
    """

    def __init__(self, data=None, allowed_exts=['.jpg', '.png', '.txt'], check_exists=True):
        validate_user_inputs(data, allowed_exts, check_exists)
        try:
            self._allowed_exts = allowed_exts
            self._check_exists = check_exists
            self._data = validate_data(data, allowed_exts, check_exists)
        except Exception as e:
            raise e

    @property
    def data(self):
        """
        data property and setter method
        """
        return self._data

    @data.setter
    def data(self, data):
        self._data = validate_data(data, self._allowed_exts, self._check_exists)

    def __add__(self, other):
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            return Filelist(self.union(other))
        except Exception as e:
            raise e

    def __iadd__(self, other):
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            new_flist = self + other
            self._data = new_flist.data
            return self
        except Exception as e:
            raise e

    def __sub__(self, other):
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            return Filelist(self.difference(other))
        except Exception as e:
            raise e

    def __isub__(self, other):
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            new_flist = self - other
            self._data = new_flist.data
            return self
        except Exception as e:
            raise e

    def __str__(self):
        if self._data:
            str_out = colored('printing filelist...', 'blue')
            for fname in self.data:
                str_out += '\n' + fname
            return str_out
        return 'Empty Filelist'

    def __sorted__(self):
        return Filelist(self._data).sort()

    def save(self, outfile='filelist.txt', relative=False):
        """
        Writes filelist to a text file
        """
        with open(outfile, 'w', encoding='utf-8') as f:
            for fname in self.data:
                if relative:
                    path = os.path.relpath(fname,
                                           start=os.path.dirname(outfile))
                else:
                    path = os.path.abspath(fname)
                f.write(str(path) + os.linesep)
            print(colored(f'filelist written to {outfile}', 'green'))

    def compare(self, other):
        """
        Compares two filelists, returning the differences between the lists
        """
        set_diff = {}
        try:
            if not isinstance(other, Filelist):
                other = Filelist(other)
            set_diff['+'] = set(self.data).difference(set(other.data))
            set_diff['-'] = set(other.data).difference(set(self.data))
            for diff in set_diff['+']:
                print(colored(f'[ + ] {diff}', 'green'))
            for diff in set_diff['-']:
                print(colored(f'[ - ] {diff}', 'red'))
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
            return set(self.data).union(set(other.data))  # NOTE: order not guaranteed
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

    def sort(self):
        """
        Sorts a filelist
        """
        self._data.sort()


def validate_user_inputs(data, exts, exists):
    accepted_data_types = [list, set, tuple, str, Filelist, type(None)]  # remove None?
    if type(data) not in accepted_data_types:
        raise TypeError(f'Invalid input type: {type(data)}')
    if not isinstance(exts, list):
        raise TypeError('Invalid input type: allowed_exts must be of type list')
    # check file exts passed
    if not isinstance(exists, bool):
        raise TypeError('Invalid input type: check_exists must be of type bool')


def validate_data(data, exts, exists):
    try:
        data = format_input(data)
        if not data:
            return data
        is_abs = data[0][0] == '/'
        valid_data = []
        for filename in data:
            if exists:
                if not os.path.isfile(filename):
                    raise FileNotFoundError(f'File Not Found: {filename}')
            if os.path.splitext(filename)[1] not in exts:
                raise TypeError(f'Bad file type: {filename}')
            if not is_abs:
                filename = relative_to_abs(filename)
            valid_data.append(filename)
        return valid_data
    except Exception as e:
        raise e


def format_input(data):
    if isinstance(data, type(None)):  # empty Filelist?
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, (set, tuple)):
        return list(data)
    if isinstance(data, Filelist):
        return data.data
    if isinstance(data, str):
        if os.path.isfile(data):
            return [os.path.abspath(data)]
        if os.path.isdir(data):
            return read_dir(data)
        raise FileNotFoundError(f'File Not Found: {data}')
    raise TypeError(f'Invalid input type: {type(data)}')


def read_dir(data):
    """
    Handles directory inputs for Filelist
    """
    try:
        data_out = []
        for path, _, files in os.walk(data):
            for filename in files:
                data_out.append(
                    os.path.abspath(os.path.join(path, filename))
                )
        return data_out
    except Exception as e:
        raise e


def relative_to_abs(path):
    """
    Convert a relative path from cwd to an absolute path
    """
    return os.path.abspath(os.path.join(os.getcwd(), path))


def write_filelist(dirname,
                   outfile,
                   relative=True,
                   allowed_exts=['.jpg', '.png', '.txt'],
                   check_exists=True):
    flist = Filelist(dirname, allowed_exts=allowed_exts, check_exists=check_exists)
    flist.save(outfile, relative)
