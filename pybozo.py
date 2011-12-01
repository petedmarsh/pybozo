#!/usr/bin/env python
import hashlib
import re
import urllib2
import BeautifulSoup
import pygoogle


PATTERNS = [ '(?P<hash>%s):(?P<plain>.+)']

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

def findHash(hash, text, verifier):
	"""Attempts to find a hash code and it's plain text in some text.
	
	Parameters
		
		hash: str
			The hash to find
			
		text: str
			The text to find the hash and it's plain text within
		
		verifier: callable
			A callable which takes two strs as an arguments, the hash
			and the possible plain text. The verifier must return True
			if the given plain text is correct and False otherwise.
		
	Returns
		
		The plaintext of the hash or None if it could not be found
	
	"""
	
	hash = str(hash)
	
	for pattern in PATTERNS:
		p = re.compile(pattern % hash)
		match = p.search(text)
		if match:
			
			plain = match.group('plain')
			
			for possibleMatch in [plain, plain.rstrip(), plain.lstrip(), plain.strip()]:
				if verifier:
					isCorrect = verifier(possibleMatch, hash)
				
					if isCorrect:
						return plain

def md5Verifier(plain, hash):
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
	
