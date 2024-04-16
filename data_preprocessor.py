import nltk
nltk.download('stopwords')
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from gensim.models import Word2Vec
import csv
from sklearn.decomposition import PCA
from sentiment_analysis_spanish import sentiment_analysis

def tokenize_and_train_word2vec(titles):
    #Stopwords:
    stop_words = stopwords.words('Spanish')
    stop_words.append('.')
    title_tokens = [word_tokenize(title.lower()) for title in titles]

    #titles length:
    titles_length = [len(title) for title in title_tokens]

    title_tokens_no_stopwords = [[word for word in title if word not in stop_words] for title in title_tokens]

    #Apply the sentiment analysis:
    analyzer = sentiment_analysis.SentimentAnalysisSpanish()

    sentiments = []

    for title in titles:
        sentiment = analyzer.sentiment(title)
        sentiments.append(sentiment)

    # Train Word2Vec model
    model = Word2Vec(sentences=title_tokens_no_stopwords, vector_size=100, window=5, min_count=1, workers=4)
    
    # Generate dense vectors for each token
    token_vectors = [model.wv[word] for title in title_tokens_no_stopwords for word in title if word in model.wv]

    return token_vectors, titles_length, sentiments


#Get file and read it with pandas
your_file = input('Introduce el nombre del archivo: ')
name = input('Name your resulting dataset: ')
df = pd.read_csv(your_file)
df['Likes'] = pd.to_numeric(df['Likes'], errors='coerce')
df['Comments'] = pd.to_numeric(df['Comments'], errors='coerce')

# Sum up likes and comments for each row
df['Total_Reactions'] = df['Likes'] + df['Comments']

# Extract the 'Total_Reactions' column as a list
total_interactions = [row['Total_Reactions'] for _, row in df.iterrows()]


#Get just the titles to apply nlp
titles = df.iloc[:,0]

#Tokenize every title and return them as dense vector
tokens, titles_length, sentiments = tokenize_and_train_word2vec(titles)

# Apply PCA for dimensionality reduction
pca = PCA(n_components=50)  # Adjust the number of components as needed
reduced_tokens = pca.fit_transform(tokens)

summed_tokens = np.sum(reduced_tokens, axis=0)

print('titles length (each)', titles_length)
print('Sentiments from each title: ', sentiments)
print('Total interactions per post: ', total_interactions)

with open(f'{name}.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Titles_length', 'Sentiments', 'Total_interactions']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()    

    for data in zip(titles_length, sentiments, total_interactions):
        writer.writerow({"Titles_length": data[0], "Sentiments": data[1], "Total_interactions": data[2]})




