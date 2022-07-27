import sys
import time
from ctypes import c_wchar_p
from random import choice


def benchmark_append_python(iters, str_len):
    print(
        f"Benchmarking {iters} iterations of Python appending with string length {str_len}"
    )
    data = []
    start = time.time()
    for _ in range(iters):
        data.append("a" * str_len)
    end = time.time()
    print(f"Runtime: {end - start}")
    print(f"Size: {sum([sys.getsizeof(i) for i in data]) / 1000} MB\n")


def benchmark_append_ctypes(iters, str_len):
    print(
        f"Benchmarking {iters} iterations of C Pointer appending with string length {str_len}"
    )
    data = []
    start = time.time()
    for _ in range(iters):
        data.append(c_wchar_p("a" * str_len))
    end = time.time()
    print(f"Runtime: {end - start}")
    print(f"Size: {sum([sys.getsizeof(i) for i in data]) / 1000} MB\n")


def benchmark_indexing_python(iters):
    print(f"Benchmarking {iters} iterations of Python indexing")
    data = []
    for _ in range(iters):
        data.append("hello, benchmarks!" * 10)
    start = time.time()
    for _ in range(iters):
        choice(data)
    end = time.time()
    print(f"Runtime: {end - start}")


def benchmark_indexing_ctypes(iters):
    print(f"Benchmarking {iters} iterations of Python indexing")
    data = []
    for _ in range(iters):
        data.append(c_wchar_p("hello, benchmarks!" * 10))
    start = time.time()
    for _ in range(iters):
        choice(data).value
    end = time.time()
    print(f"Runtime: {end - start}")


if __name__ == "__main__":
    benchmark_append_python(10000, 10)
    benchmark_append_ctypes(10000, 10)
    benchmark_append_python(10000, 100)
    benchmark_append_ctypes(10000, 100)
    benchmark_append_python(10000, 1000)
    benchmark_append_ctypes(10000, 1000)

    # benchmark_indexing_python(10000)
    # benchmark_indexing_ctypes(10000)
