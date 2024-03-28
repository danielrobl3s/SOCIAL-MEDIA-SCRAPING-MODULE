import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
import csv

#Get file and read it with pandas
your_file = input('Introduce el nombre del archivo: ')
df = pd.read_csv(your_file)

#Get just the titles to apply nlp
titles = df.iloc[:,0]





