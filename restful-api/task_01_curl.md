# Tâche 1 : Consommer une API en ligne de commande avec curl

Ce document raconte ce que j'ai fait pour la tâche 1 du projet RESTful API : interroger une API publique avec `curl`, observer les réponses, et comprendre ce que chaque option change.

L'API utilisée est **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`), une fausse API faite pour s'entraîner : elle répond comme une vraie, mais n'enregistre rien.

---

## L'idée clé

`curl` (Client URL) est un navigateur sans fenêtre : il envoie une requête HTTP et affiche la réponse brute, telle que le serveur l'a écrite. Chaque option modifie un étage de la requête ou de l'affichage.

| Option | Ce qu'elle change |
| --- | --- |
| (aucune) | Envoie un GET et affiche le corps de la réponse |
| `-I` | Envoie un HEAD : seulement les en-têtes de la réponse |
| `-i` | Affiche les en-têtes **puis** le corps |
| `-X POST` | Change la méthode HTTP |
| `-d "..."` | Envoie des données dans le corps (passe automatiquement en POST) |
| `-H "Nom: valeur"` | Ajoute un en-tête à la requête |
| `-v` | Affiche toute la conversation (`>` = requête envoyée, `<` = réponse reçue) |
| `-s` | Mode silencieux : masque la barre de progression |
| `-o /dev/null -w '%{http_code}\n'` | N'affiche que le code de statut |

---

## Étape 1 : installer curl et faire une première requête

```bash
sudo apt update && sudo apt install -y curl jq
curl --version
curl http://example.com
```

**Constaté :**

- `curl --version` affiche la version (`curl 8.x.x`) et la liste des protocoles supportés, dont `http` et `https`.
- `curl http://example.com` renvoie du **HTML brut** (`<!doctype html>`, `<title>Example Domain</title>`). Un navigateur reçoit exactement ce texte ; il le met simplement en forme.

---

## Étape 2 : récupérer des données depuis une API

```bash
curl https://jsonplaceholder.typicode.com/posts
curl -s https://jsonplaceholder.typicode.com/posts | jq '.[0]'
```

**Constaté :**

- La réponse est un **tableau JSON** `[ {...}, {...}, ... ]` de 100 posts.
- Chaque post a 4 champs : `userId`, `id`, `title`, `body`.
- `jq '.[0]'` affiche uniquement le premier post, indenté et coloré.

---

## Étape 3 : afficher uniquement les en-têtes

```bash
curl -I https://jsonplaceholder.typicode.com/posts
```

**Constaté :**

- Première ligne : `HTTP/2 200`, la version du protocole et le code de statut (succès).
- Ensuite, des lignes `nom: valeur`, dont `content-type: application/json; charset=utf-8`.
- **Aucun JSON** : `-I` envoie une requête HEAD, qui demande la réponse sans son corps.

Comparaison avec `-i` (minuscule) :

```bash
curl -i https://jsonplaceholder.typicode.com/posts/1
```

On voit les 4 étages d'une réponse HTTP : ligne de statut, en-têtes, **ligne vide**, corps JSON.

---

## Étape 4 : envoyer une requête POST

```bash
curl -X POST -d "title=foo&body=bar&userId=1" https://jsonplaceholder.typicode.com/posts
```

**Constaté :**

```json
{
  "title": "foo",
  "body": "bar",
  "userId": "1",
  "id": 101
}
```

- Le serveur renvoie les données reçues **plus un `id`** qu'il a attribué lui-même : `101`.
- C'est le comportement standard d'une API REST : c'est le serveur, pas le client, qui choisit l'identifiant d'une nouvelle ressource.

---

## Ce que j'ai découvert : formulaire ou JSON ?

Les données `title=foo&body=bar&userId=1` ne sont **pas du JSON** : c'est le format des **formulaires web**, des paires `clé=valeur` séparées par `&`.

```bash
# Ce que curl annonce quand on utilise -d seul
curl -sv -d "title=foo&body=bar&userId=1" https://jsonplaceholder.typicode.com/posts 2>&1 | grep -i '> content-type'
```

Résultat : `> Content-Type: application/x-www-form-urlencoded`.

Dans un formulaire, **tout est du texte**. C'est pour ça que la réponse contient `"userId": "1"`, entre guillemets.

Le même contenu envoyé en JSON :

```bash
curl -s -X POST https://jsonplaceholder.typicode.com/posts \
  -H 'Content-Type: application/json' \
  -d '{"title": "foo", "body": "bar", "userId": 1}'
```

Résultat : `"userId": 1`, **sans guillemets**, un vrai nombre.

| Format envoyé | En-tête Content-Type | `userId` reçu |
| --- | --- | --- |
| Formulaire (`-d "a=1&b=2"`) | `application/x-www-form-urlencoded` | `"1"` (texte) |
| JSON (`-H ... -d '{...}'`) | `application/json` | `1` (nombre) |

**Leçon** : pour envoyer du JSON à une API, il faut **toujours** préciser `-H 'Content-Type: application/json'`. C'est ce que j'ai fait ensuite pour tester mes API Flask (tâches 4 et 5), où `request.get_json()` ne lit le corps que si cet en-tête est présent.

---

## Exercices supplémentaires réalisés

### Compter et filtrer avec jq

```bash
curl -s https://jsonplaceholder.typicode.com/posts | jq 'length'
curl -s https://jsonplaceholder.typicode.com/posts | jq '.[].title' | head -3
curl -s https://jsonplaceholder.typicode.com/posts | jq '[.[] | select(.userId == 2)] | length'
```

Résultats : `100` posts, les 3 premiers titres, et `10` posts pour l'utilisateur 2. C'est le même traitement que mon script Python de la tâche 2, en une seule ligne de terminal.

### Vérifier que l'API ne fait que simuler

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST -d "title=foo" https://jsonplaceholder.typicode.com/posts
curl -s -w '  -> %{http_code}\n' https://jsonplaceholder.typicode.com/posts/101
```

Résultats : `201` (création annoncée), puis `{}  -> 404`. Le post 101 n'a jamais été enregistré : JSONPlaceholder fait semblant, ce qui permet de s'entraîner sans rien casser.

---

## Pièges rencontrés

- Confondre `-I` (en-têtes seuls) et `-i` (en-têtes puis corps).
- Oublier `-H 'Content-Type: application/json'` quand on envoie du JSON.
- Croire qu'un POST sur JSONPlaceholder enregistre vraiment les données.
- Guillemets : simples à l'extérieur, doubles à l'intérieur du JSON (`-d '{"a": 1}'`).

---

## Ce que je retiens

1. `curl` montre la **réponse brute** : code de statut, en-têtes, corps. C'est l'outil de base pour tester et déboguer une API.
2. Chaque option correspond à une partie de la requête HTTP : `-X` la méthode, `-H` les en-têtes, `-d` le corps.
3. Le format du corps compte : formulaire et JSON ne sont pas la même chose, et c'est l'en-tête `Content-Type` qui les distingue.
4. Réflexe de débogage : quand une API se comporte bizarrement, regarder la requête avec `curl -v` avant de toucher au code.

---

## Auteur

**Mathieu Bailliez** — Holberton School
GitHub : [Mathieu-Bailliez](https://github.com/Mathieu-Bailliez)
