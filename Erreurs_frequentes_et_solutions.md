# Erreurs fréquentes et solutions

Document de synthèse construit à partir de `expert/rules_engine.py`.

Chaque entrée reprend l'esprit de la règle sous une forme directement exploitable en diagnostic : constatation, cause probable et remède.

## Réseau local et droits d'exécution

| Règle / cas | Constatation | Cause | Remède |
| --- | --- | --- | --- |
| DNS manuel sur interface DHCP | Les DNS actifs sont configurés manuellement alors que l'interface est en DHCP, et ils diffèrent des DNS fournis par le DHCP. | L'adaptateur utilise une configuration DNS forcée, possiblement héritée d'un ancien réseau ou d'une manipulation manuelle. | Remettre les DNS IPv4 en automatique si le poste doit suivre le DHCP, puis renouveler le bail avec `ipconfig /release` et `ipconfig /renew`. |
| Exécution non administrateur | Certaines vérifications Windows peuvent être incomplètes. | DTLknowsWhy n'a pas les privilèges nécessaires pour lire certains états système, services, ACL ou paramètres réseau. | Relancer DTLknowsWhy en tant qu'administrateur. |
| Passerelle non joignable | La passerelle réseau ne répond pas. | Problème de connexion locale : câble, Wi-Fi, adresse IP, masque, passerelle ou bail DHCP incorrect. | Vérifier le lien réseau, l'adresse IP, le masque, la passerelle, le DHCP et la configuration locale. |
| Profil réseau Public | Le partage Windows ou la découverte réseau peuvent être bloqués. | Windows applique des règles pare-feu plus restrictives en profil Public. | Passer le profil réseau en Privé si le réseau est fiable. |

## Services Windows et SMB local

| Règle / cas | Constatation | Cause | Remède |
| --- | --- | --- | --- |
| LanmanServer arrêté | Le service de partage Windows est arrêté. | La machine locale ne publie plus correctement ses partages SMB. | Démarrer le service avec `sc start LanmanServer`, puis vérifier le pare-feu et les partages. |
| LanmanWorkstation arrêté | Le client SMB est arrêté. | La machine ne peut plus accéder correctement aux partages SMB distants. | Démarrer le service avec `sc start LanmanWorkstation`. |
| FDResPub actif | La machine devrait être visible dans le voisinage réseau, sous réserve du profil réseau et du pare-feu. | Le service de publication de ressources est actif ; si l'affichage échoue encore, le problème est ailleurs. | Vérifier le profil réseau, les règles pare-feu de découverte réseau et l'accès direct par `\\MACHINE`. |
| SMB-001 | La machine peut être invisible dans l'Explorateur réseau alors que l'accès SMB direct fonctionne. | Le voisinage réseau dépend de services de découverte distincts de SMB. SMB peut fonctionner même si l'affichage dans "Réseau" échoue. | Tester `ping <machine>`, `\\machine` et `net view \\machine`. Vérifier `sc query fdrespub`, puis corriger avec `sc config fdrespub start= delayed-auto` et `net start fdrespub`. |
| SMB-001-INFO | FDResPub est actif, mais la machine n'apparaît pas forcément dans l'Explorateur. | Le pare-feu ou la découverte réseau peuvent encore bloquer l'affichage. | Vérifier les règles pare-feu du groupe "Découverte du réseau". |
| SMB-002 | L'accès par `\\192.168.x.x` fonctionne mais `\\NOM_MACHINE` échoue. | SMB fonctionne ; la résolution de nom est défaillante. Causes possibles : NetBIOS désactivé, DNS incomplet, LLMNR défaillant ou FDResPub arrêté. | Tester `ping NOM_MACHINE`, `nbtstat -A IP` et `nslookup NOM_MACHINE`. Corriger la résolution de noms après validation de l'accès par IP. |
| RÈGLE-003 | Le profil réseau est Privé et `fdPHost` est actif, mais FDResPub est arrêté. | La découverte réseau peut avoir été neutralisée ou ses règles pare-feu supprimées. | Lister les règles avec `Get-NetFirewallRule`, puis réactiver le groupe avec `netsh advfirewall firewall set rule group="Découverte du réseau" new enable=Yes`. |

## Droits de partage SMB et ACL NTFS

| Règle / cas | Constatation | Cause | Remède |
| --- | --- | --- | --- |
| RÈGLE-SMB-010 | Le partage SMB est visible, parfois ouvert à "Tout le monde", mais l'accès est refusé. | Sous Windows, les droits effectifs sont l'intersection entre les autorisations du partage et les autorisations NTFS. Si NTFS est plus restrictif, l'accès est refusé. | Vérifier les deux niveaux : autorisations de partage et onglet Sécurité du dossier. Ajouter `Tout le monde` ou `Utilisateurs authentifiés` côté NTFS, avec Modification ou Contrôle total selon le besoin. |
| SMB_ACCESS_MISMATCH | Incohérence détectée entre les droits de partage et les droits NTFS. | Les deux couches de droits ne donnent pas le même niveau d'accès. | Aligner les permissions de partage et NTFS selon l'accès attendu, puis retester depuis le poste distant. |
| CAS-SMB-SCCF-71SFS42-CZC025814B | Cas validé : partage visible et ouvert en lecture/écriture, mais dossier NTFS limité à quelques comptes. | Le partage autorisait l'accès, mais NTFS le refusait. | Correctif validé : ajouter `Tout le monde` dans les autorisations NTFS du dossier partagé. |

