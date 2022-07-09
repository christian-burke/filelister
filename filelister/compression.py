import sys
import time
from tqdm import tqdm
import zlib
import gzip
import io
import os
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool


def decode(data):
    return data.decode('utf-8')


def read_filelist(path, compressed=True):
    if not compressed:
        with open(path, 'r', encoding='utf-8') as f:
            data = [line.rstrip() for line in f]
    else:
        with open(path, 'rb') as f:
            zdict = f.readline().strip()
            data = f.read()

        obj = zlib.decompressobj(zdict=zdict)
        data = obj.decompress(data)
        data += obj.flush()

        data = data.decode('utf-8').split(',')

        # data = data.split(b',')
        # data = [data[i:i+100000000] for i in range(0, len(data), 100000000)]

        # pool = ThreadPool(cpu_count())
        # data = pool.map(decode, data)
        # data = ''.join(data)
        # data = data.split(',')

        # pool = ThreadPool(cpu_count())
        # uncompressed_data = pool.map(decode, data)
        # return uncompressed_data
        # common_path = data[0]
        # data = [common_path + line for line in data]
    return data


def write_filelist(data, path, compressed=True):
    if not compressed:
        with open(path, 'w', encoding='utf-8') as f:
            for fn in data:
                f.write(str(fn) + '\n')
    else:
        zdict = os.path.commonprefix(data).encode('utf-8')
        # obj = zlib.compressobj(level=1)
        # common_path = os.path.commonpath(data)
        obj = zlib.compressobj(level=1, memLevel=9, zdict=zdict)
        # data = [line.replace(common_path, '') for line in data]
        # data.insert(0, common_path
        data = ','.join(data).encode('utf-8')
        data_zip = obj.compress(data)
        # to chunk data properly:
        # data_zip = obj.compress(data[:100000000])
        # data_zip += obj.compress(data[100000000:])
        data_zip += obj.flush()
        data_zip = zdict + b'\n' + data_zip

        with open(path, 'wb') as f:
            f.write(data_zip)


def read_wrapper(path):
    with open(path, 'rb') as f:
        with io.TextIOWrapper(f, encoding='utf-8') as decoder:
            data = decoder.read()
            data = data.split(',')
            common_path = data[0]
            data = [common_path + line for line in data]
            return data


def read_gzip_filelist(path):
    with gzip.open(path, mode='rb', compresslevel=1) as infile:
        with io.TextIOWrapper(infile, encoding='utf-8') as decoder:
            content = decoder.read()
            return content.split('\n')


def get_uncompressed_metrics(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        size = sys.getsizeof(data)
        lines = len(data.split('\n'))
    return size, lines


def benchmark_read_uncompressed(test_file, iterations):
    print('Benchmarking Uncompressed Reads')
    file_size, num_lines = get_uncompressed_metrics(test_file)
    print(f'Test File: {test_file}')
    print(f'Iterations: {iterations}')
    print(f'Total Lines: {num_lines}')
    print(f'File Size: {file_size / 1000000} MB')
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        read_filelist(test_file, compressed=False)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f'Total execution time: {total_runtime} seconds')
    print(f'Average execution time: {total_runtime/iterations} seconds')
    print(f'Max execution time: {max(runtimes)} seconds')
    print(f'Min execution time: {min(runtimes)} seconds')


def benchmark_write_uncompressed(data, iterations):
    print('Benchmarking Uncompressed Writes')
    # file_size, num_lines = get_uncompressed_metrics(test_file)
    # print(f'Test File: {test_file}')
    print(f'Iterations: {iterations}')
    # print(f'Total Lines: {num_lines}')
    # print(f'File Size: {file_size / 1000000} MB')
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        write_filelist(data, 'uncompressed_write.txt', compressed=False)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f'Total execution time: {total_runtime} seconds')
    print(f'Average execution time: {total_runtime/iterations} seconds')
    print(f'Max execution time: {max(runtimes)} seconds')
    print(f'Min execution time: {min(runtimes)} seconds')


