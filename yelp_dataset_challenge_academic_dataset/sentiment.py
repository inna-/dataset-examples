#http://www.nltk.org/howto/sentiment.html

import sqlite3
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

db = sqlite3.connect('local.db')
cur = db.cursor()

cur.execute('''SELECT text from REVIEW LIMIT 10''')
sentences = cur.fetchall()
sentences = [s[0] for s in sentences]
print type(sentences), len(sentences)

sid = SentimentIntensityAnalyzer()
for sentence in sentences:
    print sentence
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        print '{0}: {1}, '.format(k, ss[k])
