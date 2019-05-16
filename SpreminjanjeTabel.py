#V tej datoteki bomo napisali program za vstavljanje in spreminjanje podatkov
#pri igralcih in prestopih.

def prestop():
    cur.execute("""
        SELECT igralec FROM prestop
