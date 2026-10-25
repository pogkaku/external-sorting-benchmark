import os
import random
import time
import heapq
import resource
from pathlib import Path


NUMBERS_COUNT = 500_000
CHUNK_SIZE = 50_000
WORK_DIR = Path("sort_work")
OUTPUT_FILE = Path("sorted_output.txt")


def generate_numbers(count):
    """Generate random integers for the sorting benchmark."""
    random.seed(42)
    for _ in range(count):
        yield random.randint(0, 1_000_000)


def external_sort():
    """Sort numbers in chunks and merge the sorted chunks."""
    WORK_DIR.mkdir(exist_ok=True)

    start_time = time.perf_counter()
    chunks = []
    chunk = []

    
    for number in generate_numbers(NUMBERS_COUNT):
        chunk.append(number)

        if len(chunk) >= CHUNK_SIZE:
            chunk.sort()
            chunk_file = WORK_DIR / f"chunk_{len(chunks)}.txt"

            with open(chunk_file, "w") as file:
                file.writelines(f"{n}\n" for n in chunk)

            chunks.append(chunk_file)
            chunk = []

    
    if chunk:
        chunk.sort()
        chunk_file = WORK_DIR / f"chunk_{len(chunks)}.txt"

        with open(chunk_file, "w") as file:
            file.writelines(f"{n}\n" for n in chunk)

        chunks.append(chunk_file)

    
    def read_numbers(path):
        with open(path, "r") as file:
            for line in file:
                yield int(line.strip())

    sorted_chunks = [read_numbers(path) for path in chunks]

    with open(OUTPUT_FILE, "w") as output:
        for number in heapq.merge(*sorted_chunks):
            output.write(f"{number}\n")

    elapsed_time = time.perf_counter() - start_time

    
    previous = None
    count = 0
    is_sorted = True

    with open(OUTPUT_FILE, "r") as file:
        for line in file:
            number = int(line.strip())

            if previous is not None and number < previous:
                is_sorted = False

            previous = number
            count += 1

    
    peak_rss = resource.getrusage(
        resource.RUSAGE_SELF
    ).ru_maxrss

    if os.uname().sysname == "Darwin":
        peak_memory_mib = peak_rss / (1024 * 1024)
    else:
        peak_memory_mib = peak_rss / 1024

    print("External Sorting Benchmark")
    print("-------------------------")
    print(f"Numbers processed: {count:,}")
    print(f"Chunk size: {CHUNK_SIZE:,}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Execution time: {elapsed_time:.2f} seconds")
    print(f"Peak process memory: {peak_memory_mib:.2f} MiB")
    print(f"Output count correct: {count == NUMBERS_COUNT}")
    print(f"Output sorted: {is_sorted}")

    
    for path in chunks:
        path.unlink()

    WORK_DIR.rmdir()

    if count != NUMBERS_COUNT or not is_sorted:
        raise RuntimeError("Validation failed!")

    print("Validation passed!")


if __name__ == "__main__":
    external_sort()
