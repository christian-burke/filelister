import os
import pytest
import filelister as fs

def rel_to_abs(path):
    return os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), path))


sample_data = ['data/sample_01.txt',
               'data/sample_02.txt',
               'data/sample_03.txt']
sample_data = [rel_to_abs(path)
               for path in sample_data]
sample_data2 = ['data/sample_03.txt', 'data/sample_04.txt', 'data/sample_05.txt']
sample_data2 = [rel_to_abs(path)
                for path in sample_data2]
rel_sample = [os.path.relpath(path, start = os.getcwd()) for path in sample_data]
rel_sample2 = [os.path.relpath(path, start = os.getcwd()) for path in sample_data2]

test_data2 = [os.path.abspath(test) for test in sample_data2]
test_data = [os.path.abspath(test) for test in sample_data]
test_set = set(test_data).union(set(test_data2))


class CreateFromType:

    def test_filelist_create_from_abs_list(self):
        flist = fs.Filelist(sample_data)
        assert set(flist.data) == set(test_data)


    def test_filelist_create_from_rel_list(self):
        flist = fs.Filelist(rel_sample)
        assert set(flist.data) == set(test_data)


    def test_filelist_create_from_bad_list(self):
        test = 'test_file'
        test_list = sample_data.copy()
        test_list.append(test)
        fs.Filelist(test_list)
        assert set(flist.data) == set(test_data)

    def test_filelist_create_from_abs_set(self):
        flist = fs.Filelist(set(test_data))
        assert set(flist.data) == set(test_data)

    def test_filelist_create_from_rel_set(self):
        flist = fs.Filelist(set(rel_sample))
        assert set(flist.data) == set(test_data)

    def test_filelist_create_from_dir(self):
        flist = fs.Filelist(rel_to_abs('data'))
        assert set(flist.data) == set(test_data).union(set(test_data2))

    def test_filelist_create_from_abs_tuple(self):
        flist = fs.Filelist(tuple(sample_data))
        assert set(flist.data) == set(test_data)

    def test_filelist_create_from_rel_tuple(self):
        flist = fs.Filelist(tuple(rel_sample))
        assert set(flist.data) == set(test_data)


class TestAdd:

    def test_filelist_add_filelist(self):
        flist = fs.Filelist(sample_data)
        flist2 = fs.Filelist(sample_data2)
        flist3 = flist + flist2
        assert set(flist3.data) == test_set

    def test_filelist_add_abs_string(self):
        flist = fs.Filelist(sample_data)
        flist3 = flist + str(rel_to_abs('data/sample_04.txt'))
        set1 = set(test_data)
        set1.add(os.path.abspath(rel_to_abs('data/sample_04.txt')))
        assert set(flist3.data) == set1

    def test_filelist_add_rel_string(self):
        flist = fs.Filelist(sample_data)
        flist3 = flist + str(os.path.relpath(rel_to_abs('data/sample_04.txt'), os.getcwd()))
        set1 = set(test_data)
        set1.add(os.path.abspath(rel_to_abs('data/sample_04.txt')))
        assert set(flist3.data) == set1

    def test_add_dir_string(self):
        flist = fs.Filelist(sample_data)
        flist3 = flist + str(os.path.relpath(rel_to_abs('data'), start=os.getcwd()))
        assert set(flist3.data) == test_set

    def test_filelist_add_bad_string(self):
        with pytest.raises(FileNotFoundError, match =
                           'File Not Found: hello world!'):
            flist = fs.Filelist(sample_data)
            flist + 'hello world!'

    def test_filelist_add_abs_list(self):
        flist = fs.Filelist(sample_data)
        flist2 = flist + sample_data2
        assert set(flist2.data) == test_set

    def test_filelist_add_rel_list(self):
        flist = fs.Filelist(rel_sample)
        flist2 = flist + rel_sample2
        assert set(flist2.data) == test_set


    def test_filelist_add_bad_list(self):
        test = str(rel_to_abs('test_file'))
        flist = fs.Filelist(sample_data)
        test_list = sample_data.copy()
        test_list.append(test)
        with pytest.raises(FileNotFoundError, match = f'File Not Found: {test}'):
            flist2 = flist + test_list
            assert set(flist2.data) == set(sample_data)

    def test_add_invalid(self):
        test = 5
        with pytest.raises(TypeError, match = f'Invalid input type: {type(test)}'):
            flist = fs.Filelist(sample_data)
            flist2 = flist + test


