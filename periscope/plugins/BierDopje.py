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

import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import logging
import os
import pickle
from xml.dom import minidom
import configparser

from . import SubtitleDatabase
from periscope import version

log = logging.getLogger(__name__)

exceptions = {
    'the office' : 10358,
    'the office us' : 10358,
    'greys anatomy' : 3733,
    'sanctuary us' : 7904,
    'human target 2010' : 12986,
    'csi miami' : 2187,
    'castle 2009' : 12708,
    'chase 2010' : 14228,
    'the defenders 2010' : 14225,
    'hawaii five-0 2010' : 14211,
}

class BierDopje(SubtitleDatabase.SubtitleDB):
    url = "http://bierdopje.com/"
    site_name = "BierDopje"

    def __init__(self, config, cache_folder_path):
        super(BierDopje, self).__init__(None)
        #http://api.bierdopje.com/23459DC262C0A742/GetShowByName/30+Rock
        #http://api.bierdopje.com/23459DC262C0A742/GetAllSubsFor/94/5/1/en (30 rock, season 5, episode 1)
        self.api = None
        try:
            key = config.get("BierDopje", "key") # You need to ask for it
            if key != "":
                self.api = "http://api.bierdopje.com/%s/" %key
        except configparser.NoSectionError:
            config.add_section("BierDopje")
            config.set("BierDopje", "key", "")
            config_file = os.path.join(cache_folder_path, "config")
            configfile = open(config_file, "w")
            config.write(configfile)
            configfile.close()
            return
        self.headers = {'User-Agent' : 'periscope/%s' % version.VERSION}
        self.cache_path = os.path.join(cache_folder_path, "bierdopje.cache")
        if not os.path.exists(self.cache_path):
            log.info("Creating cache file %s" % self.cache_path)
            f = open(self.cache_path, 'w')
            pickle.dump({'showids' : {}}, f)
            f.close()
        f = open(self.cache_path, 'r')
        self.cache = pickle.load(f)
        f.close()

    def process(self, filepath, langs):
        ''' main method to call on the plugin, pass the filename and the wished 
        languages and it will query the subtitles source '''
        fname = self.getFileName(filepath)
        try:
            subs = self.query(fname, langs)
            if not subs and fname.rfind(".[") > 0:
                # Try to remove the [VTV] or [EZTV] at the end of the file
                teamless_filename = fname[0 : fname.rfind(".[")]
                subs = self.query(teamless_filename, langs)
                return subs
            else:
                return subs
        except Exception as e:
            log.exception("Error raised by plugin")
            return []
            
    def createFile(self, subtitle):
        '''get the URL of the sub, download it and return the path to the created file'''
        sublink = subtitle["link"]
        subpath = subtitle["filename"].rsplit(".", 1)[0] + '.srt'
        self.downloadFile(sublink, subpath)
        return subpath
    
    def query(self, token, langs=None):
        ''' makes a query and returns info (link, lang) about found subtitles'''
        if not self.api:
            log.error("BierDopje requires an API key. Ask a personnal on on http://www.bierdopje.com/forum")
            return []
            
        guessedData = self.guessFileData(token)
        if "tvshow" != guessedData['type'] :
            return []
        elif langs and not set(langs).intersection((['en', 'nl'])): # lang is given but does not include nl or en
            return []
            
        if not langs :
            availableLangs = ['nl', 'en']
        else :
            availableLangs = list(set(langs).intersection((['en', 'nl'])))
        log.debug("possible langs : %s " % availableLangs)

        sublinks = []
        
        # Query the show to get the show id
        showName = guessedData['name'].lower()
        if showName in exceptions:
            show_id = exceptions.get(showName)
        elif showName in self.cache['showids']:
            show_id = self.cache['showids'].get(showName)
        else :
            getShowId_url = "%sGetShowByName/%s" %(self.api, urllib.parse.quote(showName))
            log.debug("Looking for show Id @ %s" % getShowId_url)
            
            req = urllib.request.Request(getShowId_url, headers = self.headers )
            page = urllib.request.urlopen(req)
            dom = minidom.parse(page)
            if not dom or len(dom.getElementsByTagName('showid')) == 0 :
                page.close()
                return []
            show_id = dom.getElementsByTagName('showid')[0].firstChild.data
            self.cache['showids'][showName] = show_id
            f = open(self.cache_path, 'w')
            pickle.dump(self.cache, f)
            f.close()
            page.close()
        
        # Query the episode to get the subs
        for lang in availableLangs :
            getAllSubs_url = "%sGetAllSubsFor/%s/%s/%s/%s" %(self.api, show_id, guessedData['season'], guessedData['episode'], lang)
            log.debug("Looking for subs @ %s" %getAllSubs_url)
            req = urllib.request.Request(getAllSubs_url, headers = self.headers )
            page = urllib.request.urlopen(req)
            dom = minidom.parse(page)
            page.close()
            for sub in dom.getElementsByTagName('result'):
                release = sub.getElementsByTagName('filename')[0].firstChild.data
                if release.endswith(".srt"):
                    release = release[:-4]
                dllink = sub.getElementsByTagName('downloadlink')[0].firstChild.data
                log.debug("Release found : %s" % release.lower())
                log.debug("Searching for : %s" % token.lower())
                if release.lower() == token.lower():
                    result = {}
                    result["release"] = release
                    result["link"] = dllink
                    result["page"] = dllink
                    result["lang"] = lang
                    sublinks.append(result)
            
        return sublinks
