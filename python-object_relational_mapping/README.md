# Python - Object-relational mapping

Projet Holberton School qui relie deux mondes : les **bases de données MySQL** et **Python**.

- **Partie 1 (tâches 0 à 5)** : on se connecte à MySQL avec le module `MySQLdb` et on écrit nous-mêmes les requêtes SQL.
- **Partie 2 (tâches 6 à 14)** : on utilise **SQLAlchemy**, un ORM (Object-Relational Mapper). On ne manipule plus du SQL, mais des **objets Python**, et SQLAlchemy écrit le SQL à notre place.

---

## Objectifs d'apprentissage

À la fin du projet, je dois savoir expliquer sans aide :

| Question | Réponse courte |
| --- | --- |
| Comment se connecter à MySQL depuis Python ? | `MySQLdb.connect(host, port, user, passwd, db)` ou, avec un ORM, `create_engine("mysql+mysqldb://user:pass@localhost:3306/db")` |
| Comment faire un SELECT depuis Python ? | Avec MySQLdb : `cursor.execute("SELECT ...")` puis `cursor.fetchall()`. Avec SQLAlchemy : `session.query(Classe).all()` |
| Comment faire un INSERT depuis Python ? | Avec SQLAlchemy : créer un objet, `session.add(objet)`, puis `session.commit()` |
| Que veut dire ORM ? | Object-Relational Mapping : une classe Python représente une table, un objet représente une ligne, un attribut représente une colonne |
| Comment lier une classe Python à une table MySQL ? | La classe hérite de `Base` (créé par `declarative_base()`), définit `__tablename__` et des attributs `Column(...)` |

---

## Prérequis AVANT de commencer le projet

### Connaissances

- **SQL de base** (projets SQL introduction et SQL more queries) : `SELECT`, `WHERE`, `ORDER BY`, `LIKE`, `JOIN`, `INSERT`, `UPDATE`, `DELETE`, clé primaire, clé étrangère, `AUTO_INCREMENT`.
- **Python** : fonctions, boucles, listes, tuples (et leur déballage `a, b = (1, 2)`), classes, héritage, `sys.argv`, `if __name__ == "__main__":`.
- **Terminal Linux** : `cd`, `ls`, `cat`, `chmod +x`, redirections `|`.

### Environnement imposé par le sujet

| Élément | Version utilisée par le correcteur |
| --- | --- |
| Système | Ubuntu 20.04 LTS |
| Python | 3.8.5 |
| MySQL | 8.0 |
| MySQLdb (`mysqlclient`) | 2.0.x |
| SQLAlchemy | 1.4.x |
| pycodestyle | 2.7.x |

### Installation

```bash
# MySQL
sudo apt update
sudo apt install mysql-server
mysql --version

# Outils nécessaires pour compiler MySQLdb
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config zlib1g-dev

# Modules Python
pip3 install mysqlclient "SQLAlchemy<2"

# Vérifier
python3 -c "import MySQLdb, sqlalchemy; print(MySQLdb.version_info, sqlalchemy.__version__)"
```

**Attention aux environnements virtuels (venv)** : les scripts commencent par `#!/usr/bin/python3`, donc lancés avec `./script.py`, ils utilisent **le Python du système**, pas celui d'un venv. Pour ce projet, travailler **hors du venv** (`deactivate`) et installer les modules pour le système.

---

## PENDANT le projet : méthode de travail

### Règles imposées par le sujet

- Première ligne de chaque fichier : exactement `#!/usr/bin/python3`.
- Tous les fichiers sont exécutables (`chmod +x`) et se terminent par un saut de ligne.
- Style vérifié avec `pycodestyle`.
- Documentation obligatoire (une vraie phrase) pour chaque **module**, **classe** et **fonction**.
- Le code ne doit **pas s'exécuter à l'import** : tout le script principal va sous `if __name__ == "__main__":`.
- Interdit d'utiliser `execute` avec SQLAlchemy.
- Connexion à MySQL sur `localhost`, port `3306`.

### Checklist avant chaque push

