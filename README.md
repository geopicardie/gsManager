# gsManager

Application python permettant d'interagir avec une instance Geoserver.

## Prérequis et configuration

L'utilisation de gsManager nécessite, pour accéder à l'API REST de Geoserver de disposer d'un environnement Python avec le module [`gsconfig`](https://github.com/boundlessgeo/gsconfig) installé. Pour cela il est recommandé d'utiliser un environnement virtuel.

```
$ python -m virtualenv gsManager
$ source gsManager/bin/activate  <= Sous Linux
$ .\gsManager\Script\activate    <= Sous Windows
$ pip install gsconfig
```
Par ailleurs, veillez à utiliser une version récente de Python (version 2.7.12 testée).
La version 2.7.5 (installation de QGIS par défaut) ne semble pas supporter les connexions HTTPS même en désactivant le contrôle de certificat.

## ATTENTION : version modifiée
La version actuelle est une version modifiée du projet initial pour ajouter une analyse des sections onlineResources dans les fiches pointées par les metadataURL dans Geoserver. L'analyse vérifie s'il y a des services WMS, WFS, WCS ou WMTS déclarés et pour chacun vérifie si le getCapabilities est indiqué et si le layername est bien celui de la source Geoserver.

Elle ne fonctionne qu'en Python 3.6. Plutôt que gsconfig il faut donc installer [`gsconfig-py3`](https://pypi.python.org/pypi/gsconfig-py3) et dans config.json, bien mettre le "/" après "rest" dans gs_url

Il vous faudra aussi installer neogeo_utils pour le parseur XML (avec pip ou pip3)
```
pip install git+https://github.com/neogeo-technologies/neogeo_utils.git
```
Enfin, il faut également ajouter le module requests
```
pip install requests
```
*******************


La configuration de la connexion à Geoserver s'effectue dans config.json (url, login, mot de passe, etc.).

- gs_ws_include le script parcours uniquement les workspace Geoserver précisés
- gs_ws_exclude le script parcours tous les workspace à l'exeption de ceux précisés

Pour obtenir la liste des processus (fonctions) disponibles dans gsManager:
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
- get_styles : télécharger les sld d'un workspace
- post_styles : injecter les sld d'un dossier dans Geoserver en affectant un workspace

## Ajouter de nouveaux processus

Pour ajouter un nouveau processus:
- Créer dans le répertoire "process" le fichier ".py" (module) contenant les processus (fonctions) à ajouter
- Ajouter dans le fichier _processes.py_:
    - L'import du module créé dans _process_: `import process.my_module`
    - Les process (fonctions) nécessaires à la variable `lst`: `'my_process': process.my_module.my_process`
- Testez votre processus

Pour ajouter les variable de configuration à son module, utiliser `import config as cfg`.
A noter que des fonctions générique existent dans le module _helpers.py_, notamment la fonction `helpers.get_datadir()` qui permet de récupérer l'ensemble du Datadir Geoserver sous forme de dictionnaire python (processus assez long sur des grands nombre de layers).
