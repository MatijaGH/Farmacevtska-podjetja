import bottle
from bottle import *
#import auth as auth
import psycopg2, psycopg2.extensions, psycopg2.extras
import hashlib
import webbrowser

#priklop na bazo
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) #da imamo lahko sumnike
baza = psycopg2.connect(database='sem2019_matijagh', host='baza.fmf.uni-lj.si', user='matijagh', password='f3wl64em')
#baza = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
baza.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogocimo transakcije
cur = baza.cursor(cursor_factory=psycopg2.extras.DictCursor)

#bottle.TEMPLATE_PATH.insert(0,"./CoolAdmin-master")
                            

###POMOŽNE FUNKCIJE
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


###KONEC POMOŽNIH FUNKCIJ




################
#test priklopa na bazo(ni še v redu, popraviti moram program za tabelo)

##def test():
##    cur.execute('''
##                    SELECT * FROM uporabnik WHERE vloga = 'agent;'
##                    ''')
##    return (cur.fetchall())
##
##print(test())
##def test2():
##    cur.execute('''
##                    SELECT * FROM uporabnik WHERE vloga = 'igralec;'
##                    ''')
##    return (cur.fetchall())
##print(test2())

################
#bottle uvod, pomozne funkcije

static_dir = "./static"
secret = "to skrivnost je zelo tezko uganiti 1094107c907cw982982c42"

def vloga(user):
    cur.execute("SELECT pooblastilo FROM uporabnik WHERE username=%s",
              [user])
    r = cur.fetchone()[0]
    return r


#def password_md5(s):
    """Vrni MD5 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
       kodirana s to funkcijo."""
    #p = hashlib.md5()
    #p.update(s.encode('utf-8'))
    #return p.hexdigest()


def get_user(auto_login = True, auto_redir=False):
    """Poglej cookie in ugotovi, kdo je prijavljeni uporabnik,
       vrni njegov username in ime. Ce ni prijavljen, presumeri
       na stran za prijavo ali vrni None (advisno od auto_login).
    """
    # Dobimo username iz piskotka
    username = request.get_cookie('username', secret=secret) 
    print(username)
    c = baza.cursor()
    cur.execute('''
                    SELECT * FROM uporabnik WHERE uporabnisko_ime=%s
                    ''', [username])
    tmp = cur.fetchone()
    # Preverimo, ali ta uporabnik obstaja
    if username is not None:
        #Ce uporabnik ze prijavljen, nima smisla, da je na route login
        if auto_redir:
                if tmp[3] == 'igralec;':
                    redirect('/index-igralec/')
                elif tmp[3] == 'agent;':
                    redirect("/index-agent/")
                else:
                    redirect("/index-klub/")
        else:
            c = baza.cursor()
            c.execute("SELECT uporabnik FROM uporabnik WHERE uporabnisko_ime=%s",
					  [username])
            r = c.fetchone()
            c.close ()
            if r is not None:
                # uporabnik obstaja, vrnemo njegove podatke
                return r
    # Ce pridemo do sem, uporabnik ni prijavljen, naredimo redirect
    if auto_login:
        redirect('/login/')
    else:
        return None


#tukaj bo potrebno narediti še strani, kamor želimo preusmerjati in pogledati, kaj točno so parametri
def preusmeri(parameter, pooblastilo):
    if parameter == "agent":
        redirect('/index-agent/')
    elif parameter == "igralec":
        redirect('/index-igralec/')
    


@route("/static/<filename:path>")
def static(filename):
    """Splosna funkcija, ki servira vse staticne datoteke iz naslova
       /static/..."""
    return static_file(filename, root=static_dir)


################
#bottle routes
@get("/")
def zero_get():
    "Takoj preusmeri na login stran."
    curuser = get_user(auto_login = False, auto_redir = True)
    return template("login.html",
                           napaka=None,
                           username=None)


@get("/login/")
def login_get():
    """Serviraj formo za login."""
    curuser = get_user(auto_login = False, auto_redir = True)
    return template("login.html",
                           napaka=None,
                           username=None)

@post('/login/', method='post')
def do_login():
    """Obdelaj izpolnjeno formo za prijavo"""
    # Uporabnisko ime, ki ga je uporabnik vpisal v formo
    username = request.forms.get('username')
    # Spravimo geslo v bazo
    password = request.forms.get('password')
    print(username)
    print(password)
    # Preverimo, ali se je uporabnik pravilno prijavil
    c = baza.cursor()
    cur.execute('''
                    SELECT * FROM uporabnik WHERE uporabnisko_ime=%s AND geslo=%s
                    ''', [username, password])
    tmp = cur.fetchone()
    lol = tmp
    print(tmp)
    # preverimo, če je uporabnik v bazi
    if tmp is None:
            return template("login.html",
                            napaka="Nepravilna prijava.",
                            username=None
                     )
    else:
        response.set_cookie('username', username, path='/', secret=secret)
        if tmp[3] == 'igralec;':
            get_kartica_igralec(tmp)
            redirect('/index-igralec/')
        elif tmp[3] == 'agent;':
            get_kartica_agent(tmp)
            redirect("/index-agent/")
        else:
            get_kartica_klub(tmp)
            redirect("/index-klub/")
# else:
    #     # Vse je v redu, nastavimo cookie in preusmerimo na glavno stran
    #     response.set_cookie('username', username, path='/', secret=secret)
    #     redirect("/index/")



@get("/index-agent/")
def index_agent_get():
    """Serviraj formo za index1."""
    return template("index-agent.html")

@get("/index-igralec/")
def index_igralec_get():
    """Serviraj formo za index1."""
    return template("index-igralec.html")

@get("/index-klub/")
def index_klub_get():
    """Serviraj formo za index-klub.html"""
    return template("index-klub.html")

