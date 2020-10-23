# Stopwatch

Stopwatch is a python utility script to test speed of python code

## Installation

1. Clone this repo or download as zip
2. Open commandline in directory where `stopwatch.py` is
3. Enter command:
```
pip install -r requirements.txt
```

## Usage

```
usage: stopwatch.py [-h] [-n Number] [-a ARGS] [-s SORT] [--json] file

positional arguments:
  file                  File containing speed test functions.

optional arguments:
  -h, --help            show this help message and exit
  -n Number             Number of repeats for each test.
  -a ARGS, --args ARGS  Json file with {"args": [...], "kwargs": {...}} that will be passed to each test
  -s SORT, --sort SORT  Parameter to sort result by(Possible: name, mean, median, best, worst)
  --json                Output data as json string.
```

Main parameter here is `file`, it must be a path to file you want to test.

File must have functions prefixed with `st_`(which is short for **s**peed **t**est). Stopwatch will execute each of this functions and will show you stats like this:

```
┌────────────────────────────────┬───────────┬───────┬───────────┬──────────┬──────┬───────┬──────────┐
│ Name                           │ N-repeats │ Total │ Mean      │ Variance │ Best │ Worst │ Slowness │
├────────────────────────────────┼───────────┼───────┼───────────┼──────────┼──────┼───────┼──────────┤
│ concantenation                 │ 1000000   │ 0.437 │ 4.37e-07  │ 6.8e-09  │ 0.0  │ 0.016 │ 100.0%   │
│ f_string                       │ 1000000   │ 0.467 │ 4.67e-07  │ 7.3e-09  │ 0.0  │ 0.016 │ 106.86%  │
│ percent_format_without_mapping │ 1000000   │ 0.563 │ 5.63e-07  │ 8.8e-09  │ 0.0  │ 0.016 │ 128.83%  │
│ format_without_mapping         │ 1000000   │ 0.719 │ 7.19e-07  │ 1.12e-08 │ 0.0  │ 0.016 │ 164.53%  │
│ percent_formating_with_mapping │ 1000000   │ 0.815 │ 8.15e-07  │ 1.28e-08 │ 0.0  │ 0.016 │ 186.5%   │
│ format_with_mapping            │ 1000000   │ 1.123 │ 1.123e-06 │ 1.75e-08 │ 0.0  │ 0.016 │ 256.98%  │
└────────────────────────────────┴───────────┴───────┴───────────┴──────────┴──────┴───────┴──────────┘
```

Where:

​	**Name** is name of tested function

​	**N-repeats** - number of times functions was called

​	**Total** - total execution time in seconds

​	**Mean** - average time per call

​	**Variance** - dispersion of execution times

​	**Best/Worst** - best and worst times respectively

​	**Slowness** - percentage of function slowness where 100% is fastest solution from all tested 