'''
Created on Feb 25, 2014

@author: Milton Mobley
'''

import os
import sys
import json
from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.md') as f:
    readme = f.read()

with open('COPYING.txt') as f:
    copying = f.read()

''' Read data files description, convert it to form needed by data_files
    parameter below.
'''
with open('DATAFILES.txt') as f:
    filedata = json.loads(f.read())

for index1 in range(len(filedata)):
    (dir_, files) = filedata[index1]
    # dir_ is both the source and destination folder,
    # files items are just filenames
    for index2 in range(len(files)):
        files[index2] = os.path.join(dir_, files[index2])
    filedata[index1] = (dir_, files)

setup(
    name = 'patchtools',
    version = '1.0.4',
    description = 'Linux kernel patch evaluator',
    long_description=readme + '\n\n' + copying,
    author = 'Milton Mobley',
    author_email = 'miltmobley@gmail.com',
    url = 'none',
    packages = ['patchtools',
                'patchtools.doc',
                'patchtools.lib',
                'patchtools.examples',
                'patchtools.examples.alldrivers',
                'patchtools.examples.archives',
                'patchtools.examples.capemgr',
                'patchtools.examples.dts',
                'patchtools.examples.tscadc'
                ],      
    package_data = {'' : ['*.txt','*.json']},
    data_files = filedata,
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Other Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License', 
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Topic :: Software Development :: Build Tools',
                   'Topic :: System :: Operating System Kernels :: Linux'
                   ]
    )

if __name__ == '__main__':
    pass