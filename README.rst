pl-freesurfer_pp_moc
====================

.. image:: https://badge.fury.io/py/freesurfer_pp_moc.svg
    :target: https://badge.fury.io/py/freesurfer_pp_moc

.. image:: https://travis-ci.org/FNNDSC/freesurfer_pp_moc.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/freesurfer_pp_moc

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-freesurfer_pp_moc

.. contents:: Table of Contents


Abstract
--------

``freesurfer_pp_moc.py`` is a *dummy* FreeSurfer plugin / container that is prepopulated with the results of several *a priori* FreeSurfer runs. For a given run, this script will simply copy elements of one of these prior runs to the output directory. 

Synopsis
--------

.. code::

        python freesurfer_pp_moc.py                                         \
            [-v <level>] [--verbosity <level>]                          \
            [--version]                                                 \
            [--man]                                                     \
            [--meta]                                                    \
            [--copySpec <copySpec>]                                     \
            [--ageSpec <ageSpec>]                                       \
            <inputDir>                                                  \
            <outputDir> 

Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image. The PyPI mode is largely included for completeness sake and only useful if run against some pre-processed tree that exists in the filesystem. 

Using PyPI
~~~~~~~~~~

*You probably do not want to run the PyPI version unless you are a developer! Mostly likely you want the docker containerized run -- see the next section.*

To run from PyPI, simply do a 

.. code:: bash

    pip install freesurfer_pp_moc

and run with

.. code:: bash

    freesurfer.py --man /tmp /tmp


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

The real utility of this package is to run it containerized against bundled data that is packed into the container.

Assign an "input" directory to ``/incoming`` and an "output" directory to ``/outgoing``. Note that the "input" directory is effectively ignored by this plugin, but is required. Make sure that the host ``$(pwd)/out`` directory is world writable!

In the simplest sense, the plugin can be run with

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-freesurfer_pp_moc freesurfer_pp_moc.py                    \
            /incoming /outgoing

which will copy **only** the internal `stats` directory from a ``10-yr/06-mo/01-da`` subject to the output. By specifying a ``--copySpec stats,3D,sag,cor,tra`` several additional directories containing png image frames through parcellated sagittal, coronal, and transverse (axial) planes as well as multiple 3D images are also copied.

Examples
--------

Check available pre-processed runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get a listing of the internal tree of already processed and available FreeSurfer choices:

.. code:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-freesurfer_pp_moc freesurfer_pp_moc.py            \
            -T ../preprocessed                                          \
            /incoming /outgoing

This will print a tree of the available choices of `preprocessed` data in a directory tree. 

Copy the default for a selected pre-processed run
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Select one run, say the `08-yr/07-mo/16-da` and specify that to copy:

.. code:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-freesurfer_pp_moc freesurfer_pp_moc.py            \
            -a 08-07-16 \
            /incoming /outgoing

Simulate a processing delay
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To simulate a processing delay, specify some time in seconds:

.. code:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-freesurfer_pp_moc freesurfer_pp_moc.py            \
            -a 08-07-16                                                 \
            -P 20                                                       \
            /incoming /outgoing

Explicitly copy all the data including images from a pre-processed run
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To copy all the image directories from the ``10-yr/06-mo/01-da`` subject, 

.. code:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-freesurfer_pp_moc freesurfer_pp_moc.py            \
            -a 10-06-01                                                 \
            -c stats,sag,cor,tra,3D                                     \
            /incoming /outgoing            


