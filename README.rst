=============================
IPYTHON NERSC KERNEL
=============================

The package
===============

Create custom IPython kernels for using jupyter notebooks at NERSC.

Why would you need this script?
===============

When you try to connect to jupyter-dev, it will read your JUPYTER_PATH.
If for some reasons, there are packages in your path in conflict with the default
paths of jupyter-dev, you will not be able to connect. If you encounter such problem, here is a solution:

* Edit your .bashrc.ext (or whatever file where you declare your paths) and reorganise it the following:

::

    export NERSC_HOST=`/usr/common/usg/bin/nersc_host`
    if [ ${NERSC_HOST} != "cori19" ]; then
        export NERSC_HOST="toto"
    fi

    if [ ${NERSC_HOST} != "cori" ]; then
        <all your declarations and module loads>
    fi

* By doing so, if you connect to jupyter-dev (cori19), you won't load all your custom packages. However, if you connect to cori, you will load everything as usual.
* Then on cori, run the script makekernel.py and create a kernel with all your custom paths:

::

    python makekernel.py -kernelname mykernel -py_version 2.7

or

::

    python makekernel.py -kernelname mykernel -py_version 3.6

* It will set the $LD_LIBRARY_PATH, $PYTHONPATH, and $PATH. You can choose python2.7 or python3.6 (latest anaconda-4.4).
* Connect to https://jupyter-dev.nersc.gov/hub/login and create a notebook with the kernel mykernel${py_version} you just created (which contains all your favourite paths).

Other usage
===============

It is easy to modify the script to generate any kind of custom kernels. Feel free to edit it!
