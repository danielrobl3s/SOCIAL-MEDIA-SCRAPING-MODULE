import nltk
nltk.download('stopwords')
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
    titles_length = []
    title_tokens = []
    most_common = []
    new_list_title_no_stop_words = []

    for title in titles:
        new_list_title = word_tokenize(title)
        titles_length.append(len(new_list_title))

        for word in new_list_title:

            if word not in stop_words:
                new_list_title_no_stop_words.append(word)


        fd = FreqDist(new_list_title_no_stop_words)
        most_common.append(fd.most_common(3))
        title_tokens.append(new_list_title_no_stop_words)
        
    return title_tokens, titles_length, 'MOST COMMON NEXT ----------------------------->', most_common


#Get file and read it with pandas
your_file = input('Introduce el nombre del archivo: ')
df = pd.read_csv(your_file)

#Get just the titles to apply nlp
titles = df.iloc[:,0]

#Stopwords:
stop_words = stopwords.words('Spanish')
stop_words.append('.')

#Tokenize every title
tokens = turn_tokens(titles)

print(str(len(titles)))
print(tokens)



