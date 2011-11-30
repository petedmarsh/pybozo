#!/usr/bin/env python
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


	