## Authentification SMB

| Règle / cas | Constatation | Cause | Remède |
| --- | --- | --- | --- |
| RÈGLE-005-006-014 | TCP 445 est accessible, mais l'authentification SMB échoue avec une erreur 86 ou 1326. | Identifiants cachés, mauvais format de compte, entrée MicrosoftAccount parasite ou niveau NTLM incompatible. | Exécuter `net use * /delete /y`, supprimer les entrées du Gestionnaire d'identification liées à la cible, puis retester avec le bon format : `DOMAINE\utilisateur`, `MACHINE\utilisateur` ou compte Entra selon le contexte. |
| RÈGLE-007-STRICT | `LmCompatibilityLevel` vaut 5 ou plus. | L'authentification est maximalement restrictive : NTLMv2 uniquement, refus LM et NTLM. Certains serveurs anciens ou Workgroups peuvent refuser l'accès avec erreur 1326. | Pour compatibilité Workgroup, régler `LmCompatibilityLevel` à 3, ou à 1 si l'ancien environnement l'exige vraiment. Commande type : `Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name LmCompatibilityLevel -Value 3 -Type DWord`. |
| RÈGLE-007-WEAK | `LmCompatibilityLevel` vaut 0. | LM est activé, ce qui est très permissif et faible côté sécurité. | Régler `LmCompatibilityLevel` à 3 pour imposer NTLMv2 côté client. |
| RÈGLE-007-INFO | `LmCompatibilityLevel` est défini avec une valeur intermédiaire. | Le registre force explicitement un comportement d'authentification NTLM. | Documenter la valeur, vérifier sa cohérence avec les serveurs cibles, et ajuster seulement si un symptôme SMB le justifie. |

## Cible distante et connectivité

| Règle / cas | Constatation | Cause | Remède |
| --- | --- | --- | --- |
| RÈGLE-016 | La cible répond au ping, mais TCP 5050 est inaccessible et le snapshot agent distant n'est pas reçu. | L'agent DTLknowsWhy n'est pas installé, pas démarré, ou bloqué par le pare-feu Windows. | Sur la cible, autoriser TCP 5050 pour `DTLknowsWhy-Agent.exe`. Valider avec `Test-NetConnection <IP> -Port 5050`. |
| Cible Windows sans TCP 445 | La cible semble être un poste Windows, mais le port SMB 445 est inaccessible. | Pare-feu, service LanmanServer arrêté ou partage de fichiers désactivé sur la cible. | Vérifier sur la cible : pare-feu Windows, partage de fichiers et `sc query lanmanserver`. |
| RÈGLE-008-013 | La cible répond au ping mais TCP 445 est inaccessible, équivalent à une erreur 53 par IP. | Blocage transport pur : port 445 fermé, filtré ou service SMB absent. La résolution de noms n'est pas en cause. | Sur la cible, vérifier `sc query lanmanserver`, démarrer avec `sc start lanmanserver` si besoin, puis contrôler les règles pare-feu entrantes TCP 445. |
| RÈGLE-009 | Le ping peut répondre uniquement via une adresse IPv6 link-local `fe80::`. | Un ping IPv6 link-local ne prouve pas que SMB IPv4 est joignable. | Exécuter `ping -4 NOM_MACHINE`, puis `Test-NetConnection IP -Port 445`. |
| RÈGLE-010 | `\\NOM_MACHINE` est lent ou bloqué alors que TCP 445 est accessible. | Windows tente une énumération complète via LLMNR/NetBIOS avant d'afficher les partages, surtout si le nom est mal résolu ou pas encore mappé. | Mapper directement le partage : `net use Z: \\MACHINE\PARTAGE /persistent:yes`. Vérifier aussi le Gestionnaire d'identification. |
| RÈGLE-011 | La cible expose HTTP/HTTPS mais pas SMB, avec possiblement un TTL proche de 62. | Il s'agit probablement d'un équipement réseau, Linux ou appliance, et non d'un PC Windows. | Identifier le constructeur avec `arp -a`, vérifier la MAC et classer la cible comme équipement réseau plutôt que poste Windows. |
| Cible mobile Apple | La cible est identifiée comme appareil mobile Apple probable. | La cible répond sur le réseau, mais ne présente pas le profil d'un poste Windows SMB. | Ne pas chercher un diagnostic SMB Windows classique ; vérifier le type d'appareil et son rôle attendu. |
| Cible mobile Android | La cible est identifiée comme appareil mobile Android probable. | La cible répond sur le réseau, mais ne présente pas le profil d'un poste Windows SMB. | Ne pas chercher un diagnostic SMB Windows classique ; vérifier le type d'appareil et son rôle attendu. |
| Équipement réseau probable | La cible est joignable mais ressemble davantage à un équipement réseau ou une console. | Les services détectés ne correspondent pas à un poste Windows. | Identifier la MAC, les ports ouverts et le constructeur avant de conclure à une panne Windows. |
| Hôte inconnu joignable | La cible répond au ping mais son type n'a pas pu être déterminé. | Informations insuffisantes : peu ou pas de services détectables. | Compléter avec scan de ports, résolution DNS/NetBIOS et vérification MAC. |
| Cible injoignable | La cible distante ne répond pas. | Alimentation, connexion réseau, pare-feu ou adresse cible incorrecte. | Vérifier alimentation, câble/Wi-Fi, adresse IP, VLAN, pare-feu et présence effective de la machine. |

