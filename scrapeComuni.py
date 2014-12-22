from scrapeSIOPE import *
import csv
import sys
import time
import sqlite3


def main(filename):
	conn = sqlite3.connect(filename+'.db')
	cur = conn.cursor()

	with open(filename, 'r') as f:
		rd = csv.reader(f)
		headers=rd.next()
		print headers
		for row in rd:
			codice, _, _, denominazione, _, _ = row
			codice = "%09d" % (int(codice),)
			print "SEARCH", codice
			res=cur.execute("SELECT codiceente FROM comuniSIOPE WHERE codiceente = ?", (codice,))
			if len(res.fetchall()) < 1:
				print "FETCH",codice,denominazione
				try:
					SIOPE=scrapeSIOPE('PRO',codice,denominazione)
				except:
					print "ERROR",codice,denominazione
					SIOPE = None
				if SIOPE:
					cur.execute('INSERT INTO comuniSIOPE(codiceente,json) VALUES(?,?)', (codice, SIOPE))
				else:
					cur.execute('INSERT INTO comuniSIOPE(codiceente,json) VALUES(?,NULL)', (codice,))
				conn.commit()


if __name__=='__main__':
	main(sys.argv[1])



