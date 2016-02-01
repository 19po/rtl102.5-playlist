#!/usr/bin/env python
#-*- coding: utf-8 -*-

# ------------------ #
#   RTL 102.5 info   #
# ------------------ #

import urllib
from xml.dom.minidom import parse
import re
import os
import json

def uni(s):
	"""
	Decode text.
	"""
	ascii_char = re.findall(r'\d+', s)
	other_char = re.findall(r'\[[a-z]\]+', s)
	
	for char in ascii_char:
		if char in s:
			s = s.replace(char , unichr(int(char)))

 	for char in other_char:
		if char in s:
			s = s.replace(char , '')
	return s

def get_info():
	"""
	Get information.
	"""
	# check if VLC is turned on
	try:
		urllib.urlretrieve('http://127.0.0.1:8080/requests/status.xml', '/tmp/info.xml')
	except IOError:
		print 'VLC is closed.'
		return None
	
	# replace html characters with xml
	with open('/tmp/info.xml', 'r') as fr, open('/tmp/info2.xml', 'w') as fw:
		z = ['&lt;', '&gt;']
		x = ['<', '>']
		
		for line in fr.readlines():
			for i in range(len(z)):
				if z[i] in line:
					line = line.replace(z[i], x[i])
			fw.write(line)

	# open xml file, get information and make json file
	with open('/tmp/info2.xml', 'r') as fr:
		dom = parse(fr)
		cnodes =  dom.childNodes
	
		info_dict = {"programme":"", "speakers":"", "prog-image":"",
					"artist":"", "song":"", "song-cover":""}
		try:
			info_dict["programme"] = uni(cnodes[0].\
						getElementsByTagName('prg_title')[0].firstChild.data)
			info_dict["speakers"] = uni(cnodes[0].\
						getElementsByTagName('speakers')[0].firstChild.data)
			info_dict["prog-image"] = cnodes[0].\
						getElementsByTagName('image400')[0].firstChild.data
							
			info_dict["artist"] = uni(cnodes[0].\
					getElementsByTagName('mus_art_name')[0].firstChild.data)
			info_dict["song"] = uni(cnodes[0].\
					getElementsByTagName('mus_sng_title')[0].firstChild.data)
			info_dict["song-cover"] = cnodes[0].\
			getElementsByTagName('mus_sng_itunescoverbig')[0].firstChild.data
		
		except IndexError or AttributeError:
			pass
		# save as json file
		with open('rtl1025-playlist.json', 'w') as fw:
			fw.write(json.dumps(info_dict))	
	
	# display data
	with open('rtl1025-playlist.json', 'r') as fw:
		j = json.load(fw)
		for k, v in j.iteritems():
			print "{:11}{:2}{:1}".format(k, ":", v)			


get_info()

