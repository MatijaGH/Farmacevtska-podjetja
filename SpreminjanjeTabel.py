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

def predlagaj_prestop():
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
















    
