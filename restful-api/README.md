# RESTful API

Projet Holberton School sur les **API REST** : comment des programmes échangent des données à travers le Web.

Le projet suit le chemin complet d'une requête HTTP :

- **Côté client (tâches 0 à 2)** : comprendre HTTP, puis consommer une API avec `curl` et avec Python (`requests`).
- **Côté serveur (tâches 3 et 4)** : créer sa propre API, d'abord à la main avec `http.server`, puis avec le framework **Flask**.
- **Sécurité (tâche 5)** : protéger l'API avec l'authentification Basic, les jetons **JWT** et des **rôles**.

---

## Objectifs d'apprentissage

| Objectif | Ce que je dois savoir expliquer | Tâche |
| --- | --- | --- |
| HTTP/HTTPS Basics | Structure d'une requête et d'une réponse, méthodes, codes de statut, différence HTTP / HTTPS | 0 |
| API Consumption with Command Line | Envoyer des requêtes GET et POST avec `curl` et lire la réponse | 1 |
| API Consumption with Python | Récupérer des données avec `requests`, les traiter, les convertir en CSV | 2 |
| API Development with http.server | Créer un serveur HTTP en écrivant chaque partie de la réponse à la main | 3 |
| API Development with Flask | Routes, routes dynamiques, réponses JSON, requêtes POST, codes d'erreur | 4 |
| API Security & Authentication | Authentification vs autorisation, Basic Auth, JWT, rôles, 401 vs 403 | 5 |
| API Standards & Documentation with OpenAPI | Décrire une API dans un fichier standard (routes, méthodes, codes) | Culture générale |

---

## Prérequis AVANT de commencer le projet

### Connaissances

- **Le Web** : ce qu'est un client, un serveur, une URL, un nom de domaine, une adresse IP, un port.
- **Python** : fonctions, boucles, listes, dictionnaires (`.get()`, `.keys()`, `in`), classes et héritage, décorateurs (`@...`), `if __name__ == "__main__":`, `with open(...)`.
- **JSON** : un format texte proche des dicts et listes Python (`true`/`false`/`null` au lieu de `True`/`False`/`None`).
- **Terminal Linux** : ouvrir deux terminaux (un pour le serveur, un pour le client), `curl`, `|`, `grep`, `head`.

### Les mots indispensables

| Mot | Définition |
| --- | --- |
| Client | Le programme qui **demande** (navigateur, `curl`, script Python) |
| Serveur | Le programme qui **écoute** sur un port et **répond** |
| Requête | Message du client : méthode, chemin, en-têtes, corps |
| Réponse | Message du serveur : code de statut, en-têtes, corps |
| API | La liste des demandes qu'un programme accepte, et la forme de ses réponses |
| REST | Style de conception d'API : des URL qui désignent des ressources, les verbes HTTP pour dire quoi en faire, aucune mémoire entre deux requêtes |
| Endpoint | Une URL précise de l'API, par exemple `/users/jane` |
| JSON | Format texte des données échangées |

### Environnement imposé par le sujet

| Élément | Version |
| --- | --- |
| Python | 3.9 |
| Style | pycodestyle |

### Installation

```bash
sudo apt install -y curl
pip install requests flask flask-httpauth flask-jwt-extended pycodestyle

# Vérifier
python3 -c "import requests, flask, flask_httpauth, flask_jwt_extended; print('OK')"
```

---

## PENDANT le projet : méthode de travail

### Tester un serveur : toujours deux terminaux

```bash
# Terminal 1 : le serveur (il "attend", c'est normal)
python3 task_03_http_server.py              # tâche 3, port 8000
flask --app task_04_flask.py run            # tâches 4 et 5, port 5000

# Terminal 2 : le client
curl -i http://localhost:8000/
```

On arrête un serveur avec **Ctrl+C**. Après chaque modification du code, il faut le **relancer**.

### Les options de curl les plus utiles