class TestSub:

    def test_sub_abs_string(self):
        flist = fs.Filelist(sample_data)
        flist2 = flist - str(sample_data[2])
        assert set(flist2.data) == set(sample_data[:2])

    def test_sub_rel_string(self):
        flist = fs.Filelist(sample_data)
        flist2 = flist - str(rel_sample[2])
        assert set(flist2.data) == set(test_data[:2])

    def test_sub_dir_string(self):
        flist = fs.Filelist(sample_data)
        flist3 = flist - str(os.path.relpath(rel_to_abs('data'), start=os.getcwd()))
        assert set(flist3.data) == set()

    def test_filelist_sub_bad_string(self):
        with pytest.raises(FileNotFoundError, match = 
                           'File Not Found: hello world!'):
            flist = fs.Filelist(sample_data)
            flist - 'hello world!'

    def test_filelist_sub_abs_list(self):
        flist = fs.Filelist(sample_data)
        flist2 = flist - sample_data2
        assert set(flist2.data) == set(test_data[:2])

    def test_filelist_sub_rel_list(self):
        flist = fs.Filelist(rel_sample)
        flist2 = flist - rel_sample2
        assert set(flist2.data) == set(test_data[:2])


    def test_filelist_sub_bad_list(self):
        test = str(rel_to_abs('test_file'))
        test_list = sample_data.copy()
        test_list.append(test)
        flist = fs.Filelist(sample_data)
        with pytest.raises(FileNotFoundError, match=f'File Not Found: {test}'):
            flist2 = flist - test_list


    def test_sub_invalid(self):
        test = 5
        with pytest.raises(TypeError, match = f'Invalid input type: {type(test)}'):
            flist = fs.Filelist(sample_data)
            flist - test

class TestIadd:

    def test_iadd_abs_string(self):
        flist = fs.Filelist(sample_data)
        flist += str(rel_to_abs('data/sample_04.txt'))
        set1 = set(test_data)
        set1.add(os.path.abspath(rel_to_abs('data/sample_04.txt')))
        assert set(flist.data) == set1

    def test_iadd_rel_string(self):
        flist = fs.Filelist(sample_data)
        flist += str(os.path.relpath(rel_to_abs('data/sample_04.txt'), start=os.getcwd()))
        set1 = set(test_data)
        set1.add(os.path.abspath(rel_to_abs('data/sample_04.txt')))
        assert set(flist.data) == set1

    def test_iadd_dir_string(self):
        flist = fs.Filelist(sample_data)
        flist += str(os.path.relpath(rel_to_abs('data'), start=os.getcwd()))
        assert set(flist.data) == test_set

    def test_iadd_bad_string(self):
        with pytest.raises(FileNotFoundError, match = f'File Not Found: test_file'):
            flist = fs.Filelist(sample_data)
            flist += 'test_file'

    def test_iadd_Filelist(self):
        flist = fs.Filelist(sample_data)
        flist2 = fs.Filelist(sample_data2)
        flist += flist2
        assert set(flist.data) == test_set

    def test_iadd_abs_list(self):
        flist = fs.Filelist(sample_data)
        flist += sample_data2
        assert set(flist.data) == test_set

    def test_iadd_rel_list(self):
        flist = fs.Filelist(sample_data)
        flist += rel_sample2
        assert set(flist.data) == test_set

    def test_iadd_bad_list(self):
        test = str(rel_to_abs('test_file'))
        flist = fs.Filelist(sample_data)
        test_list = sample_data.copy()
        test_list.append(test)
        with pytest.raises(FileNotFoundError, match = f'File Not Found: {test}'):
            flist += test_list


class TestIsub:

    def test_isub_abs_string(self):
        flist = fs.Filelist(sample_data)
        flist -= str(rel_to_abs('data/sample_03.txt'))
        set1 = set(test_data[:2])
        assert set(flist.data) == set1

    def test_isub_rel_string(self):
        flist = fs.Filelist(sample_data)
        flist -= str(os.path.relpath(rel_to_abs('data/sample_03.txt'), start=os.getcwd()))
        set1 = set(test_data[:2])
        assert set(flist.data) == set1

    def test_isub_dir_string(self):
        flist = fs.Filelist(sample_data)
        flist -= str(os.path.relpath(rel_to_abs('data'), start=os.getcwd()))
        assert flist.data == []

    def test_isub_bad_string(self):
        with pytest.raises(FileNotFoundError, match = 'File Not Found: test_file'):
            flist = fs.Filelist(sample_data)
            flist -= 'test_file'

    def test_isub_Filelist(self):
        flist = fs.Filelist(sample_data)
        flist2 = fs.Filelist(sample_data2)
        flist -= flist2
        assert set(flist.data) == set(test_data[:2])

    def test_isub_abs_list(self):
        flist = fs.Filelist(sample_data)
        flist -= sample_data2
        assert set(flist.data) == set(test_data[:2])

    def test_isub_rel_list(self):
        flist = fs.Filelist(sample_data)
        flist -= rel_sample2
        assert set(flist.data) == set(test_data[:2])

    def test_isub_bad_list(self):
        test = str(rel_to_abs('test_file'))
        flist = fs.Filelist(sample_data)
        test_list = sample_data.copy()
        test_list.append(test)
        with pytest.raises(FileNotFoundError, match = f'File Not Found: {test}'):
            flist -= test_list

