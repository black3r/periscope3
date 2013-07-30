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

import zipfile, os, urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error, logging, traceback, http.client, re, socket
from bs4 import BeautifulSoup

from . import SubtitleDatabase

LANGUAGES = {"English" : "en",
			 "English (US)" : "en",
			 "English (UK)" : "en",
			 "Italian" : "it",
			 "Portuguese" : "pt",
			 "Portuguese (Brazilian)" : "pt-br",
			 "Romanian" : "ro",
			 "Español (Latinoamérica)" : "es",
			 "Español (España)" : "es",
			 "Spanish (Latin America)" : "es",
			 "Español" : "es",
			 "Spanish" : "es",
			 "Spanish (Spain)" : "es",
			 "French" : "fr",
			 "Greek" : "el",
			 "Arabic" : "ar",
			 "German" : "de",
			 "Croatian" : "hr",
			 "Indonesian" : "id",
			 "Hebrew" : "he",
			 "Russian" : "ru",
			 "Turkish" : "tr",
			 "Swedish" : "se",
			 "Czech" : "cs",
			 "Dutch" : "nl",
			 "Hungarian" : "hu",
			 "Norwegian" : "no",
			 "Polish" : "pl",
			 "Persian" : "fa"}

class Addic7ed(SubtitleDatabase.SubtitleDB):
	url = "http://www.addic7ed.com"
	site_name = "Addic7ed"

	def __init__(self, config, cache_folder_path):
		super(Addic7ed, self).__init__(langs=None,revertlangs=LANGUAGES)
		#http://www.addic7ed.com/serie/Smallville/9/11/Absolute_Justice
		self.host = "http://www.addic7ed.com"
		self.release_pattern = re.compile(" \nVersion (.+), ([0-9]+).([0-9])+ MBs")
		

	def process(self, filepath, langs):
		''' main method to call on the plugin, pass the filename and the wished 
		languages and it will query the subtitles source '''
		fname = str(self.getFileName(filepath).lower())
		guessedData = self.guessFileData(fname)
		if guessedData['type'] == 'tvshow':
			subs = self.query(guessedData['name'], guessedData['season'], guessedData['episode'], guessedData['teams'], langs)
			return subs
		else:
			return []
	
	def query(self, name, season, episode, teams, langs=None):
		''' makes a query and returns info (link, lang) about found subtitles'''
		sublinks = []
		name = name.lower().replace(" ", "_")
		searchurl = "%s/serie/%s/%s/%s/%s" %(self.host, name, season, episode, name)
		logging.debug("dl'ing %s" %searchurl)
		try:
			socket.setdefaulttimeout(3)
			page = urllib.request.urlopen(searchurl)
		except urllib.error.HTTPError as inst:
			logging.info("Error : %s - %s" %(searchurl, inst))
			return sublinks
		except urllib.error.URLError as inst:
			logging.info("TimeOut : %s" %inst)
			return sublinks
		
		#HTML bug in addic7ed
		content = page.read()
		content = content.replace("The safer, easier way", "The safer, easier way \" />")
		
		soup = BeautifulSoup(content)
		for subs in soup("td", {"class":"NewsTitle", "colspan" : "3"}):
			if not self.release_pattern.match(str(subs.contents[1])):
				continue
			subteams = self.release_pattern.match(str(subs.contents[1])).groups()[0].lower()
			
			# Addic7ed only takes the real team	into account
			fteams = []
			for team in teams:
				fteams += team.split("-")
			teams = set(fteams)
			subteams = self.listTeams([subteams], [".", "_", " "])
			
			logging.debug("[Addic7ed] Team from website: %s" %subteams)
			logging.debug("[Addic7ed] Team from file: %s" %teams)
			logging.debug("[Addic7ed] match ? %s" %subteams.issubset(teams))
			langs_html = subs.findNext("td", {"class" : "language"})
			lang = self.getLG(langs_html.contents[0].strip().replace('&nbsp;', ''))
			#logging.debug("[Addic7ed] Language : %s - lang : %s" %(langs_html, lang))
			
			statusTD = langs_html.findNext("td")
			status = statusTD.find("strong").string.strip()

			# take the last one (most updated if it exists)
			links = statusTD.findNext("td").findAll("a")
			link = "%s%s"%(self.host,links[len(links)-1]["href"])
			
			#logging.debug("%s - match : %s - lang : %s" %(status == "Completed", subteams.issubset(teams), (not langs or lang in langs)))
			if status == "Completed" and subteams.issubset(teams) and (not langs or lang in langs) :
				result = {}
				result["release"] = "%s.S%.2dE%.2d.%s" %(name.replace("_", ".").title(), int(season), int(episode), '.'.join(subteams)
)
				result["lang"] = lang
				result["link"] = link
				result["page"] = searchurl
				sublinks.append(result)
		return sublinks
		
	def listTeams(self, subteams, separators):
		teams = []
		for sep in separators:
			subteams = self.splitTeam(subteams, sep)
		#logging.debug(subteams)
		return set(subteams)
	
	def splitTeam(self, subteams, sep):
		teams = []
		for t in subteams:
			teams += t.split(sep)
		return teams

	def createFile(self, subtitle):
		'''pass the URL of the sub and the file it matches, will unzip it
		and return the path to the created file'''
		suburl = subtitle["link"]
		videofilename = subtitle["filename"]
		srtbasefilename = videofilename.rsplit(".", 1)[0]
		srtfilename = srtbasefilename +".srt"
		self.downloadFile(suburl, srtfilename)
		return srtfilename

	def downloadFile(self, url, srtfilename):
		''' Downloads the given url to the given filename '''
		req = urllib.request.Request(url, headers={'Referer' : url, 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3)'})
		
		f = urllib.request.urlopen(req)
		dump = open(srtfilename, "wb")
		dump.write(f.read())
		dump.close()
		f.close()
		logging.debug("Download finished to file %s. Size : %s"%(srtfilename,os.path.getsize(srtfilename)))
