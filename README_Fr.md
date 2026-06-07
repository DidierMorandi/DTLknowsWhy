# DTLknowsWhy

## Présentation

DTLknowsWhy est un moteur expert de diagnostic et d'analyse causale pour Windows, conçu pour identifier les causes les plus probables des problèmes de réseau, de partage SMB et de configuration des postes de travail.

Contrairement aux outils de diagnostic traditionnels qui se contentent de collecter des informations, DTLknowsWhy compare les environnements, détecte les différences significatives et propose des causes probables accompagnées d'actions correctives.

Version : 2.0.0 du 6 juin 2026 Didier DTL Morandi (http://www.didiermorandi.com/netdtl)

---

## Fonctionnalités principales

### Diagnostic local

* Inventaire du poste Windows
* Analyse de la configuration réseau
* Diagnostic du client et du serveur SMB
* Analyse DNS et résolution de noms
* Contrôle des services Windows
* Tests de connectivité
* Génération d'un snapshot local

### Diagnostic distant

* Collecte de snapshots distants
* Support de DTLknowsWhy-Agent
* Acquisition distante via HTTP
* Exécution de l'agent en tant que service Windows
* Inventaire d'une machine distante

### Analyse comparative

* Comparaison poste local / poste distant
* Détection des différences de configuration
* Comparaison des paramètres SMB
* Analyse du contexte d'identité et d'authentification
* Comparaison DNS et profils réseau
* Moteur expert basé sur des règles causales

### Rapports

* Rapports TXT lisibles par un technicien
* Rapports HTML enrichis
* Support du français et de l'anglais
* Visualisation distincte des systèmes local et distant
* Présentation des causes probables et actions recommandées

---

## Architecture

### Poste d'analyse

DTLknowsWhy s'exécute sur un poste d'administration et peut :

* collecter un snapshot local ;
* collecter un snapshot distant via DTLknowsWhy-Agent ;
* comparer les deux environnements ;
* générer des rapports de diagnostic.

### Agent distant

DTLknowsWhy-Agent peut fonctionner :

* en mode interactif ;
* en tant que service Windows.

L'agent génère un snapshot local sur la machine cible puis le transmet au poste d'analyse.

---

## Scénario d'utilisation typique

1. Lancer DTLknowsWhy sur un poste de référence.
2. Interroger une machine distante via DTLknowsWhy-Agent.
3. Récupérer le snapshot distant.
4. Comparer les deux environnements.
5. Identifier les causes probables.
6. Générer les rapports HTML et TXT.

---

## Exemple

Poste de référence :

PREDATOR

Poste cible :

PC-BEN-002

Différence détectée :

La signature SMB est obligatoire sur la machine cible mais pas sur la machine de référence.

Cause probable :

Des stratégies de sécurité SMB différentes peuvent affecter l'accès aux partages, l'authentification, les performances ou l'interopérabilité.

Action recommandée :

Vérifier les paramètres de signature SMB et harmoniser les configurations si nécessaire.

---

## Prérequis

* Windows 10 ou Windows 11
* Python 3.10 ou version ultérieure
* Droits administrateur recommandés

---

## Utilisation

### Génération d'un snapshot local

```cmd
python -m agent.agent --snapshot --lang fr
```

### Analyse d'une machine distante

```cmd
python -m agent.agent --target PC-BEN-002 --lang fr
```

### Démarrage de l'agent distant

```cmd
DTLknowsWhy-Agent.exe --listen
```

### Installation de l'agent en tant que service Windows

```cmd
DTLknowsWhy-Agent.exe install
DTLknowsWhy-Agent.exe start
```

## Dépannage de l'agent distant

### Ouverture du port TCP 5050

Par défaut, DTLknowsWhy-Agent écoute sur le port TCP 5050.

Pour permettre à un poste d'administration de récupérer un snapshot distant, ce port doit être autorisé dans le pare-feu Windows de la machine cible.

Lors des tests de validation de la version 2.0.0, l'ouverture du port 5050 a été nécessaire sur PC-BEN-002 afin de permettre la communication avec DTLknowsWhy-Agent.

Exemple de création de la règle depuis une invite de commandes administrateur :

```cmd
netsh advfirewall firewall add rule name="DTLknowsWhy Agent" dir=in action=allow protocol=TCP localport=5050
```

Vous pouvez également créer cette règle depuis :

```text
Pare-feu Windows Defender
→ Paramètres avancés
→ Règles de trafic entrant
→ Nouvelle règle
→ Port TCP 5050
→ Autoriser la connexion
```

### Avertissement de sécurité Windows

Selon la configuration de sécurité du poste, Windows peut afficher un message similaire à :

```text
Windows a protégé votre ordinateur.

Microsoft Defender SmartScreen a empêché le démarrage d'une application non reconnue.
```

ou :

```text
La stratégie de sécurité de votre organisation empêche l'exécution ou l'installation de cette application.
```

Ce comportement est normal lorsque l'exécutable n'est pas signé numériquement ou lorsqu'une politique de sécurité restrictive est appliquée.

Pour poursuivre l'installation :

1. Vérifier que l'exécutable provient bien du dépôt officiel DTLknowsWhy.
2. Cliquer sur « Informations complémentaires » si cette option est proposée.
3. Cliquer sur « Exécuter quand même » ou autoriser explicitement l'installation selon la politique de sécurité en vigueur.

Dans un environnement d'entreprise, il peut être nécessaire de faire approuver ou signer l'exécutable avant son déploiement à grande échelle.

---

## Historique des versions

### Version 2.0.0

* Support des agents distants
* Support des services Windows
* Collecte de snapshots distants
* Comparaison causale locale / distante
* Rapports HTML enrichis
* Amélioration du moteur expert
* Distinction visuelle entre système local et système distant

### Version 1.2.0

* Serveur expérimental de snapshots distants

### Version 1.0.0

* Diagnostic local et génération de rapports

---

## Objectif du projet

DTLknowsWhy cherche à répondre à une question simple :

« Pourquoi cela fonctionne-t-il sur une machine et pas sur une autre ? »

L'objectif du projet est d'identifier les causes des problèmes plutôt que de simplement constater leurs symptômes.

## Documentation

Les documents DTLknowsWhy Manuel de référence v2.1 et Guide Utilisateur v2.1 sont disponibles dans notre dépôt documentaire NetDTL à l'adresse :
https://didiermorandi.com/netdtl/doc/
