from collections import namedtuple
from array import array
from statistics import mean, variance
from time import monotonic_ns
from importlib.util import (spec_from_file_location,
                            module_from_spec)
from os.path import basename, splitext
from inspect import getmembers, isfunction
from argparse import ArgumentParser
from json import load, dumps

from rich.console import Console
from rich.table import Table
from rich.progress import track


def read_args(filepath: str):
    if not filepath:
        return dict()
    with open(filepath, 'r', encoding='utf-8') as file:
        data = load(file)
    assert isinstance(data, dict)
    return data

parser = ArgumentParser()

parser.add_argument(
    '-n', default=1_000_000, metavar='Number', type=int,
    help='Number of repeats for each test.'
)

parser.add_argument(
    '-a', '--args', default='', type=read_args,
    help='Json file with {"args": [...], "kwargs": {...}} that will be passed to each test'
)

parser.add_argument(
    '-s', '--sort', default='name',
    help='Parameter to sort result by(Possible: name, mean, median, best, worst)'
)

parser.add_argument(
    '--json', action='store_true', help='Output data as json string.'
)

parser.add_argument(
    'file',
    help='File containing speed test functions.')


console = Console()


FuncTimeResult = namedtuple(
    'FuncTimeResult',
    ['name', 'n', 'total', 'mean', 'variance', 'best', 'worst']
    )


def load_module(path: str):
    spec = spec_from_file_location(
        splitext(basename(path))[0],
        path
        )
    module = module_from_spec(spec)

    spec.loader.exec_module(module)

    test_funcs = []
    for name, obj in getmembers(module):
        if not name.startswith('st_'):
            continue
        if not callable(obj):
            continue
        test_funcs.append(obj)
    return test_funcs


def time_func(func: callable,
              args: tuple = tuple(),
              kwargs: dict = dict()
              ):
    start_time = monotonic_ns()
    func(*args, **kwargs)
    return (monotonic_ns() - start_time)/(10 ** 9)


def time_in_loop(func: callable,
                 args: tuple = tuple(),
                 kwargs: dict = dict(),
                 n: int=1_000_000,
                 ):
    times = array('d', [])
    
    iterator = track(range(n), description=f'Timing {func.__name__}...')
    total = 0
    best = float('inf')
    worst = float('-inf')
    for i in iterator:
        try:
            t = time_func(func, args, kwargs)
            times.append(t)
            total += t
            if t > worst:
                worst = t
            elif t < best:
                best = t
        except KeyboardInterrupt:
            break
    try:
        tmean = mean(times)
        tvariance = variance(times, tmean)
    except KeyboardInterrupt:
        quit()

    return FuncTimeResult(
        func.__name__[3:],
        i+1, 
        round(total, 4),
        tmean,
        round(tvariance, 10),
        best,
        worst
    )


def print_results(*args):
    t = Table(title='Results')
    t.add_column('Name')
    t.add_column('N-repeats')
    t.add_column('Total')
    t.add_column('Mean')
    t.add_column('Variance')
    t.add_column('Best', style='green')
    t.add_column('Worst', style='red')
    t.add_column('Slowness')
    ideal_time = min([
        i.mean for i in args
    ])
    if ideal_time:
        percent_slowness = [
            f'{round((i.mean / ideal_time) * 100, 2)}%'
            for i in args
        ]
    else:
        percent_slowness = ['Infinitely slow' for _ in args]
    for a, slowness in zip(args, percent_slowness):
        t.add_row(*[str(i) for i in a], slowness)
    
    console.print(t)


def main():
    cli_args = parser.parse_args()
    targets = load_module(cli_args.file)

    results = []
    for func in targets:
        results.append(
            time_in_loop(
                func,
                cli_args.args.get('args', tuple()),
                cli_args.args.get('kwargs', dict()),
                n=cli_args.n
            )
        )
    results = sorted(
        results,
        key=lambda item: getattr(item, cli_args.sort)
        )
    if cli_args.args:
        console.print(cli_args.args, soft_wrap=True)
    
    if not cli_args.json:
        print_results(*results)
    else:
        print(dumps([i._asdict() for i in results]))


if __name__ == '__main__':
    main()