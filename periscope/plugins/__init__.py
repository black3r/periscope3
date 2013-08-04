# -*- coding: utf-8 -*-

#   This file is part of periscope3.
#   Copyright (c) 2013 Roman Hudec <black3r@klikni.cz>
#    
#   This file contains parts of code from periscope.
#   Copyright (c) 2008-2011 Patrick Dessalle <patrick@dessalle.be>
#
#    periscope is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    periscope is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with emesene; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#from SubtitleSource import SubtitleSource # require a key in the config file

## Working plug-ins:
from .OpenSubtitles import OpenSubtitles
from .Subtitulos import Subtitulos
from .TheSubDB import TheSubDB
from .SubsWiki import SubsWiki
from .Addic7ed import Addic7ed
from .Podnapisi2 import Podnapisi # not really sure if working, needs proper testing

## Currently not working (untested yet)
#from .SubScene import SubScene

## Currently not working (code broken / unfinished)
#from .Podnapisi import Podnapisi  # Podnapisi plug-in not working currently (on-site changes)
#from .TvSubtitles import TvSubtitles # Unfinished/Not working plug-in
#from .SubDivX import SubDivX # Broken & Not worth it (only espanol subtitles and can't really search well)

## Currently not working (site faults)
#from .LegendasTV import LegendasTV # LegendasTV plug-in not working currently (site offline + requires username/password)
#from .BierDopje import BierDopje # BierDopje plug-in not working currently (need API key)
