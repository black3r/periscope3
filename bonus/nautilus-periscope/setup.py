# -*- coding: utf-8 -*-

#   This file is part of periscope3.
#   Copyright (c) 2013 Roman Hudec <black3r@klikni.cz>
#	
#   This file contains parts of code from periscope.
#   Copyright (c) 2008-2011 Patrick Dessalle <patrick@dessalle.be>
#
#    periscope is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    periscope is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with periscope; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from setuptools import setup
import shutil
import os
from . import version

PACKAGE = 'periscope-gnome'
VERSION = version.VERSION

try:
	os.makedirs("./debian/periscope-gnome/usr/share/nautilus-python/extensions")
except:
	pass
shutil.copy('periscope-nautilus/periscope-nautilus.py', 'debian/periscope-gnome/usr/share/nautilus-python/extensions')
