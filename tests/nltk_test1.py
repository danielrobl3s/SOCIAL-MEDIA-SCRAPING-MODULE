import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
import csv

text = ''

with open('canal10posts - canal10posts.csv.csv', 'r', encoding='utf-8') as f:
    text = f.read()


tokens = word_tokenize(text.lower())
text1 = nltk.Text(tokens)

#print(text1.similar("PANORAMA"))

frdist = FreqDist([word for word in set(text1)])

print(frdist.items())

