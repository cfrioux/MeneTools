# -*- coding: utf-8 -*-

# Copyright (C) 2017-2021 Clémence Frioux & Arnaud Belcour - Inria Dyliss - Pleiade
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from setuptools import setup
import menetools

setup(
    name             = 'MeneTools',
    version          = menetools.__version__,
    url              = 'https://github.com/cfrioux/MeneTools',
    download_url     = f'https://github.com/cfrioux/MeneTools/tarball/{menetools.__version__}',
    license          = 'GPLv3+',
    description      = 'Metabolic Network Topology Analysis Tools',
    long_description = 'Python Metabolic Network Topology Tools. Analyze the \
topology of metabolic networks. Explore producibility, production paths and \
needed initiation sources. \
More information on usage and troubleshooting on Github: https://github.com/cfrioux/MeneTools',
    author           = 'Clemence Frioux',
    author_email     = 'clemence.frioux@inria.fr',
    classifiers      =[
                            'Programming Language :: Python :: 3.6',
                            'Programming Language :: Python :: 3.6',
                            'Programming Language :: Python :: 3.7',
                            'Programming Language :: Python :: 3.8',
                            'Operating System :: MacOS :: MacOS X',
                            'Operating System :: Unix',
                        ],
    packages         = ['menetools'],
    package_dir      = {'menetools' : 'menetools'},
    package_data     = {'menetools' : ['encodings/*.lp']},
    #scripts          = ['menetools/menecof.py','menetools/menescope.py','menetools/menepath.py','menetools/menecheck.py'],
    entry_points     = {'console_scripts': ['mene = menetools.__main__:main']},
    install_requires = ['clyngor_with_clingo']
)
