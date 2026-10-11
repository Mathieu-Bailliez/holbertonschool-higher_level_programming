#!/usr/bin/python3
"""Lists all cities of a given state, safe from SQL injection."""
import sys

import MySQLdb

if __name__ == "__main__":
    # Le code ne s'exécute que si on lance le script, pas si on l'importe

    # Connexion au serveur MySQL avec les 3 premiers arguments
    db = MySQLdb.connect(host="localhost", port=3306,
                         user=sys.argv[1], passwd=sys.argv[2],
                         db=sys.argv[3])
    cur = db.cursor()

    # JOIN pour relier chaque ville à son état (comme la tâche 4)
    # %s + tuple = requête paramétrée, sans injection possible (tâche 3)
    # On ne sélectionne que cities.name : c'est tout ce qu'on affiche
    cur.execute("SELECT cities.name FROM cities "
                "JOIN states ON cities.state_id = states.id "
                "WHERE BINARY states.name = %s "
                "ORDER BY cities.id ASC", (sys.argv[4],))
    rows = cur.fetchall()

    # Chaque row est un tuple d'un élément ('Dallas',) donc row[0] = 'Dallas'
    # ", ".join() colle les noms avec une virgule et un espace entre eux
    # Si aucune ville : join renvoie "" et print affiche une ligne vide
    print(", ".join(row[0] for row in rows))

    cur.close()
    db.close()
