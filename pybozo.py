#!/usr/bin/env python
import urllib2
import BeautifulSoup
import pygoogle


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
	


	
