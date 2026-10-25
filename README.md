External Sorting Benchmark on Google Cloud

This project compares the execution time and peak memory usage of a Python external sorting algorithm on Google Cloud VMs with 1 GB, 2 GB, and 4 GB RAM.

Results

VM RAM| Execution Time| Peak Memory
1 GB| 1.04 s| 14.83 MiB
2 GB| 1.00 s| 14.83 MiB
4 GB| 0.95 s| 15.00 MiB

Each test processed 500,000 integers using 50,000-number chunks, disk storage, and "heapq.merge()". All three runs passed validation.

Limitation

Due to the limited time available for this lab exercise, each configuration was tested only once. The results are preliminary, not averages, and repeated runs would be needed for a more reliable performance comparison.

Technologies

- Python
- Google Cloud Compute Engine
- External sorting and file handling

Course: COMP 548 DL — University of Nicosia
Author: Akama Ghislain
