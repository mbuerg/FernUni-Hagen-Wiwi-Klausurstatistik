# FernUni-Hagen-Wiwi-Klausurstatistik
Webscraper, der Notenverteilungen von Wiwi Modulen der FernUni Hagen zusammenfasst

Unter https://www.fernuni-hagen.de/wirtschaftswissenschaft/studium/klausurstatistik.shtml findet man die Notenverteilungen der Wiwi Module.
Um zu sehen wie die Verteilungen sind, muss man Semesterbuttons drücken und den Modulnamen bzw Modulnummer suchen. Interessiert man sich beispielsweise für die
Entwicklung der Durchschnittsnote in einem Modul muss man umständlich viele Buttons aufklappen, mit Strg+F die Modulnummer suchen und sich die Noten 
notieren.

Dieses Projekt soll diese Verteilungen in einem Dataframe zusammenfassen (Paneldaten) und im nächsten Schritt visualisieren.

In klausurstatistik.py werden die Daten gezogen und aufbereitet.
In visualisierung.py werden die Daten noch auf die Visualisierung vorbereitet. Dann wird per Dash ein Dashboard erstellt.

![visualisierung](https://user-images.githubusercontent.com/106337257/202548421-df181949-129d-4ff1-aeca-3e9781c32ad2.PNG)


To Do:
1. Durchschnittswerte berechnen und visualisieren
2. Histogramme erstellen
3. Code effizienter machen