class TestSetCompars:

    def test_compare_main(self):
        flist = fs.Filelist(sample_data)
        flist2 = fs.Filelist(sample_data2)
        set_diff = flist.compare(flist2)
        assert set_diff == {'+': {sample_data[0],sample_data[1]}, '-':
                        {sample_data2[1], sample_data2[2]}}

    def test_compare_error_invalid_input(self):
        test = 5
        with pytest.raises(TypeError, match=f'Invalid input type: {type(test)}'):
            flist = fs.Filelist(sample_data)
            flist.compare(test)

    def test_compare_error_fnf(self):
        test = 'test_file'
        with pytest.raises(FileNotFoundError, match=f'File Not Found: {test}'):
            test_list = sample_data2.copy()
            test_list.append(test)
            flist = fs.Filelist(sample_data)
            flist.compare(test_list)

    def test_union(self):
        flist = fs.Filelist(sample_data)
        flist2 = fs.Filelist(sample_data2)
        assert flist.union(flist2) == test_set

    def test_difference(self):
        flist = fs.Filelist(sample_data)
        flist2 = fs.Filelist(sample_data2)
        assert flist.difference(flist2) == {test_data[0], test_data[1]}

    def test_intersection(self):
        flist = fs.Filelist(sample_data)
        assert flist.intersection(sample_data2) == {test_data[2]}

    def test_isdisjoint_false(self):
        flist = fs.Filelist(sample_data)
        flist2 = fs.Filelist(sample_data2)
        assert flist.isdisjoint(flist2) is False

    def test_isdisjoint_true(self):
        flist = fs.Filelist(sample_data)
        assert flist.isdisjoint(sample_data2[1:]) is True

    def test_issubset_false(self):
        flist = fs.Filelist(sample_data)
        assert flist.issubset(sample_data2) is False

    def test_issubset_true(self):
        flist = fs.Filelist(sample_data)
        assert flist.issubset(test_set) is True

    def test_issuperset_false(self):
        flist = fs.Filelist(sample_data)
        assert flist.issuperset(test_set) is False

    def test_issuperset_true(self):
        flist = fs.Filelist(test_set)
        assert flist.issuperset(sample_data) is True

    def test_symmetric_difference(self):
        flist = fs.Filelist(sample_data)
        assert flist.symmetric_difference(sample_data2) == {test_data[0], test_data[1],
                                                            test_data2[1], test_data2[2]}


class TestUtils:

    def test_sort(self):
        flist = fs.Filelist(test_set)
        flist.sort()
        assert flist.data == [test_data[0], test_data[1], test_data[2], test_data2[1], test_data2[2]]


    def test_save_abs(self):
        test_path = os.path.join(os.getcwd(), os.path.dirname(__file__),'filelists/test_filelist_abs.txt')
        flist = fs.Filelist(sample_data)
        flist.save(test_path)
        with open(test_path, encoding='utf-8') as f:
            saved_data = [line.rstrip() for line in f]
            assert saved_data == test_data

    def test_save_rel(self):
        test_path = os.path.join(os.getcwd(), os.path.dirname(__file__),'filelists/test_filelist_rel.txt')
        flist = fs.Filelist(sample_data)
        flist.save(test_path, relative=True)
        with open(test_path, encoding='utf-8') as f:
            saved_data = [os.path.normpath(os.path.join(os.path.dirname(test_path), line.rstrip()))
                          for line in f]
            assert saved_data == test_data

    def test_read_filelist_abs(self):
        test_path = os.path.join(os.getcwd(), os.path.dirname(__file__),'filelists/test_filelist_abs.txt')
        flist = fs.read_filelist(test_path)
        assert flist.data == test_data


    def test_read_filelist_rel(self):
        test_path = os.path.join(os.getcwd(), os.path.dirname(__file__),'filelists/test_filelist_rel.txt')
        flist = fs.read_filelist(test_path)
        assert flist.data == test_data