```bash
chmod +x <fichier>.py
pycodestyle <fichier>.py                                  # aucune ligne = OK
python3 -c 'print(__import__("<fichier>").__doc__)'      # docstring du module
./<fichier>.py <user> <password> <base> [argument]        # comparer avec le sujet
git add <fichier>.py
git commit -m "message clair"
git push
```

### Réinitialiser une base avant de tester

Les scripts qui ajoutent, modifient ou suppriment des lignes changent la base. Pour retrouver l'état attendu par le sujet :

```bash
echo "DROP DATABASE IF EXISTS <nom_base>;" | mysql -uroot -p
cat <fichier>.sql | mysql -uroot -p
```

### Astuce de débogage

Ajouter `echo=True` dans `create_engine(...)` affiche **chaque requête SQL** générée par SQLAlchemy. C'est le meilleur moyen de comprendre ce que fait l'ORM.

### Bases de données utilisées

| Base | Tables | Tâches |
| --- | --- | --- |
| `hbtn_0e_0_usa` | `states` | 0 à 3 |
| `hbtn_0e_4_usa` | `states`, `cities` | 4 et 5 |
| `hbtn_0e_6_usa` | `states` | 6 à 13 |
| `hbtn_0e_14_usa` | `states`, `cities` | 14 |

---

## Partie 1 : MySQLdb (on écrit le SQL)

Schéma commun à toutes les tâches de cette partie :

```python
db = MySQLdb.connect(host="localhost", port=3306, user=user,
                     passwd=password, db=database)
cur = db.cursor()                 # le curseur envoie les requêtes
cur.execute("SELECT ...")         # on écrit le SQL nous-mêmes
for row in cur.fetchall():        # chaque ligne est un tuple
    print(row)
cur.close()
db.close()
```

### Tâche 0 : Get all states — `0-select_states.py`

- **Objectif** : afficher tous les États de `hbtn_0e_0_usa`, triés par `states.id` croissant.
- **Prérequis** : `SELECT ... ORDER BY`, `sys.argv`, la connexion MySQLdb.
- **Ce que j'apprends** : le cycle complet connexion → curseur → `execute` → `fetchall` → fermeture.
- **Résultat** : une ligne par État, sous forme de tuple, par exemple `(1, 'California')`.
- **Piège** : oublier de fermer le curseur et la connexion.

### Tâche 1 : Filter states — `1-filter_states.py`

- **Objectif** : afficher les États dont le nom **commence par un N majuscule**.
- **Prérequis** : `LIKE 'N%'`.
- **Ce que j'apprends** : MySQL compare le texte **sans tenir compte de la casse** par défaut. Pour exiger un `N` majuscule, on utilise `LIKE BINARY 'N%'`.
- **Résultat** : `(4, 'New York')`, `(5, 'Nevada')`.

### Tâche 2 : Filter states by user input — `2-my_filter_states.py`

- **Objectif** : afficher l'État dont le nom est passé en argument, en construisant la requête avec `format()`.
- **Ce que j'apprends** : insérer une entrée utilisateur directement dans le texte SQL fonctionne, **mais c'est dangereux**. Cette tâche prépare la suivante.

### Tâche 3 : SQL Injection... — `3-my_safe_filter_states.py`

- **Objectif** : même chose que la tâche 2, mais **protégé contre l'injection SQL**.
- **Prérequis** : comprendre la faille de la tâche 2 (un argument comme `Arizona' OR '1'='1` modifie la requête).
- **Ce que j'apprends** : les **requêtes paramétrées**. La valeur est passée séparément, jamais collée dans le SQL :

```python
cur.execute("SELECT * FROM states WHERE name = %s ORDER BY id", (name,))
```

- **Piège** : la virgule dans `(name,)` est obligatoire, c'est elle qui crée un tuple.

### Tâche 4 : Cities by states — `4-cities_by_state.py`

