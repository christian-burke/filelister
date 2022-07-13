"""
Benchmarking for filelister compression
"""


import sys
import time
import os
from tqdm import tqdm
import filelister as fs


def get_uncompressed_metrics(path):
    """
    gets metrics for uncompressed filelist
    """

    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        size = sys.getsizeof(data)
        lines = len(data.split('\n'))
    return size, lines


def benchmark_read_uncompressed(test_file, iterations):
    """
    benchmarks uncompressed reads
    """
    print('Benchmarking Uncompressed Reads')
    file_size, num_lines = get_uncompressed_metrics(test_file)
    print(f'Test File: {test_file}')
    print(f'Iterations: {iterations}')
    print(f'Total Lines: {num_lines}')
    print(f'File Size: {file_size / 1000000} MB')
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        fs.read_filelist(test_file, compressed=False, check_exts=False, check_exists=False)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f'Total execution time: {total_runtime} seconds')
    print(f'Average execution time: {total_runtime/iterations} seconds')
    print(f'Max execution time: {max(runtimes)} seconds')
    print(f'Min execution time: {min(runtimes)} seconds')


def benchmark_write_uncompressed(test_list, iterations):
    """
    benchmarks uncompressed writes
    """
    print('Benchmarking Uncompressed Writes')
    print(f'Iterations: {iterations}')
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        test_list.save('uncompressed_write.txt', compressed=False)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f'Total execution time: {total_runtime} seconds')
    print(f'Average execution time: {total_runtime/iterations} seconds')
    print(f'Max execution time: {max(runtimes)} seconds')
    print(f'Min execution time: {min(runtimes)} seconds')


def benchmark_write_compressed(test_list, iterations):
    """
    benchmarks compressed writes
    """
    print('Benchmarking Compressed Writes')
    print(f'Iterations: {iterations}')
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        test_list.save('compressed_write.zz', compressed=True)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f'Total execution time: {total_runtime} seconds')
    print(f'Average execution time: {total_runtime/iterations} seconds')
    print(f'Max execution time: {max(runtimes)} seconds')
    print(f'Min execution time: {min(runtimes)} seconds')


def get_compressed_metrics(path):
    """
    gets metrics for compressed filelist
    """
    with open(path, 'rb') as f:
        raw_data = f.read()
        size = sys.getsizeof(raw_data)
    flist = fs.read_filelist(path, check_exists=False, check_exts=False, compressed=True)
    lines = len(flist.data)
    return size, lines


def benchmark_read_compressed(test_file, iterations):
    """
    benchmarks compressed reads
    """
    print('Benchmarking Compressed Reads')
    file_size, num_lines = get_compressed_metrics(test_file)
    print(f'Test File: {test_file}')
    print(f'Iterations: {iterations}')
    print(f'Total Lines: {num_lines}')
    print(f'File Size: {file_size / 1000000} MB')
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        fs.read_filelist(test_file, check_exts=False, check_exists=False, compressed=True)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f'Total execution time: {total_runtime} seconds')
    print(f'Average execution time: {total_runtime/iterations} seconds')
    print(f'Max execution time: {max(runtimes)} seconds')
    print(f'Min execution time: {min(runtimes)} seconds')



if __name__ == '__main__':
    NUM_ITERATIONS = 2
    TEST_FILE = os.path.join(os.getcwd(), os.path.dirname(__file__), 'filelists/national_parks.txt')
    compressed_file = os.path.splitext(TEST_FILE)[0] + '_compressed.zz'
    flist = fs.read_filelist(TEST_FILE, compressed=False,
                             check_exists=False, check_exts=False)
    flist.save(compressed_file, compressed=True)


    print('\n\n')

    # write benchmarks
    benchmark_write_uncompressed(flist, NUM_ITERATIONS)
    print('\n\n\n\n')
    benchmark_write_compressed(flist, NUM_ITERATIONS)
    print('\n\n\n\n')
    NUM_ITERATIONS = 4
    # read benchmarks
    benchmark_read_uncompressed(TEST_FILE, NUM_ITERATIONS)
    print('\n\n\n\n')
    benchmark_read_compressed(compressed_file, NUM_ITERATIONS)
    compressed_flist = fs.read_filelist(compressed_file, compressed=True)
    print(flist.compare(compressed_flist))
