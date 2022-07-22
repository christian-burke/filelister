import os

import filelister as fs
import pytest

_this_path = os.path.abspath(os.path.dirname(__file__))


def rel_to_abs(path):
    return os.path.abspath(os.path.join(os.getcwd(), _this_path, path))


def normalize_rel_path(path):
    return os.path.relpath(os.path.join(_this_path, path), start=os.getcwd())


sample_data = ["data/sample_01.txt", "data/sample_02.txt", "data/sample_03.txt"]
sample_data = [rel_to_abs(path) for path in sample_data]
sample_data2 = ["data/sample_03.txt", "data/sample_04.txt", "data/sample_05.txt"]
sample_data2 = [rel_to_abs(path) for path in sample_data2]
rel_sample = [normalize_rel_path(path) for path in sample_data]
rel_sample2 = [normalize_rel_path(path) for path in sample_data2]

test_data2 = [os.path.abspath(test) for test in sample_data2]
test_data = [os.path.abspath(test) for test in sample_data]
test_set = set(test_data).union(set(test_data2))
test_list = test_data + test_data2[1:]
test_list_rel = rel_sample + rel_sample2[1:]
test_no_context = ["sample_01.txt", "sample_02.txt", "sample_03.txt"]
test_no_context_abs = [rel_to_abs(fpath) for fpath in test_no_context]
test_nested_data = [
    "data/sample_01.txt",
    "data/moredata/sample_02.txt",
    "data/moredata/deeper/sample_03.txt",
]
test_nested_data_rel = [normalize_rel_path(fpath) for fpath in test_nested_data]
test_nested_data_abs = [rel_to_abs(fpath) for fpath in test_nested_data]

data_rel = normalize_rel_path("data")
data_abs = rel_to_abs("data")


class TestCreateFromType:
    def test_filelist_create_from_abs_list(self):
        flist = fs.Filelist(sample_data)
        assert set(flist.data) == set(test_data)
        assert flist._curr_commpfx == data_abs
        assert flist._abs_commpfx == data_abs
        assert flist._rel_commpfx == data_rel

    def test_filelist_create_from_rel_list(self):
        flist = fs.Filelist(rel_sample)
        assert flist.data == rel_sample
        assert flist._curr_commpfx == data_rel
        assert flist._abs_commpfx == data_abs
        assert flist._rel_commpfx == data_rel

    def test_filelist_create_from_abs_set(self):
        flist = fs.Filelist(set(test_data))
        assert set(flist.data) == set(test_data)
        assert flist._curr_commpfx == data_abs
        assert flist._abs_commpfx == data_abs
        assert flist._rel_commpfx == data_rel

    def test_filelist_create_from_rel_set(self):
        flist = fs.Filelist(set(test_list_rel))
        assert set(flist.data) == set(test_list_rel)
        assert flist._curr_commpfx == data_rel
        assert flist._abs_commpfx == data_abs
        assert flist._rel_commpfx == data_rel

    def test_filelist_create_from_abs_dir(self):
        flist = fs.Filelist(rel_to_abs("data"))
        assert set(flist.data) == set(test_list)
        assert flist._curr_commpfx == data_abs
        assert flist._abs_commpfx == data_abs
        assert flist._rel_commpfx == data_rel

    def test_filelist_create_from_rel_dir(self):
        flist = fs.Filelist(normalize_rel_path("data"))
        assert set(flist.data) == set(test_list_rel)
        assert flist._curr_commpfx == data_rel
        assert flist._abs_commpfx == data_abs
        assert flist._rel_commpfx == data_rel

    def test_filelist_create_from_abs_tuple(self):
        flist = fs.Filelist(tuple(sample_data))
        assert set(flist.data) == set(test_data)
        assert flist._curr_commpfx == data_abs
        assert flist._abs_commpfx == data_abs
        assert flist._rel_commpfx == data_rel

    def test_filelist_create_from_rel_tuple(self):
        flist = fs.Filelist(tuple(rel_sample))
        assert flist.data == rel_sample
        assert flist._curr_commpfx == data_rel
        assert flist._abs_commpfx == data_abs
        assert flist._rel_commpfx == data_rel

    def test_create_with_no_context(self):
        flist = fs.Filelist(test_no_context)
        assert flist.data == test_no_context
        assert flist._curr_commpfx == normalize_rel_path("")
        assert flist._abs_commpfx == rel_to_abs("")
        assert flist._rel_commpfx == normalize_rel_path("")

    def test_create_nested_rel(self):
        flist = fs.Filelist(test_nested_data_rel)
        t = os.path.commonprefix(test_nested_data_rel)
        assert flist.data == test_nested_data_rel
        assert flist._curr_commpfx == data_rel
        assert flist._abs_commpfx == data_abs
        assert flist._rel_commpfx == data_rel