- **Objectif** : afficher toutes les villes avec le nom de leur État, triées par `cities.id`, en **un seul** `execute`.
- **Prérequis** : `JOIN ... ON`, clé étrangère.
- **Ce que j'apprends** : la **jointure** recolle chaque ville à son État en faisant correspondre `cities.state_id` et `states.id`.
- **Résultat** : `(1, 'San Francisco', 'California')`.

### Tâche 5 : All cities by state — `5-filter_cities.py`

- **Objectif** : afficher les villes d'un État passé en argument, sur une seule ligne, séparées par des virgules.
- **Prérequis** : jointure (tâche 4) et requête paramétrée (tâche 3).
- **Ce que j'apprends** : combiner jointure et protection contre l'injection, puis mettre en forme avec `", ".join(...)`.
- **Résultat** : `San Francisco, San Jose, Los Angeles, Fremont, Livermore`.

---

## Partie 2 : SQLAlchemy (l'ORM écrit le SQL)

Schéma commun à toutes les tâches de cette partie :

```python
engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}".format(
    user, password, database), pool_pre_ping=True)
Session = sessionmaker(bind=engine)   # fabrique de sessions
session = Session()                   # l'espace de travail
# ... requêtes sur des objets ...
session.close()
```

- Le **moteur** (`engine`) sait comment joindre MySQL.
- La **session** est un « panier » : elle garde les objets chargés, ajoutés, modifiés ou supprimés, et `commit()` envoie tout à la base.

### Tâche 6 : First state model — `model_state.py` + `6-model_state.py`

- **Objectif** : définir la classe `State` liée à la table `states`, puis créer la table.
- **Prérequis** : classes et héritage en Python, notion de table et de colonne.
- **Ce que j'apprends** : le cœur d'un ORM. `Base = declarative_base()` crée le registre des tables ; une classe qui en hérite devient une table.

```python
class State(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)
    name = Column(String(128), nullable=False)
```

- `Base.metadata.create_all(engine)` crée en base toutes les tables connues du registre.

### Tâche 7 : All states via SQLAlchemy — `7-model_state_fetch_all.py`

- **Objectif** : afficher tous les objets `State`, triés par id, au format `1: California`.
- **Ce que j'apprends** : `session.query(State).order_by(State.id).all()` renvoie une **liste d'objets** ; on lit leurs attributs `state.id` et `state.name`.

### Tâche 8 : First state — `8-model_state_fetch_first.py`

- **Objectif** : afficher le premier État (plus petit id), ou `Nothing` si la table est vide.
- **Ce que j'apprends** : `.first()` renvoie un seul objet ou `None`. Il faut tester `None` avant de lire un attribut.

### Tâche 9 : Contains `a` — `9-model_state_filter_a.py`

- **Objectif** : afficher les États dont le nom contient la lettre `a`.
- **Ce que j'apprends** : le filtrage avec `filter(State.name.like("%a%"))`. Le `%` signifie « n'importe quelle suite de caractères ».

### Tâche 10 : Get a state — `10-model_state_my_get.py`

- **Objectif** : afficher l'id de l'État dont le nom est passé en argument, ou `Not found`.
- **Prérequis** : tâche 3 (injection SQL), tâche 8 (`first` et `None`), tâche 9 (`filter`).
- **Ce que j'apprends** : `filter(State.name == nom)` est **automatiquement protégé** contre l'injection : SQLAlchemy génère `WHERE states.name = %s` et envoie la valeur à part.
- **Résultat** : `Texas` → `3` ; `Illinois` → `Not found`.

### Tâche 11 : Add a new state — `11-model_state_insert.py` (CREATE)

- **Objectif** : ajouter l'État `Louisiana` et afficher son nouvel id.
- **Ce que j'apprends** : créer une ligne = créer un objet, `session.add(objet)`, puis `session.commit()`. L'id est choisi par MySQL (`AUTO_INCREMENT`) et rangé dans l'objet **après** le `commit`.
- **Piège** : sans `commit`, rien n'est enregistré. Le script n'est pas idempotent : chaque lancement ajoute une nouvelle Louisiana.

### Tâche 12 : Update a state — `12-model_state_update_id_2.py` (UPDATE)

