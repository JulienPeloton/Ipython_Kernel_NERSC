#!/usr/bin/python
"""
Script to generate IPython kernels at NERSC with your $PYTHONPATH added

Author: Julien Peloton, j.peloton@sussex.ac.uk
"""
from __future__ import division, absolute_import, print_function

import os
import argparse


def safe_mkdir(path, verbose=False):
    """
    Create a path and catch the race condition between path exists and mkdir.

    Parameters
    ----------
    path : string
        Name of the folder to be created.
    verbose : bool
        If True, print messages about the status.

    Examples
    ----------
    Folders are created
    >>> safe_mkdir('toto/titi/tutu', verbose=True)

    Folders aren't created because they already exist
    >>> safe_mkdir('toto/titi/tutu', verbose=True)
    Folders toto/titi/tutu already exist. Not created.

    >>> os.removedirs('toto/titi/tutu')
    """
    abspath = os.path.abspath(path)
    if not os.path.exists(abspath):
        try:
            os.makedirs(abspath)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    else:
        if verbose:
            print("Folders {} already exist. Not created.".format(path))

def create_json(path, kernelname):
    """
    Create submission file for the software xpure

    Parameters
    ----------
    path : string
        Where to store the kernel file
    kernelname : string
        Name of the kernel
    """
    host = os.environ['NERSC_HOST']
    LD_LIBRARY_PATH = os.environ['LD_LIBRARY_PATH']
    PYTHONPATH = os.environ['PYTHONPATH']
    PATH = os.environ['PATH']

    filename = os.path.join(path, 'kernel.json')
    with open(filename, 'w') as f:
        print('{', file=f)
        print('  "display_name": "{}",'.format(kernelname), file=f)
        print('  "language": "python",', file=f)
        print('  "argv": [', file=f)
        print('    "/global/common/cori/software/python/2.7-anaconda/bin/python",', file=f)
        print('    "-m",', file=f)
        print('    "ipykernel",', file=f)
        print('    "-f",', file=f)
        print('    "{connection_file}"', file=f)
        print('  ],', file=f)
        print('  "env": {', file=f)
        print('    "PATH": ', file=f)
        print('    "{}",'.format(PATH), file=f)
        print('    "LD_LIBRARY_PATH":', file=f)
        print('    "{}",'.format(LD_LIBRARY_PATH), file=f)
        print('    "PYTHONPATH":', file=f)
        print('    "{}"'.format(PYTHONPATH), file=f)
        print('  }', file=f)
        print('}', file=f)


def addargs(parser):
    """ Parse command line arguments for s4cmb """
    parser.add_argument(
        '-kernelname', dest='kernelname',
        required=True,
        help='Name of the IPython kernel')


if __name__ == "__main__":
    """
    Launch!
    """
    parser = argparse.ArgumentParser(
        description='Create IPython kernels for using notebooks at NERSC')
    addargs(parser)
    args = parser.parse_args(None)

    ## Grab $HOME path
    HOME = os.environ['HOME']

    ## Kernels are stored here
    ## See http://www.nersc.gov/users/data-analytics/data-analytics-2/jupyter-and-rstudio/
    path = '{}/.ipython/kernels/{}'.format(HOME, args.kernelname)

    ## Create the path, and store the kernel
    safe_mkdir(path, verbose=True)
    create_json(path, args.kernelname)

    print("Kernel at {}".format(path))
