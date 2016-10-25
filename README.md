# gsManager

Application python permettant d'interagir avec une instance Geoserver.

## Prérequis
Python 2.7.12
Installer le module gsconfig
```
$ pip install gsconfig
```

## Configuration

La configuration s'effectue dans config.json.
- gs_ws_include le script parcours uniquement les workspace Geoserver précisés
- gs_ws_exclude le script parcours tous les workspace à l'exeption de ceux précisés

Pour obtenir la liste des processus (fonctions) disponibles:
```
$ python gsManager.py help
```

## Utilisation

Pour lancer un processus, utiliser:
```
$ python gsManager.py processName
```
Par exemple: (génère un fichier CSV des layers)
```
$ python gsManager.py get_csv
```

Il est également possible de combiner plusieurs processus:
```
$ python gsManager.py processName1 processName2
```
Par exemple: (génère un fichier CSV des layers, vérifie et ajoute les liens de métadonnées manaquants, génère un nouveau fichier CSV des layers après modification)
```
$ python gsManager.py get_csv check_mdlinks get_csv
```

## Liste des processus existants

- get_csv : récupérer l'ensemble des layers et de leurs informations sous forme de fichier CSV
- check_mdlinks : vérifier les liens vers les métadonnées et compléter la liste à partir des liens déjà renseignés

## Ajouter de nouveaux processus

Pour ajouter un nouveau processus:
- Créer dans le répertoire "process" le fichier ".py" (module) contenant les processus (fonctions) à ajouter
- Ajouter dans le fichier _processes.py_:
    - L'import du module créé dans _process_: `import process.my_module`
    - Les process (fonctions) nécessaires à la variable `lst`: `'my_process': process.my_module.my_process`
- Testez votre processus

Pour ajouter les variable de configuration à son module, utiliser `import config as cfg`.
A noter que des fonctions générique existent dans le module _helpers.py_, notamment la fonction `helpers.get_datadir()` qui permet de récupérer l'ensemble du Datadir Geoserver sous forme de dictionnaire python (processus assez long sur des grands nombre de layers).
