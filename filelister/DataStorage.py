"""DataStorage class"""
from ctypes import c_wchar_p

from termcolor import colored


class DataStorage:
    """Class to store Filelist data"""

    def __init__(self, loader):
        self.paths = []
        self.lookup = {}
        self.curr_idx = 0

        for abs_path, rel_path in loader:
            if abs_path in self.lookup or rel_path in self.lookup:
                print(colored("WARN: Path is already stored. Skipping.", "red"))
                continue
            abs_ptr = c_wchar_p(abs_path)
            rel_ptr = c_wchar_p(rel_path)
            self.paths.append((abs_ptr, rel_ptr))
            self.lookup[abs_path] = (abs_ptr, len(self.paths) - 1)
            self.lookup[rel_path] = (rel_ptr, len(self.paths) - 1)

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__unpack_ptr_values(key)
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self.paths))
            return [self.__unpack_ptr_values(idx) for idx in range(start, stop, step)]
        raise TypeError(f"indices must be integers or slices, not {type(key)}")

    def __unpack_ptr_values(self, index):
        abs_ptr, rel_ptr = self.paths[index]
        return abs_ptr.value, rel_ptr.value

    def __contains__(self, value):
        return value in self.lookup

    def index(self, value):
        """Returns the index of value in DataStorage"""
        if value in self.lookup:
            return self.lookup[value][1]
        raise ValueError(f"{value} is not in DataStorage")

    def count(self, value):
        """Returns the number of occurrences of value in DataStorage"""
        return 1 if value in self.lookup else 0
