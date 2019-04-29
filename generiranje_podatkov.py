import auth
import csv
import pandas as pd
#auth.db = "sem2019_%s" % auth.user

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki


#Preberemo lahko podatke, ki jih imamo

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

#USTVARJANJE TABEL
#Kasnjeje bom malo spremenil zadeve, da bodo še foreign key v redu

def ustvari_tabelo_agent():
    cur.execute("""
        CREATE TABLE agent (
            id SERIAL PRIMARY KEY,
            ime TEXT NOT NULL,
            priimek TEXT NOT NULL,
        );
    """)
conn.commit()

def ustvari_tabelo_sportni_direktor():
    cur.execute("""
        CREATE TABLE sportni_direktor (
            id SERIAL PRIMARY KEY,
            ime TEXT NOT NULL,
            priimek TEXTNOT NULL,
        );
    """)
conn.commit()

def ustvari_tabelo_klub():
    cur.execute("""
        CREATE TABLE klub (
            id SERIAL PRIMARY KEY,
            ime TEXT NOT NULL,
            naslov TEXT NOT NULL,
        );
    """)
conn.commit()

#Ukazi za brisanje tabel

def pobrisi_tabelo_agent():
    cur.execute("""
        DROP TABLE agent;
    """)
conn.commit()

def pobrisi_tabelo_sportni_direktor():
    cur.execute("""
        DROP TABLE sportni_direktor;
    """)
conn.commit()

def pobrisi_klub():
    cur.execute("""
        DROP TABLE klub;
    """)
conn.commit()

#Ukazi za uvažanje podatkov

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

#Test, ali vse deluje, kot mora

def test():
    cur.execute("select * from agent")
    print(cur.fetchall())
    
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
test()
