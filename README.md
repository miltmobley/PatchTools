PatchTools
==========

Python based patch analysis tools

Do you need to apply GIT patches to a different source version than the one on
which they were developed? PatchTools can greatly accelerate the process of determining
whether the patches are needed by the new source, and how to fix them if they are needed.

Features
--------

- Detects missing files in your source tree
- Detects file that are incorrectly present in your source tree
- Detects lines are not at the line numbers specified in the patches
- Can find significant lines that are elsewhere in the same file
- Issues a readable report of errors found

Installation
------------

To install PatchTools from PyPi, simply enter::

    $ sudo pip install patchtools
    
To install PatchTools from a source tarball, obtain the tarball from pypi.org,
extract the files to a suitable location, and in the root folder, enter::

    $ sudo python setup.py install
    
    
Documentation
-------------

Documentation is available in the 'doc' folder of the source tarball.
