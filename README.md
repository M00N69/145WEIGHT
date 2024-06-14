Ce code est une application Streamlit qui permet d'analyser les données de pesée de packs LOT PROTEAN. L'application offre trois pages principales : "Analyse des poids", "Ressources avec surpoids" et "Rapport d'analyse".

## Analyse des poids

La page "Analyse des poids" permet à l'utilisateur de télécharger un fichier XLSX contenant les données de pesée. L'application affiche ensuite les boxplots des poids des packs par ressource et lot, ainsi qu'un histogramme des poids des packs. L'utilisateur peut sélectionner une période et une ressource spécifiques pour filtrer les données.

## Ressources avec surpoids

La page "Ressources avec surpoids" permet à l'utilisateur de télécharger un fichier XLSX contenant les données de pesée. L'application calcule le surpoids basé sur le poids médian par ressource et affiche un résumé des surpoids par ressource. L'utilisateur peut télécharger le résumé des surpoids en format CSV. L'application affiche également des statistiques descriptives et des graphiques en barres et des histogrammes des surpoids par ressource.

## Rapport d'analyse

La page "Rapport d'analyse" permet à l'utilisateur de télécharger un fichier CSV contenant le résumé des surpoids par ressource. L'application affiche un rapport d'analyse des surpoids par ressource, y compris une analyse statistique descriptive, un graphique en barres des surpoids par ressource, une analyse des distributions statistiques, et une analyse par `LOT PROTEAN` et par jour. L'utilisateur peut sélectionner les ressources à inclure dans l'analyse.

## Guide d'utilisation

1. Lancez l'application Streamlit.
2. Sélectionnez la page souhaitée dans la barre latérale de navigation.
3. Suivez les instructions de la page pour télécharger les fichiers nécessaires et filtrer les données.
4. Interprétez les résultats et utilisez-les pour prendre des décisions éclairées.
