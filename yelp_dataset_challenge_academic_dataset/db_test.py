import sqlite3

db = sqlite3.connect('test.db')
cur = db.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS category(name TEXT PRIMARY KEY)''')

def insertIt(item):
    cur.execute("INSERT INTO category values ('%s')" % item);

map(insertIt, ['cat', 'dog', 'elephant', 'panda'])

db.commit()
db.close()
