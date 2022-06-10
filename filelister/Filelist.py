import os


class Filelist:
    def __init__(self, data=None):
        if data:
            self.data = self.accept_input(data)
        elif type(data) not in [list, set, None]:
            raise TypeError(f'{type(data)} is an invalid input type.')
        else:
            self.data = None

    def __str__(self):
        if self.data:
            str_out = ''
            for fname in self.data:
                str_out += fname + '\n'
            return str_out
        else:
            return 'Filelist is empty'

    def accept_input(self, data):
        if type(data) == list:
            return self.create_from_list(data)
        elif type(data) == set:
            self.create_from_dict(data)
        elif type(data) == None:
            return None

    def create_from_list(self, data):
        if data[0][0] == '/':
            return data
        else:
            return [self.relative_to_abs(fname) for fname in data]

    def create_from_set(self, data):
        pass

    def relative_to_abs(self, path):
        return os.path.abspath(os.path.join(os.getcwd(), path))
