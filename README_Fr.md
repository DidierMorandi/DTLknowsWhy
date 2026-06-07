# DTLknowsWhy 2.1

## Présentation

DTLknowsWhy est un outil de diagnostic et d'analyse experte pour Windows conçu pour aider les administrateurs, techniciens et ingénieurs support à comprendre non seulement **ce qui** se passe sur un système, mais également **pourquoi** cela se produit.

Le projet combine l'inventaire automatisé du système, l'analyse de configuration et une base de connaissances experte afin d'identifier les causes probables des problèmes Windows courants liés au réseau, aux services, aux partages SMB, à la résolution de noms, aux produits de sécurité et à la configuration système.

DTLknowsWhy a vocation à évoluer d'un simple outil de collecte d'informations vers un véritable assistant de dépannage capable d'expliquer les symptômes observés et de suggérer les causes les plus probables.

Version 2.1.0 - 7 juin 2026
Didier DTL Morandi
[www.didiermorandi.com/netdtl](http://www.didiermorandi.com/netdtl)

---

## Nouveautés de la version 2.1

### Collecte réseau internationalisée

Les versions précédentes reposaient sur l'analyse du résultat de :

```text
ipconfig /all
```

Cette approche dépendait des libellés localisés de Windows et ne fonctionnait donc de manière fiable que sur les installations Windows françaises.

La version 2.1 introduit un tout nouveau moteur de collecte réseau basé sur des données PowerShell et CIM structurées.

Avantages :

* Fonctionnement indépendant de la langue du système
* Compatible avec les éditions Windows françaises, anglaises et autres
* Collecte des informations réseau plus fiable
* Suppression des analyses textuelles fragiles
* Meilleure compatibilité avec les futures évolutions de Windows

Les informations réseau sont désormais obtenues à partir d'objets Windows structurés plutôt qu'à partir de la sortie localisée de commandes système.

### Sélection de la langue dans l'interface graphique

À partir de la version 2.1, l'interface graphique permet à l'utilisateur de choisir sa langue au démarrage.

La langue sélectionnée est utilisée pour :

* Les éléments de l'interface utilisateur
* Les menus et boîtes de dialogue
* Les rapports générés
* Les messages de diagnostic
* Les futures explications du moteur expert

Les langues actuellement prises en charge sont :

* Français
* Anglais

L'infrastructure d'internationalisation a été conçue afin de permettre l'ajout de nouvelles langues avec un minimum de modifications du code.

Cette fonctionnalité est indépendante de la langue du système d'exploitation. Il est ainsi possible d'exécuter DTLknowsWhy en anglais sur un Windows français, ou en français sur un Windows anglais.

Associée au nouveau moteur de collecte réseau indépendant de la langue, cette évolution permet à DTLknowsWhy de fonctionner de manière cohérente dans des environnements Windows multilingues.

---

### Compatibilité ascendante

Bien que le mécanisme de collecte ait été entièrement repensé, la structure JSON générée reste inchangée.

Les éléments suivants continuent donc de fonctionner sans modification :

* Règles expertes
* Rapports HTML
* Rapports PDF
* Modules d'analyse

---

## Fonctionnalités principales

### Inventaire système

Collecte des informations détaillées concernant :

* Le système d'exploitation
* La configuration matérielle
* Les logiciels installés
* Les services
* La configuration réseau
* Les ressources partagées
* Les produits de sécurité
* Les périphériques de stockage
* Les événements système

### Diagnostic réseau

Collecte et analyse :

* Configuration IPv4
* Masques de sous-réseau
* Passerelles par défaut
* Serveurs DNS
* État DHCP
* Paramètres NetBIOS
* Interfaces réseau actives

### Détection des produits de sécurité

Détection :

* Des antivirus enregistrés
* Des entrées du Centre de sécurité Windows
* Des inscriptions antivirus orphelines
* De l'état de Windows Defender

### Analyse SMB et partage de fichiers

Aide à identifier les problèmes liés à :

* Dossiers partagés
* Résolution de noms
* Accessibilité SMB
* Découverte réseau
* Function Discovery Resource Publication (FDResPub)

### Moteur de connaissances expert

DTLknowsWhy est conçu pour mettre en relation les informations collectées avec des cas de dépannage connus et des bonnes pratiques.

Exemples :

* Accès SMB rapide par IP mais lent par nom
* Machine absente du voisinage réseau alors que SMB fonctionne
* Problèmes de configuration DNS
* Inscriptions antivirus orphelines
* Mauvaises configurations de services Windows

---

## Architecture

```text
Système Windows
       |
       v
Collecte des données
       |
       v
Inventaire JSON structuré
       |
       v
Moteur d'analyse expert
       |
       v
Diagnostic compréhensible par l'humain
```

L'objectif n'est pas simplement de présenter des données système, mais de transformer les observations en explications exploitables.

---

## Prérequis

* Windows 10
* Windows 11
* PowerShell 5.1 ou supérieur
* Droits administrateur recommandés pour un diagnostic complet

---

## Cas d'utilisation typiques

* Dépannage de postes de travail
* Diagnostic réseau
* Problèmes d'accès SMB
* Investigations DNS
* Vérification des produits de sécurité
* Audits de configuration Windows
* Préparation d'escalades vers le support

---

## Feuille de route

Améliorations prévues :

* Extension de la base de règles expertes
* Moteur de corrélation avancé
* Prise en charge de langues supplémentaires
* Intégration d'une base de connaissances
* Recommandations de remédiation enrichies
* Capacités de reporting améliorées

---

## Philosophie

La plupart des outils de diagnostic répondent à la question :

> « Quelle est la configuration de cette machine ? »

L'objectif du projet est d'identifier les causes des problèmes plutôt que de simplement constater leurs symptômes.

DTLknowsWhy cherche à répondre à la question :

> « Pourquoi ce problème se produit-il ? »

Cette différence constitue l'objectif fondamental du projet.

---

## Documentation

Les documents DTLknowsWhy Manuel de référence v2.1 et Guide Utilisateur v2.1 sont disponibles dans notre dépôt documentaire NetDTL à l'adresse : https://didiermorandi.com/netdtl/doc/

---

## Version

Version actuelle : **DTLknowsWhy 2.1**

