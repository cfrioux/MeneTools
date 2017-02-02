# Copyright (c) 2017, Clemence Frioux <clemence.frioux@inria.fr>
#
# This file is part of MeneTools.
#
# meneco is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# meneco is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with menetools.  If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
  name             = 'MeneTools',
  version          = '1.0.0',
  url              = '',
  license          = 'GPLv3+',
  description      = 'Metabolic Network Topology Tools. Analyze the topology \
                      of metabolic networks. Explore producibility, production \
                      paths and needed initiation sources',
  long_description = open('README').read(),
  author           = 'Clemence Frioux',
  author_email     = 'clemence.frioux@inria.fr',
  packages         = ['menetools'],
  package_dir      = {'menetools' : 'src'},
  package_data     = {'menetools' : ['encodings/*.lp']},
  scripts          = ['menecof.py','menescope.py','menepath.py','menecheck.py'],
  install_requires = ['pyasp == 1.4.2']
)
