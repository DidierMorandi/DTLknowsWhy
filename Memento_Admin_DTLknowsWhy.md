# Memento Admin DTLknowsWhy

## Réseau
- ncpa.cpl
- start ms-settings:network
- start ms-settings:network-ethernet
- start ms-settings:network-wifi

## Écran de veille
- control desk.cpl,,@screensaver
- desk.cpl

## IP / DNS
- ipconfig /all
- ipconfig /flushdns
- nslookup NOM_MACHINE
- ping NOM_MACHINE
- ping -4 NOM_MACHINE

## SMB
- net share
- net session
- openfiles /query
- net use
- net use Z: \\SERVEUR\PARTAGE
- net use * /delete /y
- net view \\SERVEUR

## Utilisateurs
- whoami
- whoami /all
- net user
- net localgroup

## Services
- sc query fdrespub
- sc query fdphost
- sc config fdrespub start= delayed-auto

## Credentials
- cmdkey /list
- cmdkey /delete:NOMCIBLE

## ACL
- icacls C:\DOSSIER

## NTLM
- reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LmCompatibilityLevel

## GLPI
http://SERVEUR/glpi/front/inventory.php

## PyInstaller
- pyinstaller --onefile monprogramme.py
- pyinstaller --onefile --noconsole monprogramme.py
- pyinstaller --onefile --noconsole --icon=dtl.ico monprogramme.py

## GitHub
- git status
- git add .
- git commit -m "Description modification"
- git push origin main
- git pull

## Cas DTLknowsWhy
- FDResPub pour voisinage réseau
- DNS si SMB lent par nom mais rapide par IP
- net session pour sessions SMB
- cmdkey /list pour identifiants mémorisés
