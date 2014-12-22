import sqlite3
import json

f = open('comuniSIOPE.json','r')

conn=sqlite3.connect('comuniSIOPE.csv.db')
cur=conn.cursor()


for row in f.readlines():
	try:
		j=json.loads(row)
	except:
		print "ERROR", row
		continue
	codiceente=j['data'][0]['cod_ente']
	print "INSERT", codiceente
	cur.execute('INSERT INTO comuniSIOPE(codiceente,json) VALUES (?,?)', (codiceente, row))

conn.commit()
conn.close()

