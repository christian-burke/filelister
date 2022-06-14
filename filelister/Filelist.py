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
        if data:
            self.data = accept_input(data)
        elif type(data) not in [list, set, tuple, None]:
            raise TypeError(f'{type(data)} is an invalid input type.')
        else:
            self.data = None

    def __add__(self, other):
        set1 = set(self.data)
        if isinstance(other, str):
            set1.add(other)
            return set1
        try:
            if isinstance(other, Filelist):
                set2 = set(other.data)
            else:
                set2 = set(other)
            return set1.union(set2)
        except TypeError as te:
            raise TypeError(f'{type(other)} is an invalid input type') from te

    def __iadd__(self, other):
        set1 = set(self.data)
        if isinstance(other, str):
            set1.add(other)
            self.data = list(set1)
        try:
            if isinstance(other, Filelist):
                set2 = set(other.data)
            else:
                set2 = set(other)
            self.data = list(set1.union(set2))
            return self
        except TypeError as te:
            raise TypeError(f'{type(other)} is an invalid input type') from te

    def __sub__(self, other):
        set1 = set(self.data)
        if isinstance(other, str):
            set1.remove(other)
            return set1
        try:
            if isinstance(other, Filelist):
                set2 = set(other.data)
            else:
                set2 = set(other)
            return set1.difference(set2)
        except TypeError as te:
            raise TypeError(f'{type(other)} is an invalid input type') from te

    def __str__(self):
        if self.data:
            str_out = 'printing filelist...'
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
                set2 = set(other.data)
            else:
                set2 = set(other)
            new_files = set1.difference(set2)
            removed_files = set2.difference(set1)
            set_diff['+'] = new_files
            set_diff['-'] = removed_files
            for diff in set_diff['+']:
                print(colored(f'[+] {diff}', 'green'))
            for diff in set_diff['-']:
                print(colored(f'[-] {diff}', 'red'))
            return set_diff
        except TypeError as te:
            raise TypeError(f'{type(other)} is an invalid input type') from te

    def union(self, other):
        """
        Finds union of two filelists
        """
        set1 = set(self.data)
        try:
            if isinstance(other, Filelist):
                set2 = set(other.data)
            else:
                set2 = set(other)
            return set1.union(set2)
        except TypeError as te:
            raise TypeError(f'{type(other)} is an invalid input type') from te

    def difference(self, other):
        """
        Finds difference between two filelists
        """
        set1=set(self.data)
        try:
            if isinstance(other, Filelist):
                set2 = set(other.data)
            else:
                set2 = set(other)
            return set1.difference(set2)
        except TypeError as te:
            raise TypeError(f'{type(other)} is an invalid input type') from te

    def intersection(self, other):
        """
        Finds intersection of two filelists
        """
        set1 = set(self.data)
        try:
            if isinstance(other, Filelist):
                set2 = set(other.data)
            else:
                set2 = set(other)
            return set1.intersection(set2)
        except TypeError as te:
            raise TypeError(f'{type(other)} is an invalid input type') from te

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
    if isinstance(data, str):
        if os.path.isdir(data):
            return create_from_dir(data)
        if os.path.isfile(data):
            return [data]
    if not data:
        return None
    raise TypeError(f'{type(data)} is an invalid input type')


def create_from_list(data):
    """
    Handles list inputs for Filelist
    """
    try:
        if data[0][0] == '/':
            return data
        return [relative_to_abs(fname) for fname in data]
    except TypeError as te:
        raise TypeError('data contains non-string type') from te


def create_from_set(data):
    """
    Handles set input for Filelist
    """
    data = list(data)
    if data[0][0] == '/':
        return data
    return [relative_to_abs(fname) for fname in data]


def create_from_tuple(data):
    """
    Handles tuple inputs for Filelist
    """
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
