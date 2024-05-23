# ETNA App

## Description
L'ETNA App est une application de bureau développée en Python qui se connecte à l'intranet de l'école ETNA pour récupérer des informations sur les tickets, le planning, les notes, les devoirs, etc. L'application offre une interface conviviale permettant aux utilisateurs d'accéder facilement à ces informations.

## Fonctionnalités
- **Connexion à l'intranet ETNA**: L'application permet aux utilisateurs de se connecter à leur compte ETNA à l'aide de leur identifiant et de leur mot de passe.
- **Affichage des informations utilisateur**: Une fois connecté, l'application affiche les informations de l'utilisateur telles que le nom d'utilisateur, l'e-mail, les groupes auxquels il appartient, la date de connexion, etc.
- **Affichage du planning hebdomadaire**: Les utilisateurs peuvent consulter leur planning hebdomadaire directement depuis l'application.
- **Notifications**: L'application envoie des notifications instantanées aux utilisateurs lorsqu'ils reçoivent de nouveaux tickets ou qu'un nouvel événement est ajouté à leur planning. Cela permet aux utilisateurs d'être informés rapidement des mises à jour importantes.

## API Utilisées
L'ETNA App utilise les API suivantes :
- **Authentification ETNA**: Pour permettre aux utilisateurs de se connecter à leur compte ETNA.
- **API ETNA**: Pour récupérer des informations sur les tickets, le planning, etc. Cette API est utilisée pour afficher les informations de l'utilisateur et le planning hebdomadaire.

## Comment utiliser
1. Clonez ce dépôt sur votre machine locale.
2. Installez les dépendances requises en exécutant `pip install -r requirements.txt`.
3. Lancez l'application en exécutant `python EtnaIo.py`.
4. Connectez-vous avec vos identifiants ETNA.
5. Explorez les différentes fonctionnalités de l'application à l'aide de l'interface utilisateur.

## Captures d'écran
![Capture d'écran 1](https://i.ibb.co/Mczj0hK/Screenshot-2024-05-23-153904.png)
*Affichage des informations utilisateur*

![Capture d'écran 2](https://i.ibb.co/kX1RxS9/Screenshot-2024-05-23-153943.png)
*Affichage du planning hebdomadaire*

## Remarques
- Assurez-vous d'avoir un accès valide à l'intranet ETNA pour utiliser cette application.
- Si vous rencontrez des problèmes ou si vous avez des suggestions d'amélioration, n'hésitez pas à ouvrir une issue dans ce dépôt.
