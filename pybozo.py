#!/usr/bin/env python

"""A Python implementation of BozoCrack

	https://github.com/juuso/BozoCrack

Performs a Google search to find the plain text for a given hash
(which turns out to be a lot more effective than you think it would!)

"""

import argparse
import hashlib
import itertools
import re
import urllib
import urllib2
import BeautifulSoup

__author__ = "Peter Marsh"
__copyright__ = "Copyright 2011, Peter Marsh"
__licence__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = "Peter Marsh"
__email__ = "pete.d.marsh@gmail.com"

class PyGoogle(object):
	"""A very simple interface to Google's REST search API it is intended
	as a backup for when pygoogle is not installed.
	
	"""
	
	class Result(object):
		"""A very simple wrapper around object which provides a 
		url attribute. The main body of the code uses the url attribute
		of pygoogle.Search, this is to mimic that.
		"""
		def __init__(self, url):
			self.url = url
	
	def __init__(self):
		self.key = None
		self.urlPattern = re.compile('"url"\s*:\s*"(?P<url>[^"]+)?"')
		
		
	def SearchAPI(self, key = None):
		if key:
			self.key = str(key)
		return self
		
	def webSearch(self, hash):
		
		parameters = {'q' : str(hash), 'v' : '1.0' }
		if self.key:
			parameters['key'] = str(self.key)
		
		parameters = urllib.urlencode(parameters)
		
		
		apiURL = 'https://ajax.googleapis.com/ajax/services/search/web?' + parameters
		
		results = []
		
		try:
			connection = urllib2.urlopen(apiURL)
			response = connection.read()
			for url in self.urlPattern.finditer(response):
				result = self.Result(url.group('url'))
				results.append(result)
			
		except:
			pass
		
		return results
		
try:
	import pygoogle
except ImportError, e:
	pygoogle = PyGoogle()
		

class MD5Cracker(object):
	
	
	PATTERNS = [  '(?P<plain>.+)\s+(?P<hash>%s)', 
		      '(?P<hash>%s):(?P<plain>.+)',
		      '(md5|MD5)\s*\(("|\')?(?P<plain>.*?)("|\')?\)\s*(=|:)\s*("|\')?(?P<hash>%s)("|\')?',
		]

	def __init__(self, patterns = None):
		self.patterns = patterns or self.PATTERNS
		
	def matches(self, hash, text):
		"""Attempts to find a hash code and it's plain text in some text.
	
		Parameters
			
			hash: str
				The hash to find
			
			text: str
				The text to find the hash and it's plain text within
	
		
		Returns
		
			A set of plain text matches, where each element hashes to the
			provided hash and all elements are unique (will usually contain
			one element, but it is possible that a collision case has been found)
	
		"""
	
		hash = str(hash)
		
		possibleMatches = set()
		
		for pattern in self.patterns:
			p = re.compile(pattern % hash)
			matches = p.finditer(text)
			
			for match in matches:
				plain = match.group('plain')
				possibleMatches.update([plain, plain.rstrip(), plain.lstrip(), plain.strip()])
		
		matches = itertools.ifilter(lambda plain: self.verify(plain, hash), possibleMatches)
		
		return matches
		
	
	def verify(self, plain, hash):
		"""Verifies that the MD5 hash of the given plan text
		is equal to a specified hash i.e. does md5(plain) == hash
			
		Parameters
			
			plain: str
				The plain text to check
				
			hash: str	
				The hash to check against
				
		Return
				
			True if hash is the MD5 of plain, False otherwise
				
		"""
		h = hashlib.md5()
		h.update(plain)
		return h.hexdigest() == hash
	
def getText(url, userAgent = None):
	"""Gets all of the text on a web page.
	
	Parameters
		
		url: str
			The url of the web page to scrape
	
	Returns
	
		All of the text from the web page as a str
	
	"""
	headers = {}
	if userAgent:
		headers['User-Agent'] = str(userAgent)
	
	request = urllib2.Request(str(url), headers = headers)
	connection = urllib2.urlopen(request)
	soup = BeautifulSoup.BeautifulSoup( connection.read() )
	tags = soup.findAll(text = True)
	text = reduce(lambda tag,text : tag + str(text), tags, '')
	return text


def main(hash, cracker, googleAPIKey = None, userAgent = None, **kwargs):
	"""Find the plain text of a hash using the power of Google
	
	Parameters
	
		hash: str
			The hash to find the plain text for
		
		cracker: pybozo.Cracker
			The cracker which will look for the plain text of 
			the hash in some text. Currently only pybozo.MD5Cracker
			exists, but anything which implements it's interface
			will work
		
		googleAPIKey: str [Optional]
			Google search API key
		
		userAgent: str [Optional]
			A user agent string to pass when downloading a web page.
			Some sites (e.g. Wikipedia) automatically reject requests
			which pass Python's default user agent string.
	
	Returns
		
		A set of plain text matches for the given hash.
		
	"""
	
	google = pygoogle.SearchAPI(key = googleAPIKey)
	
	urls = [result.url for result in google.webSearch(str(hash))]
	
	for url in urls:
		try:
			text = getText(url, userAgent)
			matches = cracker.matches(hash, text)
			if matches:
				for match in matches:
					print match
				return matches
		except urllib2.HTTPError, e:
			continue 

if __name__ == '__main__':
	
	CRACKERS = {'md5' : MD5Cracker }
	
	parser = argparse.ArgumentParser()
	parser.set_defaults(cracker = 'md5')
	
	parser.add_argument('hash', action = 'store', type = str, help = 'The hash to crack.')
	parser.add_argument('-g', '--google-api-key', action = 'store', dest = 'googleAPIKey', type = str, help = 'A Google API key to pass when making a search. Not required but highly recomended')
	parser.add_argument('-t', '--hash-type', action = 'store', dest = 'cracker', type = str, choices = CRACKERS, help = 'The type of the hash to be cracked.')
	parser.add_argument('-u', '--user-agent', action = 'store', dest = 'userAgent', type = str, help = 'A User-Agent string to pass to websites that are scraped for potential plain text.')
	
	arguments = parser.parse_args()
	
	arguments = vars(arguments)
	
	arguments['cracker'] = CRACKERS[arguments['cracker']]()
	
	main(**arguments)
	