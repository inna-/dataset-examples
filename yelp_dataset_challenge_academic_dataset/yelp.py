import json
import sqlite3
import pdb

db = sqlite3.connect('local.db')
cur = db.cursor()

cur.execute('''PRAGMA foreign_keys = ON''')
cur.execute('''CREATE TABLE IF NOT EXISTS category(name TEXT PRIMARY KEY)''')
cur.execute('''CREATE TABLE IF NOT EXISTS business(id TEXT PRIMARY KEY, name TEXT, full_address TEXT, city TEXT, state TEXT, longitude REAL, latitude REAL, stars REAL, open INTEGER, review_count INTEGER, type TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS business_category(business_id TEXT,category_name TEXT, FOREIGN KEY(business_id) REFERENCES business(id) ON UPDATE CASCADE, FOREIGN KEY(category_name) REFERENCES category(name) ON UPDATE CASCADE)''')
cur.execute('''CREATE TABLE IF NOT EXISTS user(id TEXT PRIMARY KEY, name TEXT, review_count INTEGER, average_stars REAL, funny INTEGER, useful INTEGER, cool INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS review(id TEXT PRIMARY KEY, business_id TEXT, user_id TEXT,stars INTEGER, date TEXT, type TEXT, text TEXT, funny INTEGER, useful INTEGER, cool INTEGER, FOREIGN KEY(business_id) REFERENCES business(id) ON UPDATE CASCADE, FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE)''')

def reviews():
    with open('yelp_academic_dataset_review.json') as f:
        for line in f:
            d = json.loads(line)
            data = [d['review_id'], d['business_id'], d['user_id'], d['stars'], d['date'], d['type'], d['text']]
            votes = d['votes']
            data.extend([votes['funny'], votes['useful'], votes['cool']])
            cur.execute('INSERT INTO review values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
            print 'inserted', d['review_id']
    db.commit()

def user():
    with open('yelp_academic_dataset_user.json') as f:
        mult_items = set()
        for line in f:
            d = json.loads(line)
            data = [d['user_id'], d['name'], d['review_count'], d['average_stars']]
            votes = d['votes']
            data.extend([votes['funny'], votes['useful'], votes['cool']])
            cur.execute('INSERT INTO user values (?, ?, ?, ?, ?, ?, ?)', data) 
            print 'inserted', d['user_id']
    db.commit()

def updateCat():
    with open('yelp_academic_dataset_business.json') as f:
        categories_list = set()
        for line in f:
            d = json.loads(line)
            categories = d['categories']
            for category in categories:
                categories_list.add(category)
    categories_list = list(categories_list)
    categories_list.sort()
    print categories_list
    for item in categories_list:
        cur.execute('INSERT INTO category values ("%s")' % item)
        print "Inserted %s" % item
    db.commit()

def updateBiz():
    with open('yelp_academic_dataset_business.json') as f:
        for line in f:
            d = json.loads(line)
            data = [d['business_id'],
                    d['name'],
                    d['full_address'].replace('\n', ' '),
                    d['city'],
                    d['state'],
                    d['longitude'],
                    d['latitude'],
                    d['stars'],
                    int(d['open']),
                    d['review_count'],
                    d['type']]
            cur.execute('INSERT INTO business values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)

    db.commit()

def updateBizCat():
    with open('yelp_academic_dataset_business.json') as f:
        for line in f:
            d = json.loads(line)
            biz_id = d['business_id']
            categories = d['categories']
            for category in categories:
                pair = [biz_id, category]
                cur.execute('INSERT INTO business_category values (?, ?)', pair) 
                print 'inserted', category
    db.commit()

def tips():
    with open('yelp_academic_dataset_tip.json') as f:
        for line in f:
            d = json.loads(line)
            for k, v in d.iteritems():
                print k, v
            break


def checkins():
    with open('yelp_academic_dataset_checkin.json') as f:
        for line in f:
            d = json.loads(line)
            bid = d['business_id']
            checkin = d['checkin_info']
            for k, v in checkin.iteritems():
                k = [int(val) for val in k.split('-')]
                print k[0], k[1], v
            break

# user()
# updateBiz()
# updateCat()
# updateBizCat()
# reviews()
# checkins()

db.close()
