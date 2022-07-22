"""Tests for Filelist Loader"""
import filelister as fs

test_data = ["/path/dir/file_00.jpg", "/path/dir/file_01.jpg"]


class TestFilelistLoader:
    def test_constructor(self):
        fs_loader = fs.FilelistLoader(test_data)
        assert fs_loader.data[0] == test_data[0]
        assert fs_loader.data[1] == test_data[1]

    def test_iter(self):
        fs_loader = fs.FilelistLoader(test_data)
        res = []
        for value in fs_loader:
            res.append(value)
        assert res[0] == test_data[0]
        assert res[1] == test_data[1]
