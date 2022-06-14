import sys
import os
sys.path.append('../')
import filelister as fs

sample_data = ['tests/data/sample_01.txt',
               'tests/data/sample_02.txt',
               'tests/data/sample_03.txt']
test_data = [os.path.abspath(test) for test in sample_data]


def test_filelist_create_from_list():
    flist = fs.Filelist(sample_data)
    assert set(flist.data) == set(test_data)


def test_filelist_create_from_set():
    flist = fs.Filelist(set(test_data))
    assert set(flist.data) == set(test_data)


def test_filelist_create_from_dir():
    flist = fs.Filelist('tests/data')
    assert set(flist.data) == set(test_data)


def test_filelist_create_from_tuple():
    flist = fs.Filelist(tuple(sample_data))
    assert set(flist.data) == set(test_data)
