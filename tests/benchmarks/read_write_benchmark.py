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


def benchmark_read_uncompressed_best(test_file, iterations):
    """
    benchmarks uncompressed reads
    """
    print("Benchmarking Best-case Uncompressed Read")
    file_size, num_lines = get_uncompressed_metrics(test_file)
    print(f"Test File: {test_file}")
    print(f"Iterations: {iterations}")
    print(f"Total Lines: {num_lines}")
    print(f"File Size: {file_size / 1000000} MB")
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        fs.read_filelist(test_file)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f"Total execution time: {total_runtime} seconds")


def benchmark_read_uncompressed_worst(test_file, iterations):
    """
    benchmarks uncompressed reads
    """
    print("Benchmarking Worst-case Uncompressed Reads")
    file_size, num_lines = get_uncompressed_metrics(test_file)
    print(f"Test File: {test_file}")
    print(f"Iterations: {iterations}")
    print(f"Total Lines: {num_lines}")
    print(f"File Size: {file_size / 1000000} MB")
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        fs.read_filelist(
            test_file,
            compressed=False,
        )
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f"Total execution time: {total_runtime} seconds")


def benchmark_write_uncompressed(test_list, iterations):
    """
    benchmarks uncompressed writes
    """
    print("Benchmarking Uncompressed Writes")
    print(f"Iterations: {iterations}")
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        test_list.save("uncompressed_write.txt", compressed=False, relative=False)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f"Total execution time: {total_runtime} seconds")


def benchmark_write_compressed(test_list, iterations):
    """
    benchmarks compressed writes
    """
    print("Benchmarking Compressed Writes")
    print(f"Iterations: {iterations}")
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        test_list.save("compressed_write.zz", compressed=True, relative=False)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f"Total execution time: {total_runtime} seconds")


def get_compressed_metrics(path):
    """
    gets metrics for compressed filelist
    """
    with open(path, "rb") as f:
        raw_data = f.read()
        size = sys.getsizeof(raw_data)
    flist = fs.read_filelist(path, compressed=True)
    lines = len(flist)
    return size, lines


def benchmark_read_compressed_best(test_file, iterations):
    """
    benchmarks compressed reads
    """
    print("Benchmarking Best-case Compressed Reads")
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


def benchmark_read_compressed_worst(test_file, iterations):
    """
    benchmarks compressed reads
    """
    print("Benchmarking Worst-case Compressed Reads")
    file_size, num_lines = get_compressed_metrics(test_file)
    print(f"Test File: {test_file}")
    print(f"Iterations: {iterations}")
    print(f"Total Lines: {num_lines}")
    print(f"File Size: {file_size / 1000000} MB")
    runtimes = set()
    for _ in range(iterations):
        start = time.time()
        fs.read_filelist(test_file, compressed=True)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f"Total execution time: {total_runtime} seconds")


if __name__ == "__main__":
    NUM_ITERATIONS = 1
    TEST_FILE = os.path.join(
        os.getcwd(), os.path.dirname(__file__), "filelists/national_parks.txt"
    )
    TEST_FILE_REL = os.path.join(
        os.getcwd(), os.path.dirname(__file__), "filelists/rel_national_parks.txt"
    )
    compressed_file = os.path.splitext(TEST_FILE)[0] + "_compressed.zz"
    flist = fs.read_filelist(TEST_FILE, compressed=False)
    flist.save(compressed_file, compressed=True)

    print("\n\n")

    # write benchmarks
    benchmark_write_uncompressed(flist, NUM_ITERATIONS)
    print("\n\n\n\n")
    benchmark_write_compressed(flist, NUM_ITERATIONS)
    print("\n\n\n\n")
    NUM_ITERATIONS = 1
    # read benchmarks
    #    benchmark_read_uncompressed_best(TEST_FILE, NUM_ITERATIONS)
    print("\n\n\n\n")
    benchmark_read_uncompressed_worst(TEST_FILE_REL, NUM_ITERATIONS)
    print("\n\n\n\n")
    #    benchmark_read_compressed_best(compressed_file, NUM_ITERATIONS)
    print("\n\n\n\n")
    benchmark_read_compressed_worst(compressed_file, NUM_ITERATIONS)
    compressed_flist = fs.read_filelist(compressed_file, compressed=True)
    # print(flist.compare(compressed_flist))
    # print(len(compressed_flist.data))
    flist = fs.read_filelist(TEST_FILE_REL)
    print(len(flist.data))
    print(flist[:10])
