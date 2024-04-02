import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
import csv

#Function to tokenize titles
def turn_tokens(titles):
    title_tokens = []
    most_common = []
    for title in titles:
        new_list_title = word_tokenize(title)
        fd = FreqDist(new_list_title)
        most_common.append(fd.most_common(3))
        title_tokens.append(new_list_title)
        
    return title_tokens, 'MOST COMMON NEXT ----------------------------->', most_common


#Get file and read it with pandas
your_file = input('Introduce el nombre del archivo: ')
df = pd.read_csv(your_file)

#Get just the titles to apply nlp
titles = df.iloc[:,0]

#Tokenize every title
tokens = turn_tokens(titles)

print(str(len(titles)))
print(tokens)
