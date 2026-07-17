# DTLknowsWhy v2.2.0

## Présentation

DTLknowsWhy est un outil Windows de diagnostic et d'analyse experte conçu pour aider les administrateurs, techniciens et équipes support à comprendre non seulement **ce qui** se passe sur un système, mais aussi **pourquoi** cela se produit.

Le projet combine inventaire automatique, analyse de configuration et connaissances expertes pour identifier des causes probables de problèmes Windows courants : réseau, services, partage SMB, résolution de noms, produits de sécurité et configuration système.

DTLknowsWhy évolue d'un collecteur de données vers un véritable assistant de dépannage capable d'expliquer des symptômes observés et de proposer des causes probables.

Version v2.2.0 - 10 juin 2026 - Didier DTL Morandi - www.didiermorandi.com/netdtl

---

## Nouveautés de la version 2.2

La version 2.2 ajoute plusieurs fonctions importantes par rapport à la base 2.1.

### Découverte automatique des cibles par adresse IP

L'interface graphique découvre automatiquement les équipements joignables sur le sous-réseau IPv4 local au démarrage.

Le sélecteur de cible est alimenté par des adresses IP, pas par des noms de machines. Quand un nom peut être résolu, il est affiché à côté de l'adresse :

```text
172.17.7.19 - SCCF-71SFS42
172.17.7.22 - SCCF-2C49F63
172.17.7.23 - SCCF-6V5FS42
```

Si aucun nom n'est connu, seule l'adresse IP est affichée.

Les diagnostics sont lancés contre l'adresse IP elle-même. Cela évite les ambiguïtés NetBIOS, DNS ou de résolution de noms Windows lors de l'analyse de problèmes d'accès.

### Comparaison automatique de type GitScan

DTLknowsWhy peut lancer une comparaison automatique entre la machine locale de référence et une cible sélectionnée, sans que l'utilisateur choisisse manuellement une règle de diagnostic.

Ce mode est destiné aux situations de support rapides où la question est :

> « Qu'est-ce qui diffère entre le PC de référence et la cible ? »

### Analyse comparative distant-vers-distant

La version 2.2 introduit aussi une analyse comparative de second niveau entre deux diagnostics distants.

Elle compare deux points de vue clients vers la même cible, par exemple :

- le PC A peut énumérer ou accéder à un partage ;
- le PC B atteint TCP 445 mais reçoit une erreur d'authentification.

L'analyse produit :

- des explications probables ;
- des causes éliminées ;
- des scores de pertinence pour chaque différence.

Exemple :

```powershell
py -m expert.comparative_analysis PC-A_snapshot.json PC-B_snapshot.json
```

Le premier snapshot doit représenter le point de vue où l'accès fonctionne. Le second doit représenter le point de vue où l'accès échoue.

La commande écrit par défaut :

```text
comparative_analysis_<PC-A>_vs_<PC-B>_<timestamp>.txt
comparative_analysis_<PC-A>_vs_<PC-B>_<timestamp>.html
```

Options utiles :

```powershell
py -m expert.comparative_analysis PC-A_snapshot.json PC-B_snapshot.json --json
py -m expert.comparative_analysis PC-A_snapshot.json PC-B_snapshot.json --output-prefix mon_rapport
py -m expert.comparative_analysis PC-A_snapshot.json PC-B_snapshot.json --no-files
```

Conclusions typiques :

- cible injoignable éliminée ;
- blocage TCP 445 éliminé ;
- partage absent sur la cible éliminé ;
- échec SMB propre au client probable ;
- contexte d'identité différent probable.

### Snapshot d'agent distant

Quand la cible exécute DTLknowsWhy-Agent, l'outil principal peut demander un snapshot distant complet via HTTP sur le port 5050.

Le rapport peut alors comparer :

- le PC local de référence ;
- les tests de connectivité distants légers ;
- le snapshot complet de la cible distante, s'il est disponible.

Si l'agent distant fonctionne localement sur la cible mais n'est pas joignable depuis la machine de référence, DTLknowsWhy peut identifier la règle pare-feu TCP 5050 probablement manquante.

### Collecteur de sécurité des partages SMB

Le collecteur `SMB_SHARE_SECURITY` analyse chaque partage SMB local et compare les deux couches de droits Windows :

- ACL du partage ;
- ACL NTFS.

Pour chaque partage, il enregistre :

- nom du partage ;
- chemin local ;
- droits du partage ;
- droits NTFS ;
- présence de principaux larges comme `Everyone`, `Users` ou `Authenticated Users`.

Le collecteur peut produire l'indicateur :

```text
SMB_ACCESS_MISMATCH
```

Situations détectées :

- partage ouvert mais NTFS restrictif ;
- NTFS ouvert mais partage restrictif ;
- chemin de partage inaccessible ou ACL illisible ;
- incohérence entre droits de partage et droits NTFS.

Cela aide à analyser les cas où un partage est visible depuis un autre poste mais où l'accès est refusé parce que l'onglet Sécurité NTFS reste plus restrictif que les permissions du partage.

### Statut et confiance du moteur expert

Les constats experts peuvent désormais distinguer :

- observations actives ;
- causes résolues ;
- observations historiques ;
- hypothèses.

Chaque constat peut aussi porter un niveau de confiance :

- confirmé ;
- probable ;
- faible.

Cela évite qu'une ancienne observation reste affichée comme un problème actif après correction.

### Ordre des rapports

Lorsqu'une cible distante est analysée, les rapports placent désormais les informations de la cible et les constats de diagnostic en premier.

Les données de la machine locale sont placées en fin de rapport, car elles servent surtout de référence de comparaison.

### Collecte réseau internationalisée

Les versions précédentes analysaient la sortie de :

```text
ipconfig /all
```

