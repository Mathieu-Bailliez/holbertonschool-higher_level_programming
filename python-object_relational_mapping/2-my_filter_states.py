#!/usr/bin/python3
"""Displays all states whose name matches the argument given by the user."""
import sys

import MySQLdb

if __name__ == "__main__":
    # Le code ne s'exécute que si on lance le script, pas si on l'importe

    # Connexion au serveur MySQL avec les 3 premiers arguments
    db = MySQLdb.connect(host="localhost", port=3306,
                         user=sys.argv[1], passwd=sys.argv[2],
                         db=sys.argv[3])
    cur = db.cursor()

    # format() insère sys.argv[4] à la place de {} dans la requête
    # Les '' autour de {} indiquent à MySQL que c'est du texte
    # BINARY = comparaison sensible à la casse (Arizona != arizona)
    # ATTENTION : vulnérable à l'injection SQL (corrigé dans la tâche 3)
    query = ("SELECT * FROM states WHERE BINARY name = '{}' "
             "ORDER BY states.id ASC").format(sys.argv[4])
    cur.execute(query)

    # Affiche chaque ligne trouvée sous forme de tuple (id, name)
    for row in cur.fetchall():
        print(row)

    cur.close()
    db.close()
