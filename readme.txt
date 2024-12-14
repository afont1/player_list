# Instructions d'installation et d'utilisation

## Installation

1. Autorisez le fichier `.exe` dans Windows Defender, sinon il sera supprimé.

2. Lorsque vous lancez en mode administrateur, il installe les dépendances nécessaires au bon fonctionnement du programme.
   - Si vous lancez sans le mode administrateur, il lance simplement la liste des joueurs.
   - S'il y a un problème, essayez de lancer en mode administrateur, cela pourrait résoudre le problème.

## Utilisation

- Pour fermer le programme, faites un clic droit sur les icônes cachées dans Windows.
- Si vous le fermez via le gestionnaire des tâches, vous perdrez la connexion Internet.
  - Redémarrer le PC ne changera rien.
  - Si cela se produit, ouvrez PowerShell et exécutez la commande suivante :
    ```
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" -Name ProxyEnable -Value 0
    ```

## Bugs connus

- L'adresse IP du serveur ou le nom du serveur est incorrect lorsque vous changez de mer.
- Il peut y avoir de petites pointes de ping (à vérifier).
