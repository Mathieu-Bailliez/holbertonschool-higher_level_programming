#!/usr/bin/python3
"""Lists all cities with their state name from the hbtn_0e_4_usa database."""
import sys

import MySQLdb

if __name__ == "__main__":
    # Le code ne s'exécute que si on lance le script, pas si on l'importe

    # Connexion au serveur MySQL avec les 3 arguments
    db = MySQLdb.connect(host="localhost", port=3306,
                         user=sys.argv[1], passwd=sys.argv[2],
                         db=sys.argv[3])
    cur = db.cursor()

    # JOIN relie chaque ville à son état grâce à la clé étrangère state_id
    # On préfixe les colonnes (cities.name / states.name) car les deux
    # tables ont une colonne "name" : sans préfixe, MySQL ne saurait laquelle
    # Un seul execute() comme demandé par le sujet
    cur.execute("SELECT cities.id, cities.name, states.name "
                "FROM cities "
                "JOIN states ON cities.state_id = states.id "
                "ORDER BY cities.id ASC")

    # Chaque ligne est un tuple (id_ville, nom_ville, nom_état)
    for row in cur.fetchall():
        print(row)

    cur.close()
    db.close()
