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
                            


################
#test priklopa na bazo(ni še v redu, popraviti moram program za tabelo)
def test(ime):
    cur.execute('''
                    SELECT * FROM agent WHERE id=%s
                ''', [ime])
    return (cur.fetchall())

print(test(3))

################
#bottle uvod, pomozne funkcije

static_dir = "./static"
secret = "to skrivnost je zelo tezko uganiti 1094107c907cw982982c42"

def vloga(user):
    cur.execute("SELECT pooblastilo FROM uporabnik WHERE username=%s",
              [user])
    r = cur.fetchone()[0]
    return r


def password_md5(s):
    """Vrni MD5 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
       kodirana s to funkcijo."""
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

print(password_md5("psimonds0"))

def get_user(auto_login = True, auto_redir=False):
    """Poglej cookie in ugotovi, kdo je prijavljeni uporabnik,
       vrni njegov username in ime. Ce ni prijavljen, presumeri
       na stran za prijavo ali vrni None (advisno od auto_login).
    """
    # Dobimo username iz piskotka
    username = request.get_cookie('username', secret=secret)
    # Preverimo, ali ta uporabnik obstaja
    if username is not None:
        #Ce uporabnik ze prijavljen, nima smisla, da je na route login
        if auto_redir:
            redirect('/index/')
        else:
            c = baza.cursor()
            c.execute("SELECT username FROM uporabnik WHERE username=%s",
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
##def preusmeri(parameter, pooblastilo):
##    if parameter == "agent":
##        redirect('/indexagent/')
##    elif parameter == "sportni_direktor":
##        redirect('/indexsportni_direktor/')
##    elif parameter == 'raziskovalec':
##        if pooblastilo == 'zdravnik':
##            redirect('/index/')
##        elif pooblastilo == 'direktor':
##    redirect('/indexdirektor/')


@route("/static/<filename:path>")
def static(filename):
    """Splosna funkcija, ki servira vse staticne datoteke iz naslova
       /static/..."""
    return static_file(filename, root=static_dir)


################
#bottle routes
@get("/login/")
def login_get():
    """Serviraj formo za login."""
    curuser = get_user(auto_login = False, auto_redir = True)
    return template("login.html",
                           napaka=None,
                           username=None)

@get("/index-agent/")
def index_get():
    """Serviraj formo za index1."""
    return template("index-agent.html")

@get("/index-igralec/")
def index_get():
    """Serviraj formo za index1."""
    return template("index-igralec.html")
@get("/prestopi/")
def index_get():
    """Serviraj formo za index1."""
    return template("prestopi.html")

@get("/register/")
def index_get():
    """Serviraj formo za registracijo"""
    return template("register.html")

@get("/forget-pass/")
def index_get():
    """Serviraj formo za registracijo"""
    return template("forget-pass.html")

@get("/form/")
def form_get():
    """Serviraj formo za form"""
    return template("form.html")

@post('/login/', method='post')
def do_login():
    """Obdelaj izpolnjeno formo za prijavo"""
    # Uporabnisko ime, ki ga je uporabnik vpisal v formo
    username = request.forms.get('username')
    # Izracunamo MD5 has gesla, ki ga bomo spravili
    password = password_md5(request.forms.get('password'))
    # Preverimo, ali se je uporabnik pravilno prijavil
    c = baza.cursor()
    c.execute("SELECT * FROM uporabnik WHERE username=%s AND hash=%s",
              [username, password])
    tmp = c.fetchone()
    # preverimo, ali je zahtevek mogoce v cakanju
    c2 = baza.cursor()
    c2.execute("SELECT * FROM zahtevek WHERE username=%s AND hash=%s",
              [username, password])
    tmp2 = c2.fetchone()
    print(tmp2)
    if tmp is None:
        if tmp2 is None:
            return template("login.html",
                                   napaka="Nepravilna prijava",
                                   username=username)
        elif tmp2[7] == True:
            return template("login.html",
                            napaka="Nepravilna prijava",
                            username=username)
        else:
            return template("login.html",
                            napaka="Zahtevek registracije je v cakanju.",
                            username=username)
    else:
        response.set_cookie('username', username, path='/', secret=secret)
        if tmp[2] == 'igralec':
            redirect('/index-igralec/')
        elif tmp[2] == 'agent':
            redirect("/index-agent/")
        else:
            redirect("/index2/")


# else:
# Vse je v redu, nastavimo cookie in preusmerimo na glavno stran
#     response.set_cookie('username', username, path='/', secret=secret)
#     redirect("/index/")


run(host='localhost', port=8080, debug = True, reloader = True)
