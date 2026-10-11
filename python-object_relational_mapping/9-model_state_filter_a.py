#!/usr/bin/python3
"""Lists all State objects containing the letter a using SQLAlchemy."""
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model_state import Base, State

if __name__ == "__main__":
    # Le code ne s'exécute que si on lance le script, pas si on l'importe

    # Connexion à MySQL : dialecte+pilote://user:mot_de_passe@hôte:port/base
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}"
                           .format(sys.argv[1], sys.argv[2], sys.argv[3]),
                           pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # filter() = WHERE en SQL
    # State.name.like('%a%') = WHERE name LIKE '%a%' (contient un "a")
    # order_by(State.id) = ORDER BY states.id ASC
    states = (session.query(State)
              .filter(State.name.like('%a%'))
              .order_by(State.id)
              .all())

    # Chaque élément est un objet State : on lit ses attributs id et name
    for state in states:
        print("{}: {}".format(state.id, state.name))

    session.close()
