#!/usr/bin/env python
import re
import urllib2
import BeautifulSoup
import pygoogle


PATTERNS = [ '%s:(?P<plain>.+)']

google = pygoogle.SearchAPI()

def search(hash):
	"""Performs a Google web search for the given hash code
	
	Parameters
		
		hash: str
			A hash code
		
	Returns
		
		A list of URLs of pages containing the hash
	
	"""
	
	urls = [result.url for result in google.webSearch(str(hash))]
	return urls
	
def getText(url):
	"""Gets all of the text on a web page.
	
	Parameters
		
		url: str
			The url of the web page to scrape
	
	Returns
	
		All of the text from the web page as a str
	
	"""

	connection = urllib2.urlopen( str(url) )
	soup = BeautifulSoup.BeautifulSoup( connection.read() )
	tags = soup.findAll(text = True)
	return tags

def findHash(hash, text):
	"""Attempts to find a hash code and it's plaintext in some text.
	
	Parameters
		
		hash: str
			The hash to find
			
		text: str
			The text to find the hash and it's plaintext within
	
	Returns
		
		The plaintext of the hash or None if it could not be found
	
	"""
	
	hash = str(hash)
	
	for pattern in PATTERNS:
		p = re.compile(pattern % hash)
		match = p.search(text)
		if match:
			return match.group('plain')

	
