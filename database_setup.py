import sqlite3

# Verbindung zur Datenbank erstellen. Wenn die Datei nicht existiert, wird sie erstellt.
conn = sqlite3.connect('data/library.sqlite')

# Verbindung schließen
conn.close()