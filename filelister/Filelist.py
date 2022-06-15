"""
Class build to handle Filelists
"""

import os
from termcolor import colored


class Filelist:
    """
    Main class contains most functions
    """

    def __init__(self, data=None):
        try:
            self.acceptable_types = [list, set, tuple, str,
                                     Filelist, type(None)]
            if type(data) not in self.acceptable_types:
                raise TypeError(f'{type(data)} is an invalid input type.')
            if data:
                self._data = accept_input(data)
            else:
                self._data = []
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
        if data:
            self._data = accept_input(data)
        else:
            self._data = []

    def __add__(self, other):
        try:
            if isinstance(other, Filelist):
                return Filelist(self.union(other))
            other_flist = Filelist(other)
            return Filelist(self.union(other_flist))
        except Exception as e:
            raise e

    def __iadd__(self, other):
        try:
            if isinstance(other, Filelist):
                new_flist = self + other
            else:
                other_flist = Filelist(other)
                new_flist = self + other_flist
            self.data = new_flist.data
            return self
        except Exception as e:
            raise e

    def __sub__(self, other):
        try:
            if isinstance(other, Filelist):
                return Filelist(self.difference(other))
            other_flist = Filelist(other)
            return Filelist(self.difference(other_flist))
        except Exception as e:
            raise e

    def __isub__(self, other):
        try:
            if isinstance(other, Filelist):
                new_flist = self - other
            else:
                other_flist = Filelist(other)
                new_flist = self - other_flist
            self.data = new_flist.data
            return self
        except Exception as e:
            raise e

    def __str__(self):
        if self._data:
            str_out = colored('printing filelist...', 'blue')
            for fname in self.data:
                str_out += '\n' + fname
            return str_out
        return 'Filelist is empty'

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
            print(f'filelist written to {outfile}')

    def compare(self, other):
        """
        Compares two filelists, returning the differences between the lists
        """
        set1 = set(self.data)
        set_diff = {}
        try:
            if isinstance(other, Filelist):
                set2_list = other
            else:
                set2_list = Filelist(other)
            set2 = set(set2_list.data)
            new_files = set1.difference(set2)
            removed_files = set2.difference(set1)
            if new_files:
                set_diff['+'] = new_files
            if removed_files:
                set_diff['-'] = removed_files
            for diff in set_diff['+']:
                print(colored(f'[+] {diff}', 'green'))
            for diff in set_diff['-']:
                print(colored(f'[-] {diff}', 'red'))
            return set_diff
        except Exception as e:
            raise e

    def union(self, other):
        """
        Finds union of two filelists
        """
        set1 = set(self.data)
        try:
            if isinstance(other, Filelist):
                set2_list = other
            else:
                set2_list = Filelist(other)
            return set1.union(set(set2_list.data))
        except Exception as e:
            raise e

    def difference(self, other):
        """
        Finds difference between two filelists
        """
        set1 = set(self.data)
        try:
            if isinstance(other, Filelist):
                set2_list = other
            else:
                set2_list = Filelist(other)
            return set1.difference(set(set2_list.data))
        except Exception as e:
            raise e

    def intersection(self, other):
        """
        Finds intersection of two filelists
        """
        set1 = set(self.data)
        try:
            if isinstance(other, Filelist):
                set2_list = other
            else:
                set2_list = Filelist(other)
            return set1.intersection(set(set2_list.data))
        except Exception as e:
            raise e

    def isdisjoint(self, other):
        """
        Finds intersection of two filelists
        """
        set1 = set(self.data)
        try:
            if isinstance(other, Filelist):
                set2_list = other
            else:
                set2_list = Filelist(other)
            return set1.isdisjoint(set(set2_list.data))
        except Exception as e:
            raise e

    def issubset(self, other):
        """
        Finds intersection of two filelists
        """
        set1 = set(self.data)
        try:
            if isinstance(other, Filelist):
                set2_list = other
            else:
                set2_list = Filelist(other)
            return set1.issubset(set(set2_list.data))
        except Exception as e:
            raise e

    def issuperset(self, other):
        """
        Finds intersection of two filelists
        """
        set1 = set(self.data)
        try:
            if isinstance(other, Filelist):
                set2_list = other
            else:
                set2_list = Filelist(other)
            return set1.issuperset(set(set2_list.data))
        except Exception as e:
            raise e

    def symmetric_difference(self, other):
        """
        Finds intersection of two filelists
        """
        set1 = set(self.data)
        try:
            if isinstance(other, Filelist):
                set2_list = other
            else:
                set2_list = Filelist(other)
            return set1.symmetric_difference(set(set2_list.data))
        except Exception as e:
            raise e

    def sort(self):
        """
        Sorts a filelist
        """
        self.data.sort()


def relative_to_abs(path):
    """
    Convert a relative path from current working
    directory to an absolute path
    """
    return os.path.abspath(os.path.join(os.getcwd(), path))


def accept_input(data):
    """
    Handles acceptable input types
    """
    if isinstance(data, list):
        return create_from_list(data)
    if isinstance(data, set):
        return create_from_set(data)
    if isinstance(data, tuple):
        return create_from_tuple(data)
    if isinstance(data, Filelist):
        return data.data
    if isinstance(data, str):
        if os.path.isdir(data):
            return create_from_dir(data)
        if os.path.isfile(data):
            return [os.path.abspath(data)]
        raise IOError(f'{data} does not match a valid file or directory')
    raise TypeError(f'{type(data)} is an invalid input type')


def create_from_list(data):
    """
    Handles list inputs for Filelist
    """
    try:
        for fname in data:
            if not os.path.isfile(fname):
                raise IOError(f'{fname} does not match a valid file')
        if data[0][0] == '/':
            return data
        return [relative_to_abs(fname) for fname in data]
    except TypeError as te:
        raise te


def create_from_set(data):
    """
    Handles set input for Filelist
    """
    data = list(data)
    for fname in data:
        if not os.path.isfile(fname):
            raise IOError(f'{fname} does not match a valid file')

    if data[0][0] == '/':
        return data
    return [relative_to_abs(fname) for fname in data]


def create_from_tuple(data):
    """
    Handles tuple inputs for Filelist
    """
    for fname in data:
        if not os.path.isfile(fname):
            raise IOError(f'{fname} does not match a valid file')
    if data[0][0] == '/':
        return list(data)
    return [relative_to_abs(fname) for fname in data]


def create_from_dir(data):
    """
    Handles directory inputs for Filelist
    """
    data_out = []
    for path, _, files in os.walk(data):
        for filename in files:
            fpath = os.path.abspath(os.path.join(path, filename))
            data_out.append(str(fpath))
    return data_out
