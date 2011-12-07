# pybozo

pybozo is a cracker which uses Google searches to find the
plain text of a hash.

Direct inspiration is [BozoCrack](https://github.com/juuso/BozoCrack), which is a very similar program
written in Ruby.
	
I do remember reading a long time ago that Google had managed
to index enough pages with MD5 hashes on to make this possible,
(before I came across BozoCrack) but I have completely forgotten 
the original source - thank you whoever you are!

## Installation


	git clone http://github.com/petedmarsh/pybozo.git

## Usage

	
	pybozo.py [-h] [-g GOOGLEAPIKEY] [-t {md5}] [-u USERAGENT] hash

	positional arguments:
		hash                  The hash to crack.

	optional arguments:
		-h, --help            show this help message and exit
		-g GOOGLEAPIKEY, --google-api-key GOOGLEAPIKEY
                        A Google API key to pass when making a search. Not
                        required but highly recomended
		-t {md5}, --hash-type {md5}
                        The type of the hash to be cracked.
		-u USERAGENT, --user-agent USERAGENT
                        A User-Agent string to pass to websites that are
                        scraped for potential plain text.

### Example

	python pybozo.py 5f4dcc3b5aa765d61d8327deb882cf99
	password