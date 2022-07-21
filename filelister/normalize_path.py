import os


def normalize_paths(
    data, output_type, outfile
):  # outfile is relative output start location
    """normalize filepaths"""
    common_prefix = os.path.dirname(os.path.commonprefix(data))
    abs_common_prefix = os.path.abspath(common_prefix)
    rel_common_prefix = os.path.relpath(common_prefix, start=os.getcwd())

    is_abs = data[0][0] == "/"

    if output_type == "abs":
        # if absolute output, compute abs pfx, strip commpfx and strcat abspfx and truncated fpath
        if is_abs:
            return data  # not necessary but nice to insta return if abs to abs
        return [abs_common_prefix + fname[len(common_prefix) :] for fname in data]

    # if rel output, compute rel pfx from deisred start location, strip commpfx, strcat relpfx and truncated fpath
    if output_type == "rel":
        out_pfx = os.path.relpath(
            common_prefix,
            start=os.path.dirname(outfile),
        )  # outfile
        return [out_pfx + fname[len(common_prefix) :] for fname in data]
    return data


if __name__ == "__main__":
    rel_test_data = [
        "../tests/data/sample_01.txt",
        "../tests/data/sample_02.txt",
        "../tests/data/sample_03.txt",
    ]
    OUTFILE = "../../object_detection/data/images/new_flist.txt"

    print("rel to abs: ")
    print(normalize_paths(rel_test_data, "abs", OUTFILE))
    print("\n\n")
    print("rel to rel: ")
    print(normalize_paths(rel_test_data, "rel", OUTFILE))
    print("\n\n")

    abs_test_data = [
        "/home/simon/dev/data_science/filelister/tests/data/sample_01.txt",
        "/home/simon/dev/data_science/filelister/tests/data/sample_02.txt",
        "/home/simon/dev/data_science/filelister/tests/data/sample_03.txt",
    ]
    print("abs to abs: ")
    print(normalize_paths(abs_test_data, "abs", OUTFILE))
    print("\n\n")
    print("abs to rel: ")
    print(normalize_paths(abs_test_data, "rel", OUTFILE))