## Bureau à distance RDP

| Règle / cas | Constatation | Cause | Remède |
| --- | --- | --- | --- |
| RÈGLE-RDP-001 | Le compte n'est pas autorisé à ouvrir une session Bureau à distance. | L'utilisateur n'est pas membre du groupe `Utilisateurs du Bureau à distance` ou d'un groupe autorisé. | Vérifier `net localgroup "Utilisateurs du Bureau à distance"`, puis ajouter l'utilisateur avec `net localgroup "Utilisateurs du Bureau à distance" /add NOM_UTILISATEUR`. |
| RÈGLE-RDP-001 résolue | Le groupe `Utilisateurs du Bureau à distance` contient des membres. | L'ancienne cause d'autorisation RDP est éliminée. | Si l'échec continue, poursuivre sur l'identité utilisée, le mot de passe, le mécanisme d'authentification ou le client RDP. |
| RÈGLE-RDP-002 | Le poste est Azure AD / Microsoft Entra ID joined, mais pas membre d'un domaine AD classique. | Les comptes peuvent être représentés sous plusieurs formes selon l'outil. | Vérifier avec `dsregcmd /status`, puis tester les formes de compte adaptées : `SC\utilisateur`, UPN ou format Entra attendu. |
| RÈGLE-RDP-003 | `whoami` et `whoami /upn` ne donnent pas la même représentation du compte. | Windows expose différemment un même utilisateur Entra ID selon le composant interrogé. | Ne pas se limiter à `whoami`. Vérifier aussi `whoami /upn` et les groupes locaux. |
| RÈGLE-RDP-004 | `qwinsta` montre `rdp-tcp` en écoute. | Le service Terminal Server écoute correctement ; le blocage n'est probablement pas l'écoute RDP. | Utiliser ce résultat comme validation, puis poursuivre sur droits, identité ou authentification. |
| RÈGLE-RDP-005 | Il faut distinguer autorisation RDP et authentification. | Les messages d'erreur RDP peuvent indiquer soit un compte non autorisé, soit des identifiants refusés. | Si le message parle d'autorisation, vérifier les groupes locaux. S'il devient "Vos informations d'identification n'ont pas fonctionné", poursuivre sur compte, mot de passe, mécanisme d'authentification et client RDP. |
| RÈGLE-RDP-006 | Le compte doit être validé localement avant d'accuser RDP. | Un mauvais mot de passe, un compte inexistant ou verrouillé peut mimer un problème RDP. | Tester `runas /user:SC\benevole.010 cmd` ou l'équivalent du compte concerné. |
| RÈGLE-RDP-007 | Aucune tentative d'authentification n'apparaît dans les événements Windows après l'échec RDP. | L'échec peut se produire avant l'étape d'ouverture de session Windows. | Consulter l'Observateur d'événements ou `Get-WinEvent -LogName Security`, notamment l'événement 4625. |
| CAS-RDP-SCCF-CZC025814B | Cas validé : poste Entra ID, utilisateur `SC\benevole.010`, groupe RDP vide. | Le compte n'était pas autorisé à ouvrir une session RDP. | Correctif validé : ajouter `SC\benevole.010` au groupe `Utilisateurs du Bureau à distance`, puis retester la connexion. |

## Sécurité système et GLPI

| Règle / cas | Constatation | Cause | Remède |
| --- | --- | --- | --- |
| RÈGLE-012 | BitLocker est actif sur un ou plusieurs lecteurs. | Une modification système, un changement de groupe de travail/domaine ou un démarrage en réparation peut déclencher une demande de clé de récupération. | Avant toute modification, récupérer la clé via `manage-bde -protectors -get C:`, compte Microsoft, Entra ID ou AD. Ne jamais forcer une réinitialisation sans la clé. |
| RÈGLE-015 | GLPI Agent utilise un chemin UNC du type `\\IP\glpi` au lieu d'une URL HTTP. | L'agent GLPI ne peut pas joindre son serveur avec un chemin UNC dans `server = ...`. | Modifier `glpi-agent.cfg` et les fichiers `conf.d` pour utiliser `server = http://IP/glpi/front/inventory.php` ou le chemin GLPI Inventory adapté à la version. |

