# ==============================================
# SENTIMENTAL ANALYSIS, NLP AND WORDCLOUD
# ==============================================


# Import Modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist


# Functions
def load_data():
    df = pd.read_excel('Sep_Text.xlsx')
    # df.dropna(inplace=True)
    return df

def sentiments(comment):
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def sentimental_analysis(df):
    df['Sentimental Analysis'] = np.array([sentiments(str(comment)) for comment in df['FreeTextComment']])

    pos = df[df['Sentimental Analysis'] == 'positive']
    neg = df[df['Sentimental Analysis'] == 'negative']

    print('-' * 40, '\n')
    print('Total comments analyzed: {}'.format(len(df)))
    print('Percentage of positive comments: {:.1f}%'.format(len(pos) / len(df) * 100))
    print('Percentage of negative comments: {:.1f}%'.format(len(neg) / len(df) * 100))
    print('-' * 40, '\n')

def clean_data(dff):
    feedbacks = ''
    for feedback in dff['FreeTextComment']:
        feedbacks += feedback
    return feedbacks

def word_cloud(df, sentiment=['positive', 'negative']):
    for i in range(len(sentiment)):
        sWords = set(STOPWORDS)
        sWords.union({'.', ',', '(', ')', 'I', 'was', 'also'})
        dff = df[ df['Sentimental Analysis'] == sentiment[i] ]
        feedbacks = clean_data(dff)
        wordcloud = WordCloud(stopwords=sWords, width=2000, height=1000).generate(feedbacks)

        plt.style.use('ggplot')
        fig = plt.figure(1, figsize=(20,10))
        ax = fig.add_subplot(111)
        ax.imshow(wordcloud)
        ax.axis('off')
        ax.set_title('{} reviews'.format(sentiment[i]))
        plt.show()

def nlp(df, sentiment=['positive', 'negative']):
    for j in range(len(sentiment)):
        dff = df[ df['Sentimental Analysis'] == sentiment[j] ]
        feedbacks = clean_data(dff)
        tokens = [t for t in word_tokenize(feedbacks)]
        sWords = ['.', ',', '(', ')', 'I', 'was', 'also']
        for token in tokens:
            if (token in stopwords.words('english')) or token in sWords:
                tokens.remove(token)
        freq = FreqDist(tokens)
        freq.plot(20, cumulative=False)

        # for key, val in freq.items():
        #     print(key, ':', val)
        # print('-'*40, '\n')


# Run Script
if __name__ == '__main__':
    df = load_data()
    sentimental_analysis(df)
    word_cloud(df)
    nlp(df)