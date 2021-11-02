import argparse
from os.path import isfile
from triangular_grid import grid
from tecplot.io import read_tecplot, write_tecplot
from algorithms.methods import *
from time import time


def choose_method(name):
    if name not in methods.keys():
        raise ValueError('Wrong parameter ')
    return methods[name]


def check_argument(name):
    if not isfile(name):
        print('File {} does not exist'.format(name))
        exit(1)
    else:
        if not old_grid[-4:] == '.dat':
            print('File {} should be .dat file'.format(name))
            exit(1)


parser = argparse.ArgumentParser()
parser.add_argument('source', help='old grid .dat file to interpolate from')
parser.add_argument('target', help='new grid .dat file to interpolate to')
parser.add_argument('-res', '--result_grid', help='interpolated grid. if not provided than the name of the '
                                                  'result file is \"new_grid\" + \"_interpolated\"')
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity", default=0)
parser.add_argument('-m', '--method', help='method of interpolation', choices=methods.keys(), default='cell_centered')
args = parser.parse_args()

old_grid = args.source
new_grid = args.target
result_grid = args.result_grid

check_argument(old_grid)
check_argument(new_grid)
if result_grid:
    if not result_grid[-4:] == '.dat':
        print('File {} should be .dat file'.format(result_grid))
        exit(1)

start = time()
grid1 = grid.Grid()
grid2 = grid.Grid()
read_tecplot(grid1, old_grid)

if args.verbosity > 0:
    print('Old grid read')

read_tecplot(grid2, new_grid)

if args.verbosity > 0:
    print('New grid read')

choose_method(args.method)(grid1, grid2)
if args.verbosity > 0:
    print('Interpolation made')

if args.result_grid:
    write_tecplot(grid2, result_grid)
else:
    write_tecplot(grid2, new_grid[:-4] + '_interpolated.dat')

if args.verbosity > 0:
    print('Result grid was written')
    print('Total time:', time() - start)
