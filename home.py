import json
from flask import Flask, request, jsonify, render_template
import sqlite3


app = Flask(__name__)

def getTopTen():
    # Liest die besten 10 Spieler aus der Datenbank
    conn = sqlite3.connect('ergebnisse.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor() 
    sql = """
        select ROW_NUMBER() OVER (ORDER BY versuche) as platz, name, avg(versuche) as versuche from ergebnisse group by name order by versuche LIMIT 10;
    """
    c.execute(sql)
    return c.fetchall()


@app.route('/')
def hello_world():
    topten = getTopTen()
    print(topten)
    return render_template('index.html', topten=topten)

@app.route('/ergebnis', methods=['PUT'])
def ergebnis_speichern():
    # REST Methode die ein Ergebnis in der Datenbank speichert.
    conn = sqlite3.connect('ergebnisse.db')
    c = conn.cursor() 
    record = json.loads(request.data)
    print(record['name'], record['versuche'])
    sql = "insert into ergebnisse values(datetime('now'), '%s', '%s')"
    try:
        c.execute(sql % (record['name'], record['versuche']))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    return record
