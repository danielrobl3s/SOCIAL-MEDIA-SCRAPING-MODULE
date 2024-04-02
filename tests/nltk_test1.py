import nltk
nltk.download('stopwords')
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from gensim.models import Word2Vec
import csv

def tokenize_and_train_word2vec(titles):
    #Stopwords:
    stop_words = stopwords.words('Spanish')
    stop_words.append('.')
    title_tokens = [word_tokenize(title.lower()) for title in titles]

    #titles length:
    titles_length = [len(title) for title in title_tokens]

    title_tokens_no_stopwords = [[word for word in title if word not in stop_words] for title in title_tokens]

    # Train Word2Vec model
    model = Word2Vec(sentences=title_tokens_no_stopwords, vector_size=100, window=5, min_count=1, workers=4)
    
    # Generate dense vectors for each token
    token_vectors = [model.wv[word] for title in title_tokens_no_stopwords for word in title if word in model.wv]

    return token_vectors, titles_length


#Get file and read it with pandas
your_file = input('Introduce el nombre del archivo: ')
df = pd.read_csv(your_file)

#Get just the titles to apply nlp
titles = df.iloc[:,0]

#Tokenize every title and return them as dense vector
tokens = tokenize_and_train_word2vec(titles)

print(tokens)