| Option | Rôle | Exemple |
| --- | --- | --- |
| `-i` | Affiche les en-têtes de la réponse, puis le corps | `curl -i URL` |
| `-v` | Affiche toute la conversation (requête `>` et réponse `<`) | `curl -v URL` |
| `-X` | Choisit la méthode | `-X POST` |
| `-H` | Ajoute un en-tête | `-H 'Content-Type: application/json'` |
| `-d` | Envoie un corps | `-d '{"username": "jane"}'` |
| `-u` | Authentification Basic | `-u user1:password` |
| `-s -o /dev/null -w '%{http_code}\n'` | N'affiche que le code de statut | |

Petite fonction pratique pour voir le corps **et** le code de chaque réponse :

```bash
t() { curl -s -w '  -> %{http_code}\n' "$@"; }
t http://localhost:5000/status
```

### Checklist avant chaque push

```bash
chmod +x <fichier>.py
pycodestyle <fichier>.py          # aucune ligne = OK
# tester chaque route et comparer avec le sujet, au caractère près
git add <fichier>.py
git commit -m "message clair"
git push
```

Couper son serveur local avant de lancer la vérification sur l'intranet.

### Problèmes fréquents

| Message | Cause | Solution |
| --- | --- | --- |
| `Address already in use` | Un ancien serveur occupe le port | Ctrl+C, ou `ss -ltnp \| grep ':5000'` puis `kill <pid>` |
| `ModuleNotFoundError` | Module absent de l'environnement (venv ou système) | `pip install <module>` dans le bon environnement |
| `415` ou `400` sur un POST | En-tête `Content-Type: application/json` oublié | Ajouter `-H 'Content-Type: application/json'` |
| `405 Method Not Allowed` | La route n'accepte pas cette méthode | Ajouter `methods=["POST"]` à la route |

---

## Tâche 0 : Basics of HTTP/HTTPS

- **Fichier** : aucun (tâche théorique).
- **Objectif** : comprendre la structure des échanges HTTP, les méthodes, les codes de statut et la différence HTTP / HTTPS.

### HTTP vs HTTPS

| | HTTP | HTTPS |
| --- | --- | --- |
| Chiffrement | Aucun, données lisibles en route | Chiffré par TLS (anciennement SSL) |
| Port par défaut | 80 | 443 |
| Identité du serveur | Non vérifiée | Prouvée par un certificat |
| Intégrité | Données modifiables en route | Toute modification est détectée |

HTTPS = HTTP + TLS. Le contenu (méthodes, codes, en-têtes) est identique ; seul le transport change.

### Structure d'une requête et d'une réponse : 4 étages

```text
REQUÊTE                                RÉPONSE
POST /users HTTP/1.1     <- 1. ligne   HTTP/1.1 201 Created
Host: api.exemple.com    <- 2. en-têtes Content-Type: application/json
Content-Type: application/json
                         <- 3. ligne vide obligatoire
{"username": "alice"}    <- 4. corps   {"message": "User added"}
```

### Méthodes HTTP

| Méthode | Opération (CRUD) | Usage |
| --- | --- | --- |
| GET | Read | Lire une ressource sans la modifier |
| POST | Create | Créer une ressource (non idempotent : 2 POST = 2 créations) |
| PUT | Update | Remplacer entièrement une ressource |
| PATCH | Update | Modifier une partie d'une ressource |
| DELETE | Delete | Supprimer une ressource |

### Codes de statut

Le premier chiffre indique le responsable : **2xx** succès, **3xx** redirection, **4xx** erreur du client, **5xx** erreur du serveur.

| Code | Sens | Scénario |
| --- | --- | --- |
| 200 | OK | Un GET réussi |
| 201 | Created | Un POST a créé une ressource |
| 301 | Moved Permanently | `http://` redirige vers `https://` |
| 400 | Bad Request | JSON mal formé ou champ manquant |
| 401 | Unauthorized | Identité absente ou fausse |
| 403 | Forbidden | Identité prouvée, mais droit refusé |
| 404 | Not Found | Ressource inexistante |
| 405 | Method Not Allowed | Méthode non acceptée par la route |
| 409 | Conflict | La ressource existe déjà |
| 500 | Internal Server Error | Le code du serveur a planté |

---

## Tâche 1 : Consume data from an API using command line tools (curl)

- **Fichier** : aucun (tâche pratique).
- **Prérequis** : tâche 0.
- **Objectif** : interroger l'API de test JSONPlaceholder avec `curl`.

