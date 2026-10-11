#!/usr/bin/python3
"""Displays states matching the user argument, safe from SQL injection."""
import sys

import MySQLdb

if __name__ == "__main__":
    # Le code ne s'exécute que si on lance le script, pas si on l'importe

    # Connexion au serveur MySQL avec les 3 premiers arguments
    db = MySQLdb.connect(host="localhost", port=3306,
                         user=sys.argv[1], passwd=sys.argv[2],
                         db=sys.argv[3])
    cur = db.cursor()

    # Requête paramétrée : %s est un emplacement réservé (sans guillemets)
    # La valeur est passée À CÔTÉ de la requête, dans un tuple
    # MySQLdb l'échappe lui-même, donc aucune injection SQL possible
    # (sys.argv[4],) : la virgule est obligatoire pour créer un tuple
    cur.execute("SELECT * FROM states WHERE BINARY name = %s "
                "ORDER BY states.id ASC", (sys.argv[4],))

    # Affiche chaque ligne trouvée sous forme de tuple (id, name)
    for row in cur.fetchall():
        print(row)

    cur.close()
    db.close()
