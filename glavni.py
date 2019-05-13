from bottle import *
import auth as auth
import psycopg2, psycopg2.extensions, psycopg2.extras
import hashlib
import webbrowser

#priklop na bazo
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) #da imamo lahko sumnike
baza = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
baza.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogocimo transakcije
cur = baza.cursor(cursor_factory=psycopg2.extras.DictCursor)

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

def pooblastilo(user):
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

print(password_md5("mat555"))

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
