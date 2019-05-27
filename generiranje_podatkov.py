import auth
import csv
import pandas as pd
#auth.db = "sem2019_%s" % auth.user



# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
 
#priklop na bazo
conn = psycopg2.connect(database='sem2019_matijagh', host='baza.fmf.uni-lj.si', user='matijagh', password='f3wl64em')
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
                          ,'','','vrednost','klub','agent'],
                   sep = ',')
testigralci = list(igralci.ID)
###########

klub = pd.read_csv('Podatki/klub.csv', encoding = "ISO-8859-1",
                   error_bad_lines=False,
                   header=None,
                   names=['ID','Ime','Naslov'],
                   sep = ',')
testklub = list(klub.ID)
###########


#USTVARJANJE TABEL

def ustvari_tabelo_agent():
    cur.execute("""
        CREATE TABLE agent (
	    id SERIAL PRIMARY KEY,
	    ime VARCHAR(50),
	    priimek VARCHAR(50)
        );
    """)
    conn.commit()
####


def ustvari_tabelo_klub():
    cur.execute("""
        CREATE TABLE klub (
	    id SERIAL PRIMARY KEY,
	    Ime VARCHAR(50),
	    Naslov VARCHAR(50)
        );
    """)
    conn.commit()

def ustvari_tabelo_igralci():
    cur.execute("""
        CREATE TABLE igralci (
	        id SERIAL PRIMARY KEY,
	        ime VARCHAR(50),
	        priimek VARCHAR(50),
	        država VARCHAR(50),
	        plača INT,
	        vrednost INT,
	        klub SERIAL,
	        agent SERIAL,
	        FOREIGN KEY (klub) REFERENCES klub (id),
	        FOREIGN KEY (agent) REFERENCES agent (id)
        );
    """)
    conn.commit()

def ustvari_tabelo_prestop():
    cur.execute("""
        CREATE TABLE prestop (
	        id SERIAL PRIMARY KEY,
	        cena INT,
	        datum DATE,
	        stanje BOOLEAN,
	        igralec SERIAL,
	        iz_kluba SERIAL,
	        v_klub SERIAL,
	        agent SERIAL,
	        FOREIGN KEY (igralec) REFERENCES igralci (id),
	        FOREIGN KEY (iz_kluba) REFERENCES klub (id),
	        FOREIGN KEY (v_klub) REFERENCES klub (id),
	        FOREIGN KEY (agent) REFERENCES agent(id)
        );
    """)
    conn.commit()

#Ukazi za dodajanje podatkov v tabelo igralec(klub/agent)

def dodaj_podatke_igralci():
    for j in range(999):
        agent = random.choice(podatki/agent.csv.id)
        klub = random.choice(podatki/klub.csv.id)
        cur.execute("""
                INSERT INTO igralci
                (agent, klub)
                VALUES (%d, %d)
                RETURNING id
            """)
    conn.commit()

#Ukazi za brisanje tabel

def pobrisi_tabelo_agent():
    cur.execute("""
        DROP TABLE IF EXISTS agent CASCADE;
    """)
    conn.commit()


def pobrisi_tabelo_klub():
    cur.execute("""
        DROP TABLE IF EXISTS klub CASCADE;
    """)
    conn.commit()

def pobrisi_tabelo_prestop():
    cur.execute("""
        DROP TABLE  IF EXISTS prestop CASCADE;
    """)
    conn.commit()

def pobrisi_tabelo_igralci():
    cur.execute("""
        DROP TABLE IF EXISTS igralci CASCADE;
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
                (id, ime, priimek)
                VALUES (%s, %s ,%s)
                RETURNING id
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
                (id,Ime,Priimek,Država,Plača,Datum_rojstva,
                          ,,,vrednost,klub,agent)
                VALUES (%s, %s, %s, %s, %s,%d%d%d, %d, %d, %d,%d,%s,%s)
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
                (id, ime, naslov)
                VALUES (%s,%s,%s)
                RETURNING id
            """, r)
            rid, = cur.fetchone()
            print("Uvožen klub %s z ID-jem %d" % (r[0], rid))
    conn.commit()


#Test, ali vse deluje, kot mora

def test():
    cur.execute("select * from agent")
    print(cur.fetchall())
    

pobrisi_tabelo_agent()
pobrisi_tabelo_igralci()
pobrisi_tabelo_klub()
pobrisi_tabelo_prestop()
ustvari_tabelo_agent()
ustvari_tabelo_klub()
ustvari_tabelo_igralci()
ustvari_tabelo_prestop()
uvozi_podatke_agent()
uvozi_podatke_klubi()
uvozi_podatke_igralci()

test()
