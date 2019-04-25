import auth
import csv
import pandas as pd
auth.db = "sem2019_%s" % auth.user
# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

agent = pd.read_csv('Podatki/agent.csv', encoding = "ISO-8859-1",
                   error_bad_lines=False,
                   header=None,
                   names=['ID', 'Ime', 'Priimek'],
                   sep = ',')
testagent = list(agent.ID)

###########
igralci = pd.read_csv('Podatki/igralci.csv', encoding = "ISO-8859-1",
                   error_bad_lines=False,
                   header=None,
                   names=['ID', 'Ime', 'Priimek','Država','Plača','Datum_rojstva',''
                          ,'','','vrednost'],
                   sep = ',')
testigralci = list(igralci.ID)
###########

klub = pd.read_csv('Podatki/klub.csv', encoding = "ISO-8859-1",
                   error_bad_lines=False,
                   header=None,
                   names=['ID','Ime','Naslov'],
                   sep = ',')
testigralci = list(igralci.ID)
###########

sportni_direktor = pd.read_csv('Podatki/sportni_direktor.csv', encoding = "ISO-8859-1",
                   error_bad_lines=False,
                   header=None,
                   names=['ID', 'Ime', 'Priimek'],
                   sep = ',')
testsportni_direktor = list(sportni_direktor.ID)



def uvozi_podatke_agent():
    with open("Podatki/agent.csv") as f:
        rd = csv.reader(f)
        next(rd) # izpusti naslovno vrstico
        for r in rd:
            r = [None if x in ('', '-') else x for x in r]
            cur.execute("""
                INSERT INTO agent
                (ID, Ime,Priimek)
                VALUES (%d,%s ,%s)
                RETURNING ID
            """, r)
            rid, = cur.fetchone()
            print("Uvožen agent %s z ID-jem %d" % (r[0], rid))
conn.commit()

def uvozi_podatke_igralci():
    with open("Podatki/igralci.csv") as f:
        rd = csv.reader(f)
        next(rd) 
        for r in rd:
            r = [None if x in ('', '-') else x for x in r]
            cur.execute("""
                INSERT INTO igralci
                (ID,Ime,Priimek,Država,Plača,Datum_rojstva,
                          ,,,vrednost)
                VALUES (%d, %s, %s, %s, %s,%d%d%d, %d, %d, %d,%d)
                RETURNING id
            """, r)
            rid, = cur.fetchone()
            print("Uvožen igralec %s z ID-jem %d" % (r[0], rid))
conn.commit()

def uvozi_podatke_klubi():
    with open("Podatki/klub.csv") as f:
        rd = csv.reader(f)
        next(rd) 
        for r in rd:
            r = [None if x in ('', '-') else x for x in r]
            cur.execute("""
                INSERT INTO klub
                (ID,Ime, Naslov)
                VALUES (%d,%s,%s)
                RETURNING id
            """, r)
            rid, = cur.fetchone()
            print("Uvožen klub %s z ID-jem %d" % (r[0], rid))
conn.commit()

def uvozi_podatke_sportni_direktor():
    with open("Podatki/klub.csv") as f:
        rd = csv.reader(f)
        next(rd) 
        for r in rd:
            r = [None if x in ('', '-') else x for x in r]
            cur.execute("""
                INSERT INTO sportni_direktor
                (ID,Ime, Priimek)
                VALUES (%d,%s,%s)
                RETURNING id
            """, r)
            rid, = cur.fetchone()
            print("Uvožen sportni direktor %s z ID-jem %d" % (r[0], rid))
conn.commit()

conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

