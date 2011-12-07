#!/usr/bin/env python
import argparse
import hashlib
import re
import urllib2
import BeautifulSoup
import pygoogle

PATTERNS = [  '(?P<plain>.+)\s+(?P<hash>%s)', 
		      '(?P<hash>%s):(?P<plain>.+)',
		      '(md5|MD5)\s*\(("|\')?(?P<plain>.*?)("|\')?\)\s*(=|:)\s*("|\')?(?P<hash>%s)("|\')?',
		]

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
	
HASH_VERIFIERS = { 'md5' : md5Verifier }
	
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
		matches = p.finditer(text)
		
		for match in matches:
			plain = match.group('plain')
			for possibleMatch in [plain, plain.rstrip(), plain.lstrip(), plain.strip()]:
				if verifier:
					isCorrect = verifier(possibleMatch, hash)
				
					if isCorrect:
						return plain

def crack(type, hash, urls, userAgent = None):
	"""Attempts to find the plain text for the given hash.
	
	Parameters
	
		type: str
			The type of the hash
		
		hash: str
			The hash to crack
	
	"""
	urls = urls or []
	hash = str(hash)
	type = str(type).lower()
	
	if type not in HASH_VERIFIERS:
		raise ValueError('Hash type % is not supported.' % type)
		
	verifier = HASH_VERIFIERS[type]
	
	for url in urls:
		try:
			text = getText(url, userAgent)
			plain = findHash(hash, text, verifier)
			if plain:
				return plain
		except urllib2.HTTPError, e:
			continue 

def main(hash, googleAPIKey = None, **kwargs):
	google = pygoogle.SearchAPI(key = googleAPIKey)
	
	urls = [result.url for result in google.webSearch(str(hash))]
	
	result = crack('md5', hash, urls)
	if result:
		print result
	else:
		print 'No plain text found.'

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	
	parser.add_argument('hash', action = 'store', type = str)
	parser.add_argument('-g', '--google-api-key', action = 'store', dest = 'googleAPIKey', type = str)
	
	arguments = parser.parse_args()
	
	arguments = vars(arguments)
	
	main(**arguments)
	