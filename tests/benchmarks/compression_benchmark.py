"""
Benchmarking for filelister compression
"""


import os
import sys
import time

import filelister as fs
from tqdm import tqdm


def get_uncompressed_metrics(path):
    """
    gets metrics for uncompressed filelist
    """

    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
        size = sys.getsizeof(data)
        lines = len(data.split("\n"))
    return size, lines


def benchmark_read_uncompressed(test_file, iterations):
    """
    benchmarks uncompressed reads
    """
    print("Benchmarking Uncompressed Reads")
    file_size, num_lines = get_uncompressed_metrics(test_file)
    print(f"Test File: {test_file}")
    print(f"Iterations: {iterations}")
    print(f"Total Lines: {num_lines}")
    print(f"File Size: {file_size / 1000000} MB")
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        fs.read_filelist(test_file, compressed=False)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f"Total execution time: {total_runtime} seconds")
    print(f"Average execution time: {total_runtime/iterations} seconds")
    print(f"Max execution time: {max(runtimes)} seconds")
    print(f"Min execution time: {min(runtimes)} seconds")


def benchmark_write_uncompressed(test_list, iterations):
    """
    benchmarks uncompressed writes
    """
    print("Benchmarking Uncompressed Writes")
    print(f"Iterations: {iterations}")
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        test_list.save("./uncompressed_write.txt", compressed=False)
        end = time.time()
        runtimes.add(end - start)
    os.remove("./uncompressed_write.txt")
    total_runtime = sum(runtimes)
    print(f"Total execution time: {total_runtime} seconds")
    print(f"Average execution time: {total_runtime/iterations} seconds")
    print(f"Max execution time: {max(runtimes)} seconds")
    print(f"Min execution time: {min(runtimes)} seconds")


def benchmark_write_uncompressed_rel(test_list, iterations):
    """
    benchmarks uncompressed relative writes
    """
    print("Benchmarking Uncompressed Relative Writes")
    print(f"Iterations: {iterations}")
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        test_list.save("./uncompressed_write_rel.txt", compressed=False)
        end = time.time()
        runtimes.add(end - start)
    os.remove("./uncompressed_write.txt")
    total_runtime = sum(runtimes)
    print(f"Total execution time: {total_runtime} seconds")
    print(f"Average execution time: {total_runtime/iterations} seconds")
    print(f"Max execution time: {max(runtimes)} seconds")
    print(f"Min execution time: {min(runtimes)} seconds")


def benchmark_write_compressed(test_list, iterations):
    """
    benchmarks compressed writes
    """
    print("Benchmarking Compressed Writes")
    print(f"Iterations: {iterations}")
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        test_list.save("./compressed_write.zz", compressed=True)
        end = time.time()
        runtimes.add(end - start)
    os.remove("./compressed_write.zz")
    total_runtime = sum(runtimes)
    print(f"Total execution time: {total_runtime} seconds")
    print(f"Average execution time: {total_runtime/iterations} seconds")
    print(f"Max execution time: {max(runtimes)} seconds")
    print(f"Min execution time: {min(runtimes)} seconds")


def get_compressed_metrics(path):
    """
    gets metrics for compressed filelist
    """
    with open(path, "rb") as f:
        raw_data = f.read()
        size = sys.getsizeof(raw_data)
    read_flist = fs.read_filelist(path, compressed=True)
    lines = len(read_flist)
    return size, lines


def benchmark_read_compressed(test_file, iterations):
    """
    benchmarks compressed reads
    """
    print("Benchmarking Compressed Reads")
    file_size, num_lines = get_compressed_metrics(test_file)
    print(f"Test File: {test_file}")
    print(f"Iterations: {iterations}")
    print(f"Total Lines: {num_lines}")
    print(f"File Size: {file_size / 1000000} MB")
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        fs.read_filelist(test_file, compressed=True)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f"Total execution time: {total_runtime} seconds")
    print(f"Average execution time: {total_runtime/iterations} seconds")
    print(f"Max execution time: {max(runtimes)} seconds")
    print(f"Min execution time: {min(runtimes)} seconds")


if __name__ == "__main__":
    NUM_ITERATIONS = 1
    TEST_FILE = os.path.join(os.path.dirname(__file__), "./sample_flist.txt")

    sample_path = os.path.abspath(os.path.dirname(__file__))
    # write test file
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        for i in range(1000000):
            f.write(f"/home/simon/dev/data_science/filelister/test/data/sample_{str(i).zfill(7)}")

    compressed_file = os.path.splitext(TEST_FILE)[0] + "_compressed.zz"
    flist = fs.read_filelist(TEST_FILE, compressed=False)
    flist.save(compressed_file, compressed=True)

    print("\n\n")

    # write benchmarks
    benchmark_write_uncompressed(flist, NUM_ITERATIONS)
    print("\n\n")
    #    benchmark_write_uncompressed_rel(flist, NUM_ITERATIONS)
    #    print("\n\n")
    benchmark_write_compressed(flist, NUM_ITERATIONS)
    print("\n\n\n\n")
    NUM_ITERATIONS = 1
    # read benchmarks
    benchmark_read_uncompressed(TEST_FILE, NUM_ITERATIONS)
    print("\n\n")
    #    benchmark_read_uncompressed("uncompressed_write_rel.txt", NUM_ITERATIONS)
    print("\n\n")
    benchmark_read_compressed(compressed_file, NUM_ITERATIONS)
    print("\n\n")

    os.remove(TEST_FILE)
    os.remove(compressed_file)
#    rel_flist = fs.read_filelist("uncompressed_write_rel.txt")
#    print(flist.compare(rel_flist))
#    print(len(rel_flist.data))
#    print(len(flist.data))
