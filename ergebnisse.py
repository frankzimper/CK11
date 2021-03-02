# Bibliothek um mit dem Server zu kommunizieren

import requests
import json

server = 'http://127.0.0.1:5000'
url = server + '/ergebnis'

def ergebnis_speichern(name, ergebnis):
    headers = {"Content-Type": "application/json"}
    data = {'name': name, 'versuche': ergebnis}
    res = requests.put(url, data = json.dumps(data), headers=headers)
    print (res)
    return res