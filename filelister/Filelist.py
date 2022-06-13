"""Class build to handle Filelists"""

import os


class Filelist:
    """Main class contains most functions"""
    def __init__(self, data=None):
        if data:
            self.data = self.accept_input(data)
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
        except TypeError:
            raise TypeError(f'{type(other)} is an invalid input type')

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
        except TypeError:
            raise TypeError(f'{type(other)} is an invalid input type')

    def __str__(self):
        if self.data:
            str_out = 'printing filelist...'
            for fname in self.data:
                str_out += '\n' + fname
            return str_out
        return 'Filelist is empty'

    def accept_input(self, data):
        """Handles acceptable input types"""
        if isinstance(data, list):
            return self.create_from_list(data)
        if isinstance(data, set):
            return self.create_from_set(data)
        if isinstance(data, tuple):
            return self.create_from_tuple(data)
        if not data:
            return None
        return

    def create_from_list(self, data):
        """Handles list inputs for Filelist"""
        try:
            if data[0][0] == '/':
                return data
            return [self.relative_to_abs(fname) for fname in data]
        except TypeError:
            raise TypeError('data contains non-string type')

    def create_from_set(self, data):
        """Handles set input for Filelist"""
        if data[0][0] == '/':
            return list(data)
        else:
            return [self.relative_to_abs(fname) for fname in data]

    def create_from_tuple(self, data):
        """Handles tuple inputs for Filelist"""
        if data[0][0] == '/':
            return data
        else:
            return [self.relative_to_abs(fname) for fname in data]

    def relative_to_abs(self, path):
        """
        Convert a relative path from current working
        directory to an absolute path
        """
        return os.path.abspath(os.path.join(os.getcwd(), path))

    def save(self, outfile='filelist.txt', relative=False):
        """
        Writes filelist to a text file
        """
        with open(outfile, 'w', encoding='utf-8') as f:
            for fname in self.data:
                if relative:
                    p = os.path.relpath(fname, start=os.path.dirname(outfile))
                else:
                    p = os.path.abspath(fname)
                f.write(str(p) + os.linesep)
            print(f'filelist written to {outfile}')

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
        except TypeError:
            raise TypeError(f'{type(other)} is an invalid input type')

    def difference(self, other):
        """
        Finds difference between two filelists
        """
        set1 = set(self.data)
        try:
            if isinstance(other, Filelist):
                set2 = set(other.data)
            else:
                set2 = set(other)
            return set1.difference(set2)
        except TypeError:
            raise TypeError(f'{type(other)} is an invalid input type')

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
        except TypeError:
            raise TypeError(f'{type(other)} is an invalid input type')
