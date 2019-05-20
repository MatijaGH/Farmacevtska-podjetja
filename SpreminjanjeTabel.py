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
        (cena, datum, potrjen)
        VALUES (%d, '%s', 'FALSE')
        RETURNING id
        """,)
    rid, = cur.fetchone()
    print("Uvožen prestop %s z ID-jem %d" % (r[0], rid))
    conn.commit()

def potrjevanje_prestopa(potrjen):
    
