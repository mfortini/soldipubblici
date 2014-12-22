#sqlite> CREATE TABLE codici_siope(codice TEXT PRIMARY KEY, descrizione TEXT);
#sqlite> CREATE TABLE codici_enti(codice TEXT PRIMARY KEY, descrizione TEXT);
#sqlite> CREATE TABLE importi(codice_siope TEXT REFERENCES codici_siope(codice));
#sqlite> drop table importi;
#sqlite> CREATE TABLE importi(codice_siope TEXT REFERENCES codici_siope(codice), codice_ente TEXT REFERENCES codici_enti(codice), anno INTEGER, codice_gestionale TEXT, idtable TEXT, imp_uscite_att INTEGER, importo_2013 INTEGER, importo_2014 INTEGER, importo_2015 INTEGER, periodo INTEGER); 


import json
import sqlite3

conn=sqlite3.connect('comuniSIOPE.csv.db');
cur=conn.cursor()
cur2=conn.cursor()
curINS=conn.cursor()


res=cur.execute('SELECT * FROM comuniSIOPE')

for row in res:
	js = row[1]
	if js is not None and len(js) > 0:
		j=json.loads(js)
		data = j['data']
		for d in data:
			res = cur2.execute('SELECT * FROM codici_enti WHERE codice = ?', (d['cod_ente'],))
			tmp=res.fetchall()
			if len(tmp) < 1:
				print "INSERT ENTE", d['cod_ente']
				curINS.execute('INSERT INTO codici_enti(codice, descrizione) VALUES (?,?)', (d['cod_ente'],d['descrizione_ente']))
			res = cur2.execute('SELECT * FROM codici_siope WHERE codice= ?', (d['codice_siope'],))
			tmp=res.fetchall()
			if len(tmp) < 1:
				print "INSERT CODICE", d['codice_siope']
				curINS.execute('INSERT INTO codici_siope(codice, descrizione) VALUES (?,?)', (d['codice_siope'],d['descrizione_codice']))
			print "INSERT IMPORTO", d['cod_ente'],d['codice_siope'],d['descrizione_codice']
			curINS.execute('INSERT INTO importi(codice_siope, codice_ente, anno, codice_gestionale, idtable, imp_uscite_att, importo_2013, importo_2014, importo_2015, periodo) VALUES (?,?,?,?,?,?,?,?,?,?)', (d['codice_siope'],d['cod_ente'],d['anno'],d['codice_gestionale'],d['idtable'],d['imp_uscite_att'],d['importo_2013'],d['importo_2014'],d['importo_2015'],d['periodo']))

conn.commit()
