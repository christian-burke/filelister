import os


class Filelist:
    def __init__(self, data=None):
        self.accept_input(data)

    def accept_input(self, data):
        if type(data) == list:
            return create_from_list(data)
        elif type(data) == dict:
            create_from_dict(data)

    def create_from_list(self, data):
        file_data = []
        for file in data:
            if file[0] == '/':
                file_data.append(file)
            else:
                file_data.append(self.relative_to_abs(file_abspath))

    def create_from_dict(data):
        pass #Why the fuck would you do this and how would you implement it?

    def relative_to_abs(path):
        return os.path.abspath(os.path.join(os.getcwd(), path))