```bash
curl -s https://jsonplaceholder.typicode.com/posts | head -12     # GET
curl -I https://jsonplaceholder.typicode.com/posts/1              # en-têtes seuls
curl -s -X POST https://jsonplaceholder.typicode.com/posts \
  -H 'Content-Type: application/json' \
  -d '{"title": "foo", "body": "bar", "userId": 1}'               # POST
```

- **Ce que j'apprends** : chaque option de `curl` modifie un étage de la requête (`-X` la méthode, `-H` les en-têtes, `-d` le corps). Au POST, le serveur répond `201` et attribue lui-même l'id (`"id": 101`).
- **Piège** : avec `-d`, oublier `-H 'Content-Type: application/json'`. Règle des guillemets : simples à l'extérieur, doubles à l'intérieur du JSON.

---

## Tâche 2 : Consuming and processing data from an API using Python

- **Fichier** : `task_02_requests.py`
- **Prérequis** : tâche 1, dictionnaires et listes Python, `with open(...)`.
- **Objectif** :
  - `fetch_and_print_posts()` : afficher `Status Code: 200` puis le titre de chaque post ;
  - `fetch_and_save_posts()` : enregistrer `id`, `title` et `body` de chaque post dans `posts.csv`.

### Ce que j'apprends

| Étape | Code |
| --- | --- |
| Envoyer la requête | `response = requests.get(URL)` |
| Lire le code | `response.status_code` |
| Décoder le JSON en liste de dicts | `posts = response.json()` |
| Ne garder que certains champs | `[{"id": p["id"], "title": p["title"], "body": p["body"]} for p in posts]` |
| Écrire le CSV | `csv.DictWriter(f, fieldnames=["id", "title", "body"])`, `writeheader()`, `writerows()` |

- `response.json()` est une **méthode de l'objet réponse** : pas besoin d'`import json`.
- `csv` est un **module standard** de Python : c'est lui qui **crée** `posts.csv`.

### Pièges

- Confondre `response.text` (du texte) et `response.json()` (des objets Python).
- Oublier `newline=""` dans `open()` : lignes vides parasites dans le CSV.
- Compter les lignes du CSV avec `wc -l` : le champ `body` contient des retours à la ligne. Compter avec `csv.DictReader`.

### Test

```bash
python3 main_02_requests.py | head -4
head -1 posts.csv                         # id,title,body
```

---

## Tâche 3 : Develop a simple API using Python with the http.server module