class TestConversions:
    def test_abs_to_rel(self):
        flist = fs.Filelist(test_list)
        rel_flist = flist.to_rel()
        assert rel_flist.data == test_list_rel
        assert rel_flist._curr_commpfx == data_rel

    def test_abs_to_rel_nested(self):
        flist = fs.Filelist(test_nested_data_abs)
        rel_flist = flist.to_rel()
        assert rel_flist.data == test_nested_data_rel
        assert rel_flist._curr_commpfx == data_rel

    def test_rel_to_abs(self):
        flist = fs.Filelist(test_list_rel)
        abs_flist = flist.to_abs()
        assert abs_flist.data == test_list
        assert abs_flist._curr_commpfx == data_abs

    def test_abs_to_abs_raises(self):
        flist = fs.Filelist(test_list)
        with pytest.raises(TypeError, match=r"Filelist is already absolute*"):
            flist.to_abs()

    def test_rel_to_rel_raises(self):
        flist = fs.Filelist(test_list_rel)
        with pytest.raises(TypeError, match=r"Filelist is already relative*"):
            flist.to_rel()

    def test_no_context_to_abs(self):
        flist = fs.Filelist(test_no_context)
        abs_flist = flist.to_abs()
        assert abs_flist.data == test_no_context_abs


class TestUtils:
    def test_save_abs(self):
        test_path = os.path.join(
            os.getcwd(), os.path.dirname(__file__), "filelists/test_filelist_abs.txt"
        )
        flist = fs.Filelist(sample_data)
        flist.save(test_path)
        with open(test_path, encoding="utf-8") as f:
            saved_data = [line.rstrip() for line in f]
            assert saved_data == test_data

    def test_save_rel(self):
        test_path = os.path.join(
            os.getcwd(), os.path.dirname(__file__), "filelists/test_filelist_rel.txt"
        )
        flist = fs.Filelist(sample_data)
        flist.save(test_path, relative=True)
        with open(test_path, encoding="utf-8") as f:
            saved_data = [
                os.path.normpath(
                    os.path.join(os.path.dirname(test_path), line.rstrip())
                )
                for line in f
            ]
            assert saved_data == test_data

    def test_read_filelist_abs(self):
        test_path = os.path.join(
            os.getcwd(), os.path.dirname(__file__), "filelists/test_filelist_abs.txt"
        )
        flist = fs.read_filelist(test_path)
        assert flist.data == test_data

    def test_read_filelist_rel(self):
        test_path = os.path.join(
            os.getcwd(), os.path.dirname(__file__), "filelists/test_filelist_rel.txt"
        )
        flist = fs.read_filelist(test_path)
        assert flist.data == rel_sample

    def test_contains_abs(self):
        flist = fs.Filelist(test_set)
        assert flist.contains(sample_data[0]) is True

    def test_not_contains_abs(self):
        flist = fs.Filelist(test_set)
        assert flist.contains("/not_a_file") is False

    def test_contains_rel(self):
        flist = fs.Filelist(test_set)
        assert flist.contains(rel_sample[0]) is True

    def test_not_contains_rel(self):
        flist = fs.Filelist(test_set)
        assert flist.contains("not_a_file") is False

    def test_contains_throws_typeerror(self):
        flist = fs.Filelist(test_set)
        with pytest.raises(TypeError, match="Invalid input: filename must be a string"):
            flist.contains(1234)
        assert set(flist.data) == test_set


class TestCompression:
    """
    tests for reading and writing compressed filelists
    """

    def test_save_abs_compressed(self):
        """
        tests ability to save a compressed absolute filelist
        """
        test_path = os.path.join(
            os.getcwd(), os.path.dirname(__file__), "filelists/compressed_abs.txt"
        )
        flist = fs.Filelist(sample_data)
        flist.save(test_path, relative=False, compressed=True)
        compressed_size = os.stat(test_path).st_size
        uncompressed_size = os.stat(
            os.path.join(
                os.getcwd(),
                os.path.dirname(__file__),
                "filelists/test_filelist_abs.txt",
            )
        ).st_size
        assert compressed_size < uncompressed_size

    def test_read_abs_compressed(self):
        """
        tests ability to read compressed absolute filelist
        """
        test_path = os.path.join(
            os.getcwd(), os.path.dirname(__file__), "filelists/compressed_abs.txt"
        )
        flist = fs.read_filelist(test_path, check_exists=True, compressed=True)
        assert flist.data == test_data

    def test_save_rel_compressed(self):
        """
        tests ability to save a compressed absolute filelist
        """
        test_path = os.path.join(
            os.getcwd(), os.path.dirname(__file__), "filelists/compressed_rel.zz"
        )
        flist = fs.Filelist(test_list)
        flist.save(test_path, relative=True, compressed=True)
        compressed_size = os.stat(test_path).st_size
        uncompressed_size = os.stat(
            os.path.join(
                os.getcwd(),
                os.path.dirname(__file__),
                "filelists/full_filelist_rel.txt",
            )
        ).st_size
        assert 0 < compressed_size < uncompressed_size

    def test_read_rel_compressed(self):
        """
        tests ability to read compressed absolute filelist
        """
        test_path = os.path.join(
            os.getcwd(), os.path.dirname(__file__), "filelists/compressed_rel.zz"
        )
        flist = fs.read_filelist(test_path, check_exists=True, compressed=True)
        assert flist.data == test_list_rel
