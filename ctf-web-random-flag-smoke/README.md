# Random Web Flag Smoke Test

## Objectif

Ce lab web minimal sert a verifier que les flags random Altair fonctionnent
avec `lab_delivery: web`.

La step 1 a une reponse attendue au format :

```text
ALTAIR{placeholder_web_random_flag}
```

Ce format active la generation d'un flag unique par session. Au lancement du
runtime, `sessions-ms` transmet le flag a `lab-api-service`, puis le conteneur
recoit la variable :

```text
ALTAIR_FLAG_STEP_1
```

L'application web lit cette variable au runtime et la renvoie depuis
`/api/flag`. La page affiche le flag directement au chargement.

## Build local

```bash
docker build -t lab-web-random-flag-smoke:v1 .
```

## Run local

```bash
docker run --rm -p 3000:3000 \
  -e ALTAIR_FLAG_STEP_1='ALTAIR{local_web_random_flag}' \
  lab-web-random-flag-smoke:v1
```

Ouvrir ensuite :

```text
http://localhost:3000
```

## Reponses attendues en local

1. Le flag local est affiche directement :

```text
ALTAIR{local_web_random_flag}
```

Sur la plateforme, la reponse de la step 1 ne sera pas le placeholder du
`metadata.json`. Elle sera le flag random genere pour la session apprenant.

## Condition importante

Ne pas ecrire le flag au build Docker avec `RUN echo ...` ou `COPY flag.txt`.
Pour tester le flag random, le code web doit lire `ALTAIR_FLAG_STEP_1` au
runtime.
