#!/usr/bin/python3
"""Lists all states starting with an uppercase N from a MySQL database."""

import sys

import MySQLdb

if __name__ == "__main__":
    # Le code ne s'exécute que si on lance le script, pas si on l'importe

    # Connexion au serveur MySQL avec les 3 arguments de la ligne de commande
    # sys.argv[1] = user, sys.argv[2] = mot de passe, sys.argv[3] = base
    db = MySQLdb.connect(host="localhost", port=3306,
                         user=sys.argv[1], passwd=sys.argv[2],
                         db=sys.argv[3])

    # Le curseur sert à envoyer des requêtes SQL et à récupérer les résultats
    cur = db.cursor()

    # LIKE 'N%' = commence par N ; BINARY = respecte la casse (N mais pas n)
    cur.execute("SELECT * FROM states WHERE name LIKE BINARY 'N%' "
                "ORDER BY states.id ASC")

    # fetchall() renvoie toutes les lignes sous forme de tuples (id, name)
    for row in cur.fetchall():
        print(row)

    # Toujours fermer le curseur puis la connexion pour libérer les ressources
    cur.close()
    db.close()
