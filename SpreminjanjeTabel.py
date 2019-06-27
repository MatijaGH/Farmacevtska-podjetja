#V tej datoteki bomo napisali program za vstavljanje in spreminjanje podatkov
#pri igralcih in prestopih.

#Kako bomo opravili prestop? Najprej bo nekdo(klub/agent) v tabelo prestop
#dodal predlagan prestop(igralca, datum, ceno, novo plačo...). Nato bo nasprotna
#stranka dobila predlagan prestop in se odločila ali ga potrdi. Nato bo predlog
#posredovan nasprotnemu klubu. Če ga potrdi, se mu bo spremenil klub, plača in vrednost.
#ČE katerakoli od treh strank prestop zavrne, se bo shranil v tabelo kot nedokončan
#, torej false.

#Na strani od kluba_agenta, bomo imeli opcijo Predlagaj prestop, kjer bosta
#stranki imeli za izpolnit formo(izbrati igralca, vnesti datum, plačo, ...)
#To se bo nato vstavilo v tabelo prestopi in posredovalo v potrjevanje.

def predlagaj_prestop(igralec, cena, datum, ):
    cur.execute("""
        INSERT INTO prestop
        (id_igralec, cena, datum, potrjen)
        VALUES (%d, %d, '%s', 'FALSE')
        RETURNING id
        """, r)
    rid, = cur.fetchone()
    print("Uvožen prestop %s z ID-jem %d" % (r[0], rid))
    conn.commit()

def potrjevanje_prestopa(potrdilo):
    cur.execute("""
        UPDATE prestop SET potrjen = potrdilo
        WHERE potrdilo = %s
        """, r)
    rid, = cur.fetchone()
    print("Potrjen prestop %s z ID-jem  %d" % (r[0], rid))
    conn.commit()

def posodobitev_podatkov_igralec(nova_plača, nova_vrednost, nov_klub):
    cur.execute("""
        UPDATE igralec SET plača = nova_plača, vrednost = nova_vrednost, klub = nov_klub
        WHERE nova_plača = %d, nova_vrednost = %d, nov_klub = %s
        """, r)
    rid, = cur.fetchone()
    print("Spremeba podatkov igralca %s z ID-jem  %d" % (r[0], rid))
    conn.commit()


def zamenjaj_agenta(nov_agent):
    cur.execute("""
        UPDATE igralec SET agent = nov_agent
        WHERE nov_agent = %s
        """, r)
    rid, = cur.fetchone()
    print("Agent %s z ID-jem  %d" % (r[0], rid))
    conn.commit()

###Iskanje oseb
###Veliko lažje, če najprej pove kaj išče in nato samo pregledamo

def poisci(vnos):
    if not isinstance(vnos,int):
        return None
    else:
        if vnos <= 1000:
            cur.execute("""SELECT * FROM igralci WHERE id = %d""",
                    [vnos])
            podatki = cur.fetchone()
        elif vnos <= 2000:
            cur.execute("""SELECT * FROM agent WHERE id = %d""",
                    [vnos])
            podatki = cur.fetchone()
        else:
            cur.execute("""SELECT * FROM klub WHERE id = %d""",
                    [vnos])
            podatki = cur.fetchone()


###PRESTOPI
def poglej_vse_prestope():
    cur.execute("""SELECT * FROM prestopi""")
    return cur.fetchall()

def poglej_neuspele_prestope():
    cur.execute("""SELECT * FROM prestopi WHERE stanje = FALSE""")
    return cur.fetchall()

def poglej_uspele_prestope():
    cur.execute("""SELECT * FROM prestopi WHERE stanje = TRUE""")
    return cur.fetchall()
    
##def poisci(vnos):
##    if isinstance(vnos,int):
##        if vnos <= 1000:
##            cur.execute("""SELECT * from igralci WHERE id = %d""",
##                        [vnos])
##            podatki = cur.fetchone()
##        else if vnos <= 2000:
##            cur.execute("""SELECT * from agent WHERE id = %d""",
##                        [vnos])
##            podatki = cur.fetchone()
##        else:
##            cur.execute("""SELECT * from klub WHERE id = %d""",
##                        [vnos])
##            podatki = cur.fetchone()
##    else:
##        if 


    

###Za igralca
###Kartica profila
def get_kartica_igralec(tmp):
    c = baza.cursor()
    cur.execute("""
        SELECT * FROM igralci WHERE id = %s""",
        [tmp[0]])
    podatki = cur.fetchone()
    global ime
    global priimek
    global drzava
    global placa
    global datum_rojstva
    global vrednost
    global klub
    global agent
    ime = podatki[1]
    priimek = podatki[2]
    drzava = podatki[3]
    placa = podatki[4]
    datum_rojstva = podatki[5]
    vrednost = podatki[6]
    klub = podatki[7]
    agent = podatki[8]

def get_kartica_agent(tmp):
    c = baza.cursor()
    cur.execute("""
        SELECT * FROM agent WHERE id = %s""",
        [tmp[0]])
    podatki = cur.fetchone()
    global ime
    global priimek
    ime = podatki[1]
    priimek = podatki[2]

def get_kartica_klub(tmp):
    c = baza.cursor()
    cur.execute("""
        SELECT * FROM klub WHERE id = %s""",
        [tmp[0]])
    podatki = cur.fetchone()
    global ime
    global naslov
    ime = podatki[1]
    naslov = podatki[2]















    
