from Filelist import Filelist


class Empty:
    pass


my_flist = Filelist(
    [
        "../tests/data/sample_01.txt",
        "../tests/data/sample_02.txt",
        "../tests/data/sample_03.txt",
    ]
)

# copy_flist = Empty()
# copy_flist.__class__ = Filelist

# copy_flist.__dict__ = my_flist.__dict__.copy()

# print(my_flist._data, my_flist._lookup_table)
# print(copy_flist)
# print(copy_flist.__dict__)


# to abs
def to_abs():  # my_flist is self
    # TODO: if self.is_abs():
    copy_flist = Empty()
    copy_flist.__class__ = Filelist
    copy_flist.__dict__ = my_flist.__dict__.copy()

    copy_flist._data = [
        copy_flist._abs_commpfx + fpath[len(copy_flist._curr_commpfx) :]
        for fpath in copy_flist._data
    ]
    copy_flist._curr_commpfx = copy_flist._abs_commpfx
    return copy_flist


abs_flist = to_abs()
print(abs_flist._data, abs_flist._lookup_table)


def to_rel():
    copy_flist = Empty()
    copy_flist.__class__ = Filelist
    copy_flist.__dict__ = abs_flist.__dict__.copy()

    copy_flist._data = [
        copy_flist._rel_commpfx + fpath[len(copy_flist._curr_commpfx) :]
        for fpath in copy_flist._data
    ]
    copy_flist._curr_commpfx = copy_flist._rel_commpfx
    return copy_flist


rel_flist = to_rel()
print(rel_flist._data, rel_flist._lookup_table)