Cette méthode dépendait des libellés localisés de Windows et ne fonctionnait de manière fiable que sur les installations françaises.

La version 2.1 introduit un moteur de collecte réseau fondé sur PowerShell et les données CIM structurées.

Avantages :

- fonctionnement indépendant de la langue ;
- compatibilité avec Windows en français, anglais et autres langues ;
- collecte réseau plus fiable ;
- suppression de l'analyse fragile de texte ;
- meilleure compatibilité avec les futures mises à jour Windows.

### Choix de langue dans l'interface graphique

Depuis la version 2.1, l'interface permet de choisir la langue au démarrage.

La langue sélectionnée est utilisée pour :

- les éléments d'interface ;
- les menus et boîtes de dialogue ;
- les rapports générés ;
- les messages de diagnostic ;
- les futures explications du système expert.

Langues actuellement prises en charge :

- français ;
- anglais.

Cette fonction est indépendante de la langue du système d'exploitation.

---

## Compatibilité ascendante

Même si le mécanisme de collecte a été remanié, la structure JSON produite reste compatible.

Les éléments suivants continuent à fonctionner sans modification :

- règles expertes ;
- rapports HTML ;
- rapports PDF ;
- modules d'analyse.

---

## Fonctionnalités principales

### Inventaire système

Collecte d'informations détaillées sur :

- système d'exploitation ;
- matériel ;
- logiciels installés ;
- services ;
- configuration réseau ;
- ressources partagées ;
- produits de sécurité ;
- stockage ;
- événements.

### Diagnostics réseau

Collecte et analyse :

- configuration IPv4 ;
- masques de sous-réseau ;
- passerelles par défaut ;
- serveurs DNS ;
- état DHCP ;
- paramètres NetBIOS ;
- interfaces réseau actives ;
- découverte automatique des cibles IPv4 locales ;
- joignabilité TCP distante sur les ports utiles au diagnostic.

### Détection sécurité

Détection :

- antivirus enregistrés ;
- entrées du Centre de sécurité Windows ;
- inscriptions antivirus potentiellement orphelines ;
- état Windows Defender ;
- pilotes de filtre système via `fltmc`.

### Analyse SMB et partage de fichiers

Aide à identifier les problèmes liés à :

- dossiers partagés ;
- droits de partage ;
- droits NTFS ;
- incohérences partage/NTFS ;
- résolution de noms ;
- accessibilité SMB ;
- découverte réseau ;
- service Function Discovery Resource Publication (FDResPub).

### Moteur de connaissances expertes

DTLknowsWhy corrèle les données collectées avec des cas de dépannage connus et des bonnes pratiques.

Exemples :

- accès SMB lent par nom d'hôte mais rapide par IP ;
- équipements réseau manquants malgré un accès SMB réussi ;
- partage SMB visible mais accès refusé à cause de droits NTFS restrictifs ;
- agent DTLknowsWhy distant injoignable alors que le service tourne ;
- autorisation RDP et représentation d'identité Microsoft Entra ID ;
- problèmes DNS ;
- antivirus orphelins ;
- mauvaise configuration de services Windows.

---

## Architecture

```text
Système Windows
       |
       v
Collecte de données
       |
       v
Inventaire JSON structuré
       |
       v
Moteur d'analyse experte
       |
       v
Diagnostics lisibles
```

L'objectif n'est pas seulement de rapporter des données système, mais de transformer les observations en explications exploitables.

---

## Prérequis

- Windows 10
- Windows 11
- PowerShell 5.1 ou plus récent
- Droits administrateur recommandés pour un diagnostic complet

---

## Cas d'usage typiques

- Dépannage poste de travail
- Diagnostic réseau
- Problèmes d'accès SMB
- Investigations DNS
- Vérification des produits de sécurité
- Audit de configuration Windows
- Préparation d'une escalade support

---

## Build

Regénérer l'application graphique principale :

```powershell
py -m PyInstaller --clean DTLknowsWhy.spec
```

Regénérer l'agent distant :

```powershell
py -m PyInstaller --clean DTLknowsWhy-Agent.spec
```

L'agent doit être reconstruit lorsque les collecteurs, le serveur distant, la logique de service ou les formats de rapport évoluent.

---

## Documentation

Le guide utilisateur et le manuel de référence DTLknowsWhy v2.2 sont disponibles dans la documentation NetDTL :

https://didiermorandi.com/netdtl/doc/

## Version

Version courante : **DTLknowsWhy v2.2.3**

## Mise à jour - 17 juillet 2026

Le code courant indique `DTLKNOWSWHY_VERSION = "v2.2-3"` dans `shared/version.py`.

Composants présents et confirmés :

- Interface graphique Tkinter avec choix de langue, sélection de cible et bouton d'ouverture du dernier rapport HTML.
- Fond général noir et cartouche de titre aux couleurs NetDTL avec le logo NetDTL.
- Découverte automatique des cibles IPv4 locales avec affichage `IP - nom` quand un nom peut être résolu.
- Mode `--snapshot` pour générer un snapshot local.
- Mode `--target` pour lancer des diagnostics contre une machine distante.
- Mode `--gitscan TARGET` pour lancer une comparaison automatique sans choisir manuellement les règles de diagnostic.
- Mode `--listen` pour exposer un petit serveur HTTP de snapshot distant, avec `--once` pour les tests.
- Commandes de service Windows via `--service`, par exemple pour installer l'agent au démarrage.
- Collecteurs séparés pour système, réseau, services, GLPI, tests locaux et tests distants.
- Rapports texte, HTML et JSON avec sérialisation de snapshot.
- Moteur expert enrichi : comparaison causale, règles, traduction et analyse des différences SMB/RDP/DNS/sécurité.
- Documentation locale bilingue : guides utilisateur et manuels de référence en français et en anglais.
