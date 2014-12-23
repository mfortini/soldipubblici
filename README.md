# Scraper soldipubblici.gov.it

Il sito soldipubblici.gov.it fornisce una form di ricerca per ottenere gli importi relativi a un ente, ma per ora non ha un accesso ai dati non strutturati.

## Informazioni sul sito

La pagina di ricerca è questa: http://soldipubblici.gov.it/it/ricerca e risponde a una richiesta POST

I codici degli enti si trovano qui: http://www.rgs.mef.gov.it/VERSIONE-I/e-GOVERNME1/SIOPE/Codici-deg/

### Codici degli enti (da https://github.com/openfuffa/soldipubblici )

```
curl -X GET http://soldipubblici.gov.it/it/chi/search/%20  \
-H "Accept: application/json, text/javascript, */*; q=0.01" \
-H "X-Requested-With: XMLHttpRequest" > codici_ente.json
```

Esempio di curl per Amministrazione Provinciale di Arezzo:
```
curl 'http://soldipubblici.gov.it/it/ricerca' \
-H 'Cookie: _ga=GA1.3.1924561616.1419197051; _gat=1; \ soldipubblici_session=a%3A5%3A%7Bs%3A10%3A%22\
session_id%22%3Bs%3A32%3A%22b4cff00196033cfe6ed14507f8b02a23%22%3Bs%3A10%3A%22\
ip_address%22%3Bs%3A12%3A%2282.58.31.213%22%3Bs%3A10%3A%22\
user_agent%22%3Bs%3A102%3A%22Mozilla%2F5.0+%28X11%3B\
+Linux+i686%29+AppleWebKit%2F537.36+%28KHTML%2C+like\
+Gecko%29+Chrome%2F39.0.2171.95+Safari%2F537.36%22%3Bs%3A13%3A%22\
last_activity%22%3Bi%3A1419197838%3Bs%3A9%3A%22\
user_data%22%3Bs%3A0%3A%22%22%3B%7D0ae8e5ec20fc3e3182873513581950a53c8c00be'\
-H 'Origin: http://soldipubblici.gov.it'\
-H 'Accept-Encoding: gzip, deflate'\
-H 'Accept-Language: it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4'\
-H 'User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36\
(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'\
-H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8'\
-H 'Accept: application/json, text/javascript, */*; q=0.01'\
-H 'Referer: http://soldipubblici.gov.it/it'\
-H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive'\
-H 'DNT: 1' --data 'codicecomparto=PRO&codiceente=000699123&\
chi=AMMINISTRAZIONE+PROVINCIALE+DI+AREZZO&cosa=' --compressed
```

Esempio minimale di curl: 
```
curl 'http://soldipubblici.gov.it/it/ricerca'\
-H 'Origin: http://soldipubblici.gov.it'\
-H 'Accept-Encoding: gzip, deflate'\
-H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8'\
-H 'Accept: application/json, text/javascript, */*; q=0.01'\
-H 'Referer: http://soldipubblici.gov.it/it'\
-H 'X-Requested-With: XMLHttpRequest'\
-H 'Connection: keep-alive'\
-H 'DNT: 1'\
--data 'codicecomparto=PRO&codiceente=000699123' --compressed
```

Codice ente è sempre di 9 cifre, con padding a sinistra con 0

Per regione codice comparto = 'REG', per province e comuni = 'PRO'

Il valore ritornato è un array JSON

## Esempio di codice scraper python

```python
import zlib
import urllib
import urllib2
import json


def scrapeSIOPE(comparto, ente,chi):
        codiceente = '%09d' % (ente,)
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
```

# Risultato dello scrape

## Comuni

Lo scrape dei comuni al 2014-12-22 è reperibile in formato SQLITE3 qui: http://www.matteofortini.it/SOD/soldipubblici/comuniSIOPE_2014-12-22.sqlite3

Lo scrape del DB completo al 2014-12-22 è reperibile in formato SQLITE3 qui:
http://www.matteofortini.it/SOD/soldipubblici/allSIOPE_2014-12-22.sqlite3

La licenza di distribuzione dei dati è CC-BY 3.0.


