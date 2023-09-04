# Mémoire

Le dépôt contient deux dossiers principaux:

- Un dossier "mémoire" contenant le mémoire au format .tex, ainsi que les illustrations et annexes.

- Un dossier "livrables" contenant les fichiers remis à l'AAFS, qui se compose de plusieurs éléments:

     - Un dossier "Archives" avec les éléments suivants:

          - Un dossier "Conversion Excel EAD" comprenant:

              - La dernière version de l'inventaire Excel d'archives.

              - Le code Python utilisé pour transformer l'Excel en XML-EAD.

              - Le fichier d'entrée au format XML-EAD.

              - Le fichier de sortie au format XML-EAD contenant toutes les données d'archives.

          - Un dossier "Conversion EAD-CSV" incluant:

              - Un code Python pour extraire les données du fichier XML-EAD vers le format CSV en vue de leur importation dans la base d'archives.

              - Le fichier CSV résultant de cette extraction.

              - Un dossier contenant six fichiers CSV, chacun correspondant à des archives par tranches de 1000 pour faciliter la mise en base.

          - Un dossier "Conversion EAD-HTML" comprenant:

              - Un CSV intitulé "archives fichier général", résultant de l'extraction des pièces d'archives de la base Omeka S pour récupérer les identifiants.

              - Une copie de l'XML-EAD d'archives initial.

              - Un code Python permettant d'ajouter les identifiants de la base Omeka S dans l'XML-EAD (issus du fichier CSV).

              - L'XML-EAD enrichi de ces identifiants Omeka S.

              - Un fichier XSL applicable à ce dernier fichier XML-EAD pour une édition des données en HTML.

              - Le fichier HTML publiant les données d'archives sous forme de cascade sur une page web.

     - Un dossier "Exports de la base" avec des fichiers CSV d'exports finaux des données entrées dans Omeka S, divisé en deux sous-dossiers.

     - Un dossier "CSV d'import problématiques" contenant des fichiers dont le résultat de l'insertion dépend d'une manipulation de l'École Centrale de Nantes, qui héberge les données d'Omeka S.

     - Trois fichiers "Documentation" sous différents formats expliquant les principes de fonctionnement et de mise à jour de la base Omeka S.
