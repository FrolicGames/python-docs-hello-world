from tinydb import TinyDB, Query

db = TinyDB('user_logs.json')

data = {'itemSku': 'Contoso Item SKU #1'}

for i in range(0, 100):
    db.insert({'uid': str(i),
    'event_data': data,})   