- **Fichier** : `task_03_http_server.py`
- **Prérequis** : tâche 0 (structure d'une réponse), classes et héritage, `json.dumps`.
- **Objectif** : un serveur sur le port **8000** avec ces routes :

| Route | Réponse | Content-Type | Code |
| --- | --- | --- | --- |
| `/` | `Hello, this is a simple API!` | `text/plain` | 200 |
| `/data` | `{"name": "John", "age": 30, "city": "New York"}` | `application/json` | 200 |
| `/status` | `OK` | `text/plain` | 200 |
| `/info` | `{"version": "1.0", "description": "A simple API built with http.server"}` | `application/json` | 200 |
| autre | `Endpoint not found` | `text/plain` | 404 |

### Ce que j'apprends : une méthode par étage de la réponse

| Étage | Méthode de `BaseHTTPRequestHandler` |
| --- | --- |
| 1. Ligne de statut | `self.send_response(200)` |
| 2. En-têtes | `self.send_header("Content-Type", "application/json")` |
| 3. Ligne vide | `self.end_headers()` |
| 4. Corps | `self.wfile.write(texte.encode("utf-8"))` |

- `do_GET` est appelée automatiquement pour chaque requête GET ; `self.path` contient le chemin demandé.
- Le **routage** est une chaîne de `if / elif / else` sur `self.path`.

### Pièges

- `wfile.write()` attend des **octets** : toujours `.encode()`.
- Oublier `end_headers()` : la réponse est mal formée.
- Une requête `HEAD` (`curl -I`) renvoie `501`, car seul `do_GET` existe : utiliser `curl -i` pour voir les en-têtes.

---

## Tâche 4 : Develop a Simple API using Python with Flask

- **Fichier** : `task_04_flask.py`
- **Prérequis** : tâche 3, décorateurs, dictionnaires.
- **Objectif** : une API d'utilisateurs stockés en mémoire dans `users = {}` (dictionnaire **vide** au moment du push).

| Route | Méthode | Réponse | Code |
| --- | --- | --- | --- |
| `/` | GET | `Welcome to the Flask API!` | 200 |
| `/data` | GET | Liste des usernames, par exemple `["jane"]` | 200 |
| `/status` | GET | `OK` | 200 |
| `/users/<username>` | GET | Objet complet de l'utilisateur | 200 |
| `/users/<username>` inconnu | GET | `{"error": "User not found"}` | 404 |
| `/add_user` | POST | `{"message": "User added", "user": {...}}` | 201 |
| `/add_user` JSON invalide | POST | `{"error": "Invalid JSON"}` | 400 |
| `/add_user` sans username | POST | `{"error": "Username is required"}` | 400 |
| `/add_user` username existant | POST | `{"error": "Username already exists"}` | 409 |

### Ce que j'apprends

| http.server (tâche 3) | Flask |
| --- | --- |
| `if self.path == "/status":` | `@app.route("/status")` |
| Découper `self.path` à la main | Route dynamique `/users/<username>` |
| 4 lignes pour envoyer du JSON | `return jsonify(objet)` |
| `send_response(404)` | `return jsonify(objet), 404` |
| `def do_POST` | `methods=["POST"]` + `request.get_json(silent=True)` |

- `request.get_json(silent=True)` renvoie `None` si le JSON est invalide, au lieu de laisser Flask répondre avec son propre message.
- Ordre des vérifications dans `/add_user` : JSON lisible → username présent → username libre → enregistrement.

### Pièges

- Pousser des données de test dans `users` : le sujet l'interdit.
- Oublier `methods=["POST"]` : la route répond `405`.
- Flask trie les clés JSON par ordre alphabétique : c'est normal, l'ordre des clés n'a pas de sens en JSON.

### Test

```bash
flask --app task_04_flask.py run          # terminal 1
t -X POST http://localhost:5000/add_user -H 'Content-Type: application/json' \
  -d '{"username": "jane", "name": "Jane", "age": 28, "city": "Los Angeles"}'
t http://localhost:5000/users/jane        # terminal 2
```

---

## Tâche 5 : API Security and Authentication Techniques

- **Fichier** : `task_05_basic_security.py`
- **Prérequis** : tâche 4, différence entre encodage, chiffrement et hachage.
- **Objectif** : protéger des routes Flask de trois façons.

### Authentification ou autorisation ?

| | Question | Échec |
| --- | --- | --- |
| Authentification | Qui es-tu ? | **401** Unauthorized |
| Autorisation | As-tu le droit ? | **403** Forbidden |

### Les routes

| Route | Protection | Succès | Échec |
| --- | --- | --- | --- |
| `/basic-protected` | Basic Auth (`@auth.login_required`) | `Basic Auth: Access Granted` | 401 |
| `/login` (POST) | Vérifie username + password | `{"access_token": "<JWT>"}` | 401 |
| `/jwt-protected` | Jeton JWT (`@jwt_required()`) | `JWT Auth: Access Granted` | 401 |
| `/admin-only` | JWT + rôle `admin` | `Admin Access: Granted` | 401 sans jeton, 403 `{"error": "Admin access required"}` si non-admin |

### Ce que j'apprends

- **Mots de passe** : on ne stocke que des **empreintes** (`generate_password_hash`) et on vérifie avec `check_password_hash`. Le hachage est irréversible.
- **Basic Auth** : le client envoie `username:password` encodé en base64 **à chaque requête**. Le base64 ne cache rien : acceptable uniquement sur HTTPS.
- **JWT** : le mot de passe voyage **une seule fois** (`/login`), puis le client présente `Authorization: Bearer <jeton>`. Un JWT a 3 parties (`en-tête.contenu.signature`) : il est **signé, pas chiffré**, donc lisible par tous mais infalsifiable sans la clé secrète `JWT_SECRET_KEY`.
- **Rôles** : le jeton contient le username (`identity=username`) ; on relit le rôle dans `users[get_jwt_identity()]["role"]`.
- **Gestionnaires d'erreurs JWT** : toutes les erreurs d'authentification doivent renvoyer **401**.

| Gestionnaire | Cas | Arguments |
| --- | --- | --- |
| `@jwt.unauthorized_loader` | Pas de jeton | 1 |
| `@jwt.invalid_token_loader` | Jeton mal formé ou falsifié | 1 |
| `@jwt.expired_token_loader` | Jeton expiré | 2 (`jwt_header, jwt_payload`) |
| `@jwt.revoked_token_loader` | Jeton révoqué | 2 |
| `@jwt.needs_fresh_token_loader` | Jeton frais exigé | 2 |

### Pièges

- L'exemple du sujet donne un seul argument à tous les gestionnaires : pour les trois derniers, cela provoque une erreur **500** au lieu de 401.
- Mettre un dict dans `identity` : les versions récentes de PyJWT exigent une **chaîne**, sinon même un jeton valide est refusé.
- Confondre 401 et 403.

### Test

```bash
flask --app task_05_basic_security.py run       # terminal 1

# terminal 2
t -u user1:password http://localhost:5000/basic-protected
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H 'Content-Type: application/json' \
  -d '{"username": "user1", "password": "password"}' \
  | python3 -c 'import sys, json; print(json.load(sys.stdin)["access_token"])')
t -H "Authorization: Bearer $TOKEN" http://localhost:5000/jwt-protected
t -H "Authorization: Bearer $TOKEN" http://localhost:5000/admin-only   # 403
```

---

## OpenAPI : documenter une API

OpenAPI (anciennement Swagger) est un format standard, en YAML ou JSON, qui décrit une API : routes, méthodes, paramètres, corps attendus et codes de réponse. C'est le **menu officiel** de l'API, lisible par les humains et par des outils (page de test interactive, génération de code client, tests).

```yaml
openapi: 3.0.3
info:
  title: API des utilisateurs
  version: 1.0.0
paths:
  /users/{username}:
    get:
      summary: Lire un utilisateur
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: L'utilisateur demandé
        "404":
          description: Utilisateur introuvable
```

On peut visualiser une spec en la collant dans l'éditeur en ligne `https://editor.swagger.io`.

---

## Récapitulatif : le même échange vu de partout

| Besoin | curl | Python requests | http.server | Flask |
| --- | --- | --- | --- | --- |
| Méthode | `-X POST` | `requests.post()` | `def do_POST` | `methods=["POST"]` |
| En-tête | `-H 'Nom: valeur'` | `headers={...}` | `send_header()` | automatique avec `jsonify` |
| Corps JSON | `-d '{...}'` | `json=dico` | `rfile.read()` + `json.loads` | `request.get_json()` |
| Code de statut | `-w '%{http_code}'` | `.status_code` | `send_response(code)` | `return ..., code` |

## Les 3 choses à retenir

1. **HTTP est une conversation en texte, en 4 étages** : première ligne, en-têtes, ligne vide, corps. curl, requests, http.server et Flask ne sont que des façons d'écrire ou de lire ces 4 étages.
2. **Le code de statut est un contrat** : 2xx succès, 4xx faute du client, 5xx faute du serveur, et c'est le développeur du serveur qui le choisit.
3. **HTTP n'a pas de mémoire** : la preuve d'identité accompagne chaque requête. 401 quand on ne sait pas qui tu es, 403 quand tu n'as pas le droit.

---

## Ressources

- MDN, aperçu d'HTTP : `https://developer.mozilla.org/fr/docs/Web/HTTP/Overview`
- MDN, codes de statut : `https://developer.mozilla.org/fr/docs/Web/HTTP/Status`
- Requests : `https://requests.readthedocs.io`
- http.server : `https://docs.python.org/3/library/http.server.html`
- Flask : `https://flask.palletsprojects.com`
- Flask-HTTPAuth : `https://flask-httpauth.readthedocs.io`
- Flask-JWT-Extended : `https://flask-jwt-extended.readthedocs.io`
- Décoder un JWT : `https://jwt.io`
- API de test : `https://jsonplaceholder.typicode.com`

---

## Auteur

**Mathieu Bailliez** — Holberton School
GitHub : [Mathieu-Bailliez](https://github.com/Mathieu-Bailliez)
