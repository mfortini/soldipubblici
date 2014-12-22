import zlib
import urllib
import urllib2
import json

# curl 'http://soldipubblici.gov.it/it/ricerca' -H 'Origin: http://soldipubblici.gov.it'  -H 'Accept-Encoding: gzip, deflate' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://soldipubblici.gov.it/it' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'DNT: 1'  --data 'codicecomparto=PRO&codiceente=000699123' --compressed

def scrapeSIOPE(comparto, codiceente,chi):
	url = 'http://soldipubblici.gov.it/it/ricerca'
	headers = { 'Origin': 'http://soldipubblici.gov.it',
		    'Accept-Encoding': 'gzip, deflate',
		    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		    'Accept': 'application/json, text/javascript, */*; q=0.01',
		    'Referer': 'http://soldipubblici.gov.it',
	   	    'X-Requested-With': 'XMLHttpRequest',
		    'Connection': 'keep-alive' }
	values = {'codicecomparto' : comparto,
		  'codiceente' : codiceente,
		  'chi': chi }
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	the_page = zlib.decompress(response.read(), 16+zlib.MAX_WBITS) # response.read()

	return the_page

if __name__=='__main__':
	parsed = json.loads(scrapeSIOPE('PRO',727386))
	print json.dumps(parsed,indent=4)