- **Objectif** : renommer en `New Mexico` l'État dont l'id vaut 2.
- **Ce que j'apprends** : modifier une ligne = récupérer l'objet, changer son attribut (`state.name = "New Mexico"`), puis `commit`. La session **remarque seule** la modification (`session.dirty`) et génère l'`UPDATE`.
- **Résultat** : le script n'affiche rien ; la liste de la tâche 7 montre `2: New Mexico`.

### Tâche 13 : Delete states — `13-model_state_delete_a.py` (DELETE)

- **Objectif** : supprimer tous les États dont le nom contient un `a`.
- **Ce que j'apprends** : récupérer les objets (filtre de la tâche 9), appeler `session.delete(objet)` sur chacun, puis `commit`. Rien n'est supprimé avant le `commit`.
- **Résultat** (après les tâches 11 et 12) : il reste `2: New Mexico` et `4: New York`.

### Tâche 14 : Cities in state — `model_city.py` + `14-model_city_fetch_by_state.py`

- **Objectif** : définir la classe `City` (table `cities`) avec une clé étrangère vers `states.id`, puis afficher chaque ville avec le nom de son État.
- **Prérequis** : tâche 4 (jointure SQL), tâche 6 (définir une classe ORM).
- **Ce que j'apprends** :
  - déclarer une clé étrangère : `state_id = Column(Integer, ForeignKey("states.id"), nullable=False)` ;
  - `City` doit hériter du **même `Base`** que `State` (importé depuis `model_state`), sinon la clé étrangère ne trouve pas la table `states` ;
  - faire une jointure sans SQL : `session.query(State, City).filter(State.id == City.state_id).order_by(City.id)` ;
  - chaque résultat est un **tuple** `(state, city)`, qu'on déballe dans la boucle.
- **Résultat** : `California: (1) San Francisco` ... `Nevada: (15) Carson City`.
- **Piège** : sans le `filter`, on obtient un **produit cartésien** (5 États × 15 villes = 75 lignes absurdes).

---

## Récapitulatif : le CRUD avec SQLAlchemy

| Opération | Code Python | SQL généré | Tâche |
| --- | --- | --- | --- |
| Create | `session.add(State(name="Louisiana"))` puis `commit()` | `INSERT INTO states ...` | 11 |
| Read | `session.query(State).filter(...).all()` | `SELECT ... WHERE ...` | 7 à 10, 14 |
| Update | `state.name = "New Mexico"` puis `commit()` | `UPDATE states SET name=...` | 12 |
| Delete | `session.delete(state)` puis `commit()` | `DELETE FROM states WHERE id=...` | 13 |

## MySQLdb ou SQLAlchemy ?

| | MySQLdb | SQLAlchemy (ORM) |
| --- | --- | --- |
| On écrit | Du SQL dans des chaînes | Du Python sur des objets |
| Résultats | Des tuples | Des objets avec attributs |
| Injection SQL | À éviter soi-même (`%s` + tuple) | Évitée automatiquement par `filter` |
| Changer de base (MySQL vers PostgreSQL) | Réécrire le SQL | Changer seulement l'URL du moteur |
| Contrôle fin du SQL | Total | Moindre, mais visible avec `echo=True` |

## Pièges fréquents du projet

1. Lancer un script depuis un **venv** qui n'a pas `MySQLdb` : le shebang utilise le Python du système.
2. Oublier `session.commit()` après un ajout, une modification ou une suppression.
3. Construire une requête avec `format()` sur une entrée utilisateur : faille d'injection SQL.
4. Tester sur une base modifiée par un test précédent : toujours réinitialiser avec le fichier `.sql`.
5. Oublier `if __name__ == "__main__":` : le code s'exécute à l'import et le correcteur échoue.
6. Créer un nouveau `Base` dans `model_city.py` au lieu de l'importer depuis `model_state`.

---

## Auteur

**Mathieu Bailliez** — Holberton School
GitHub : [Mathieu-Bailliez](https://github.com/Mathieu-Bailliez)
