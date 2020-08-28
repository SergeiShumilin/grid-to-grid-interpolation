import argparse
import os
from grid import grid
from tecplot import reader, writer
from algorithms import kdtree
import time


def check_argument(name):
    if not os.path.isfile(name):
        print('File {} doesn\'t exist'.format(name))
        exit(1)
    else:
        if not old_grid[-4:] == '.dat':
            print('File {} should be .dat file'.format(name))
            exit(1)


parser = argparse.ArgumentParser()
parser.add_argument('old_grid', help='old grid .dat file')
parser.add_argument('new_grid', help='new grid .dat file')
parser.add_argument('-res', '--result_grid', help='interpolated grid. if not provided than the name of the '
                                                  'result file is \"new_grid\" + \"_interpolated\"')
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity", default=0)
parser.add_argument('-f', '--force_interpolation', help='force interpolation even if grids are isomorphic',
                    action='store_true')
args = parser.parse_args()

old_grid = args.old_grid
new_grid = args.new_grid
result_grid = args.result_grid

check_argument(old_grid)
check_argument(new_grid)
if result_grid:
    if not result_grid[-4:] == '.dat':
        print('File {} should be .dat file'.format(result_grid))
        exit(1)

start = time.time()
grid1 = grid.Grid()
grid2 = grid.Grid()
reader.read_tecplot(grid1, old_grid)

if args.verbosity > 0:
    print('Old grid read')

reader.read_tecplot(grid2, new_grid)

if args.verbosity > 0:
    print('New grid read')

if grid2.is_isomprphic_to(grid1) and not args.force_interpolation:
    grid2.relocate_values_from_isomorphic_grid(grid1)
    if args.verbosity > 0:
        print('Grids are isomorphic. Values have been relocated')
else:
    kdtree.interpolate(grid1, grid2)
    if args.verbosity > 0:
        print('Interpolation made')

if args.result_grid:
    writer.write_tecplot(grid2, result_grid)
else:
    writer.write_tecplot(grid2, new_grid[:-4] + '_interpolated.dat')

if args.verbosity > 0:
    print('Result grid was written')
    print('Total time:', time.time() - start)
