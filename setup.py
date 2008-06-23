#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tasoristikko: Tasristikkoja ratkaiseva ohjelma
# Copyright (C) 2008 Ville Leskinen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pyTasoristikko

from distutils.core import setup
from distutils.cmd import Command
from distutils.errors import *

import sys

class build_doc(Command):
    description = 'Luodaan dokumentaatio.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            from epydoc import cli
            old_argv = sys.argv[1:]
            sys.argv[1:] = [
                    '--config=epydoc.conf'
                    ]
            cli.cli()
            sys.argv[1:] = old_argv

        except ImportError:
            print 'epydoc ei asennettuna, ei tehdä dokumentaatiota'

setup(name = 'tasoristikko',
      description = 'Tasoristikkoja ratkaiseva ohjelma.',
      version = pyTasoristikko.__version__,
      author = pyTasoristikko.__author__,
      author_email = 'vleskinen@gmail.com',
      url = pyTasoristikko.__url__,
      license = pyTasoristikko.__license__,
      scripts = ['tasoristikko'],
      packages = ['pyTasoristikko', 'pyTasoristikko.Qt4Gui'],
      cmdclass = {
          'build_doc': build_doc
          })