@get("/prestopi/")
def prestopi_get():
    """Serviraj formo za prestopi.html"""
    return template("prestopi.html")

@get("/register/")
def register_get():
    """Serviraj formo za registracijo"""
    curuser = get_user(auto_login = False, auto_redir = True)
    return template("register.html", username = None, ime = None,
                    priimek = None, vloga = None, email = None,
                    DatumRojstva = None, geslo = None, geslo2 = None,
                    naslov = None, država = None, napaka = None)

@post("/register/", method = 'post')
def nov_zahtevek():
    vloga= request.forms.get('vloga')
    #Za agenta
    if vloga == '1':
        username = request.forms.get('username_agent')
        ime = request.forms.get('ime_agent')
        priimek = request.forms.get('priimek_agent')
        
        email = request.forms.get('email_agent')

        geslo = request.forms.get('geslo_agent')
        geslo2 = request.forms.get('geslo2_agent')

    #Za igralca
    elif vloga == '2':
        username = request.forms.get('username_igralec')
        ime = request.forms.get('ime_igralec')
        priimek = request.forms.get('priimek_igralec')
        email = request.forms.get('email_igralec')
        DatumRojstva = str(request.forms.get('DatumRojstva_igralec'))
        država = request.forms.get('drzava')
        print(type(username))
        print(type(ime))
        print(type(priimek))
        print(type(email))
        print(type(DatumRojstva))
        print(type(država))
        print(type(str(0)))
        print(type(str(None)))
        geslo = request.forms.get('geslo_igralec')
        geslo2 = request.forms.get('geslo2_igralec')
    
    #Za klub
    else:
        username = request.forms.get('username_klub')
        ime = request.forms.get('ime_klub')
        naslov = request.forms.get('naslov_klub')
        geslo = request.forms.get('geslo_klub')
        geslo2 = request.forms.get('geslo2_klub')
        
    c1 = baza.cursor()
    c1.execute("SELECT * FROM uporabnik WHERE uporabnisko_ime=%s",
              [username])
    tmp = c1.fetchone()   
    if tmp is not None:
        return template("register.html", username = username, ime = ime,
                    priimek = priimek, vloga = vloga, email = email,
                    DatumRojstva = DatumRojstva, geslo = geslo, geslo2 = geslo2,
                    država = država, napaka="Uporabniško ime je že zavzeto, izberi novega.")

    #preverimo, ali se gesli ujemata
    if geslo != geslo2:
        return template("register.html", username = username, ime = ime,
                    priimek = priimek, vloga = vloga, email = email,
                    DatumRojstva = DatumRojstva, geslo = geslo, geslo2 = geslo2,
                    naslov = naslov, država = država, napaka="Gesli se ne ujemata!")


    #ce pridemo, do sem, je vse uredu in lahko vnesemo zahtevek v bazo

    #pogledam največji id, da bom dodajal za tem
    c1.execute("SELECT id FROM uporabnik ORDER BY id DESC LIMIT 1")
    dolzina = c1.fetchone()[0]
    id = dolzina + 1
    c = baza.cursor()
    #vnesem agenta v bazo
    if vloga == '1':
        c.execute("""INSERT INTO uporabnik (id, uporabnisko_ime, geslo, vloga)
                VALUES (%s, %s, %s, %s)""",
              [id, username, geslo, 'agent;'])
        c.execute("""INSERT INTO agent (id, ime, priimek)
                VALUES (%s, %s, %s) """,
                  [id, ime, priimek])
        return template("register.html", username = None, ime = None,
                    priimek = None, vloga = None, email = None,
                    starost = None, geslo = None, geslo2 = None,
                    naslov = None, napaka="Prošnja poslana uspešno!")
    #vnesem igralca v bazo
    elif vloga == '2':
        c.execute("""INSERT INTO uporabnik (id, uporabnisko_ime, geslo, vloga)
                VALUES (%s, %s, %s, %s)""",
              [id, username, geslo, 'igralec;'])
        c.execute("""INSERT INTO igralci (id, ime, priimek, država, plača, datum_rojstva, vrednost, klub, agent)
                VALUES (%s, %s, %s, %s, %s, %s, %s) """,
                  [id, ime, priimek, država, 0, DatumRojstva, 0, None, None])
        print("Uspeh!")
        return template("register.html", username = None, ime = None,
                    priimek = None, vloga = None, email = None,
                    starost = None, geslo = None, geslo2 = None,
                    naslov = None, napaka="Prošnja poslana uspešno!")
    #vnesem klub v bazo
    elif vloga == '3':
        print('Gasa')
        c.execute("""INSERT INTO uporabnik (id, uporabnisko_ime, geslo, vloga)
                VALUES (%s, %s, %s, %s)""",
              [id, username, geslo, 'klub;'])
        c.execute("""INSERT INTO klub (id, ime, naslov)
                VALUES (%s, %s, %s) """,
                  [id, ime, naslov])
        print("Uspeh!")
        return template("register.html", username = None, ime = None,
                    priimek = None, vloga = None, email = None,
                    starost = None, geslo = None, geslo2 = None,
                    naslov = None, napaka="Prošnja poslana uspešno!")

@get("/logout/")
def logout():
    """Pobrisi cookie in preusmeri na login."""
    response.delete_cookie('username', path='/', secret=secret)
    #print(get_user())
    redirect('/login/')

@get("/forget-pass/")
def forget_pass_get():
    """Serviraj formo za pozabjeno geslo"""
    curuser = get_user(auto_login = False, auto_redir = True)
    return template("forget-pass.html")

@get("/form/")
def form_get():
    """Serviraj formo za form"""
    return template("form.html")




run(host='localhost', port=8080)