def benchmark_write_compressed(data, iterations):
    print('Benchmarking Compressed Writes')
#    file_size, num_lines = get_uncompressed_metrics(test_file)
#    print(f'Test File: {test_file}')
    print(f'Iterations: {iterations}')
#    print(f'Total Lines: {num_lines}')
#    print(f'File Size: {file_size / 1000000} MB')
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        write_filelist(data, 'compressed_write.txt')
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f'Total execution time: {total_runtime} seconds')
    print(f'Average execution time: {total_runtime/iterations} seconds')
    print(f'Max execution time: {max(runtimes)} seconds')
    print(f'Min execution time: {min(runtimes)} seconds')


def get_compressed_metrics(path):
    with open(path, 'rb') as f:
        raw_data = f.read()
        size = sys.getsizeof(raw_data)
    data = read_filelist(path)
    lines = len(data)
    return size, lines


def benchmark_read_compressed(test_file, iterations):
    print('Benchmarking Compressed Reads')
    file_size, num_lines = get_compressed_metrics(test_file)
    print(f'Test File: {test_file}')
    print(f'Iterations: {iterations}')
    print(f'Total Lines: {num_lines}')
    print(f'File Size: {file_size / 1000000} MB')
    runtimes = set()
    for _ in tqdm(range(iterations)):
        start = time.time()
        read_filelist(test_file)
        end = time.time()
        runtimes.add(end - start)
    total_runtime = sum(runtimes)
    print(f'Total execution time: {total_runtime} seconds')
    print(f'Average execution time: {total_runtime/iterations} seconds')
    print(f'Max execution time: {max(runtimes)} seconds')
    print(f'Min execution time: {min(runtimes)} seconds')


#    print(f'Benchmarking Compressed Reads')
#    file_size, num_lines = get_compressed_metrics(test_file)
#    print(f'Test File: {test_file}')
#    print(f'Iterations: {iterations}')
#    print(f'Total Lines: {num_lines}')
#    print(f'File Size: {file_size / 1000000} MB')
#    start = time.time()
#    for i in tqdm(range(iterations)):
#        read_filelist(test_file)
#    end = time.time()
#    print(f'{iterations} compressed reads took {end - start} seconds\n')
#

def benchmark_gzip_read_compressed(test_file, iterations):
    # print(f'Benchmarking GZIP Compressed Reads')
    # file_size, num_lines = get_compressed_metrics(test_file)
    print(f'Test File: {test_file}')
    print(f'Iterations: {iterations}')
    # print(f'Total Lines: {num_lines}')
    # print(f'File Size: {file_size / 1000000} MB')
    start = time.time()
    for i in tqdm(range(iterations)):
        read_gzip_filelist(test_file)
    end = time.time()
    print(f'{iterations} compressed reads took {end - start} seconds\n')


def benchmark_read_npy_compressed(test_file, iterations):
    # print(f'Benchmarking Numpy Compressed Reads')
    # file_size, num_lines = get_numpy_compressed_metrics(test_file)
    print(f'Test File: {test_file}')
    print(f'Iterations: {iterations}')
    # print(f'Total Lines: {num_lines}')
    # print(f'File Size: {file_size / 1000000} MB')
    start = time.time()
    for i in tqdm(range(iterations)):
        read_filelist(test_file)
    end = time.time()
    print(f'{iterations} compressed reads took {end - start} seconds\n')


if __name__ == '__main__':
    data = read_filelist('national_parks.txt', compressed=False)
    write_filelist(data, 'compressed_parks.txt')

    num_iterations = 25
    print('\n\n')

    # write benchmarks
    # benchmark_write_uncompressed(data, num_iterations)
    # print('\n\n\n\n')
    # benchmark_write_compressed(data, num_iterations)
    # print('\n\n\n\n')

    # read benchmarks
    # benchmark_read_uncompressed('national_parks.txt', num_iterations)
    # print('\n\n\n\n')
    benchmark_read_compressed('compressed_parks.txt', num_iterations)
