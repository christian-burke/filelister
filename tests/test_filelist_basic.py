import sys
import os
sys.path.append('../')
import filelister as fs

sample_data = ['data/sample_01.txt',
               'data/sample_02.txt',
               'data/sample_03.txt']
sample_data = [os.path.join(os.getcwd(), os.path.dirname(__file__), path) for path in sample_data]
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
