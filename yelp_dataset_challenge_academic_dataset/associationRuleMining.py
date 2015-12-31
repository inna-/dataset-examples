import sqlite3
from collections import Counter
from apriori import *
import itertools

db = sqlite3.connect('local.db')
cur = db.cursor()

def categoryExp(category):
    ids = cur.execute("Select business_id, count(business_id) from business_category group by business_id having count(business_id) > 2 \
        and category_name = ?",(category,)).fetchall()
    ids = [i[0] for i in ids]
    categories_list = []
    for i in ids:
        categories = cur.execute("SELECT category_name from \
                business_category where business_id = ? and category_name <> ?",(i,category)).fetchall()
        categories = [c[0] for c in categories]
        categories_list.append(categories)
    # chain = itertools.chain(*categories_list)
    # d = Counter(list(chain))
    # for k, v in d.iteritems():
        # print k, v
    L, suppData = apriori(categories_list, minSupport=0.01)
    rules = generateRules(L, suppData, minConf=0.5)
    for rule in rules:
        print rule

categories = ['Restaurants', 'Beauty & Spas', 'Shopping']
for category in categories:
    categoryExp(category)


db.close()
