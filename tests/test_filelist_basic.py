import os
import filelister as fs
import pytest


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


def test_filelist_create_from_abs_list():
    flist = fs.Filelist(sample_data)
    assert set(flist.data) == set(test_data)


def test_filelist_create_from_rel_list():
    flist = fs.Filelist(rel_sample)
    assert set(flist.data) == set(test_data)


def test_filelist_create_from_abs_set():
    flist = fs.Filelist(set(test_data))
    assert set(flist.data) == set(test_data)


def test_filelist_create_from_rel_set():
    flist = fs.Filelist(set(rel_sample))
    assert set(flist.data) == set(test_data)


def test_filelist_create_from_dir():
    flist = fs.Filelist(rel_to_abs('data'))
    assert set(flist.data) == set(test_data).union(set(test_data2))


def test_filelist_create_from_abs_tuple():
    flist = fs.Filelist(tuple(sample_data))
    assert set(flist.data) == set(test_data)


def test_filelist_create_from_rel_tuple():
    flist = fs.Filelist(tuple(rel_sample))
    assert set(flist.data) == set(test_data)


def test_filelist_add_filelist():
    flist = fs.Filelist(sample_data)
    flist2 = fs.Filelist(sample_data2)
    flist3 = flist + flist2
    assert flist3 == test_set


def test_filelist_add_abs_string():
    flist = fs.Filelist(sample_data)
    flist3 = flist + str(rel_to_abs('data/sample_04.txt'))
    set1 = set(test_data)
    set1.add(os.path.abspath(rel_to_abs('data/sample_04.txt')))
    assert flist3 == set1


def test_filelist_add_rel_string():
    flist = fs.Filelist(sample_data)
    flist3 = flist + str(os.path.relpath(rel_to_abs('data/sample_04.txt'), os.getcwd()))
    set1 = set(test_data)
    set1.add(os.path.abspath(rel_to_abs('data/sample_04.txt')))
    assert flist3 == set1


def test_add_dir_string():
    flist = fs.Filelist(sample_data)
    flist3 = flist + str(os.path.relpath(rel_to_abs('data'), start=os.getcwd()))
    assert set(flist3) == test_set


def test_filelist_add_bad_string():
    with pytest.raises(TypeError, match = 'hello world! does not match a valid file or directory'):
        flist = fs.Filelist(sample_data)
        flist + 'hello world!'


def test_filelist_add_abs_list():
    flist = fs.Filelist(sample_data)
    flist2 = flist + sample_data2
    assert flist2 == test_set


def test_filelist_add_rel_list():
    flist = fs.Filelist(rel_sample)
    flist2 = flist + rel_sample2
    assert flist2 == test_set


def test_filelist_add_bad_list():
    test = str(rel_to_abs('cocks'))
    with pytest.raises(TypeError, match = f'{test} does not match a valid file'):
        flist = fs.Filelist(sample_data)
        flist2 = flist + [test]


def test_add_invalid():
    test = 5
    with pytest.raises(TypeError, match = f'{type(test)} is an invalid input type'):
        flist = fs.Filelist(sample_data)
        flist2 = flist + test


def test_iadd_abs_string():
    flist = fs.Filelist(sample_data)
    flist += str(rel_to_abs('data/sample_04.txt'))
    set1 = set(test_data)
    set1.add(os.path.abspath(rel_to_abs('data/sample_04.txt')))
    assert set(flist.data) == set1


def test_iadd_rel_string():
    flist = fs.Filelist(sample_data)
    flist += str(os.path.relpath(rel_to_abs('data/sample_04.txt'), start=os.getcwd()))
    set1 = set(test_data)
    set1.add(os.path.abspath(rel_to_abs('data/sample_04.txt')))
    assert set(flist.data) == set1


def test_iadd_dir_string():
    flist = fs.Filelist(sample_data)
    flist += str(os.path.relpath(rel_to_abs('data'), start=os.getcwd()))
    assert set(flist.data) == test_set


def test_iadd_Filelist():
    flist = fs.Filelist(sample_data)
    flist2 = fs.Filelist(sample_data2)
    flist += flist2
    assert set(flist.data) == test_set


def test_iadd_abs_list():
    flist = fs.Filelist(sample_data)
    flist += sample_data2
    assert set(flist.data) == test_set

def test_iadd_rel_list():
    flist = fs.Filelist(sample_data)
    flist += rel_sample2
    assert set(flist.data) == test_set
