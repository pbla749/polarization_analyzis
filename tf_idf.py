# -*- coding: utf-8 -*-
"""TF_IDF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11W7Id3jtnXIrYX5q9uLP6-DPi8B0XpRA

Libs import
"""

from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
import spacy
import pandas as pd

STOPWORDS = set(stopwords.words('german'))
print(STOPWORDS)
import numpy as np
#!pip install gensim
#!pip install --upgrade gensim

"""Parties' programmes data"""

# Read data into papers
df_programmes = pd.read_csv('./content/results.csv',sep=';',encoding='utf-8')
# Print head
df_programmes

"""A small pre-processing : sub punctuation and digits + lower()"""

# Remove punctuation
df_programmes['programmes_processed'] = df_programmes['programmes'].map(lambda x: re.sub('[,\|/_.!?]', '', x))
df_programmes['programmes_processed'] = df_programmes['programmes_processed'].map(lambda x: re.sub('[0-9]', '', x))

# Convert the titles to lowercase
df_programmes['programmes_processed'] = df_programmes['programmes_processed'].map(lambda x: x.lower())

# Print out the first rows of papers
df_programmes['programmes_processed']

df_programmes.to_csv('./content/programmes_processed.csv', sep=';', encoding='utf-8')

"""Removing Stopwords, short words + stemming"""

# Initialize the pipeline
#!pip install unidecode

import unicodedata
import unidecode
import spacy.cli
spacy.cli.download("de_core_news_sm")
nlp = spacy.load("de_core_news_sm")

def cleaning_pipeline(text):

    """
    clean the data before processing
    """

    # remove stopwords from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) 

    # removes any words composed of less than 3 
    text = ' '.join(word for word in text.split() if (len(word) >= 3))

    # removes accents
    text = ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))

    text = text.lower()
    text = re.sub(r"[_/(){}\[\]\|@,;]", " ", text)
    text = re.sub(r"[^0-9a-z #+_]", "", text)
    text= re.sub(r"[0-9]+"," ", text)
    text = re.sub(r"[\d+]", "", text)

    #Lemm
    text = ' '.join(word.lemma_.lower() for word in nlp(text))

    # Stemming the words
    text = ' '.join(stemmer.stem(word) for word in text.split())
    
    return text

"""Lemmatizing words"""

programme_0 = []
programme_1 = []
programme_2 = []
programme_3 = []
programme_4 = []
programme_5 = []
programme_6 = []

for i in range(len(df_programmes['programmes_processed'])):
  doc = nlp(cleaning_pipeline(df_programmes['programmes_processed'][i]))
  print(doc)
  for token in doc:
      eval('programme_'+str(i)).append(token.lemma_.lower())

print(programme_0)
print(programme_1)
print(programme_2)
print(programme_3)
print(programme_4)
print(programme_5)
print(programme_6)

"""TF exploratory"""

wordDict0 = dict.fromkeys(programme_0 + programme_1 +programme_2 + programme_3 + programme_4 + programme_5+programme_6 , 0) 
wordDict1 = dict.fromkeys(programme_0 + programme_1 +programme_2 + programme_3 + programme_4 + programme_5+programme_6 , 0) 
wordDict2 = dict.fromkeys(programme_0 + programme_1 +programme_2 + programme_3 + programme_4 + programme_5+programme_6 , 0) 
wordDict3 = dict.fromkeys(programme_0 + programme_1 +programme_2 + programme_3 + programme_4 + programme_5+programme_6 , 0) 
wordDict4 = dict.fromkeys(programme_0 + programme_1 +programme_2 + programme_3 + programme_4 + programme_5+programme_6 , 0) 
wordDict5 = dict.fromkeys(programme_0 + programme_1 +programme_2 + programme_3 + programme_4 + programme_5+programme_6 , 0) 
wordDict6 = dict.fromkeys(programme_0 + programme_1 +programme_2 + programme_3 + programme_4 + programme_5+programme_6 , 0) 

for word in programme_0:
    wordDict0[word]+=1
    
for word in programme_1:
    wordDict1[word]+=1

for word in programme_2:
    wordDict2[word]+=1
    
for word in programme_3:
    wordDict3[word]+=1

for word in programme_4:
    wordDict4[word]+=1
    
for word in programme_5:
    wordDict5[word]+=1

for word in programme_6:
    wordDict6[word]+=1

tf_table = pd.DataFrame([wordDict0, wordDict1,wordDict2,wordDict3,wordDict4,wordDict5,wordDict6])

tf_table.replace(np.nan, 0,  inplace=True)
print(tf_table.head())
print(tf_table.loc[:0])

"""TF Function"""

def computeTF(wordDict, doc):
    tfDict = {}
    corpusCount = len(doc)
    for word, count in wordDict.items():
        tfDict[word] = count/float(corpusCount)
    return(tfDict)

#running our sentences through the tf function:
tf0 = computeTF(wordDict0, programme_0)
tf1 = computeTF(wordDict1, programme_1)
tf2 = computeTF(wordDict2, programme_2)
tf3 = computeTF(wordDict3, programme_3)
tf4 = computeTF(wordDict4, programme_4)
tf5 = computeTF(wordDict5, programme_5)
tf6 = computeTF(wordDict6, programme_6)

#Converting to dataframe for visualization
tf = pd.DataFrame([tf0, tf1, tf2,tf3,tf4,tf5,tf6])
tf.replace(np.nan, 0,  inplace=True)
print(tf.head())

"""TF to_csv"""

tf.to_csv('/content/term_frequency_programmes.csv', sep=';')

"""IDF function"""

import math 
def computeIDF(docList):
    idfDict = {}
    N = len(docList)
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for word, val in idfDict.items():
      idfDict[word] = math.log10(N / (float(val) + 1))
    return(idfDict)

#inputing our sentences in the log file
idfs = computeIDF([wordDict0, wordDict1,wordDict2,wordDict3,wordDict4,wordDict5,wordDict6])

"""TFIDF function"""

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
      tfidf[word] = val*idfs[word]
    return(tfidf)

#running our two sentences through the IDF:
idf0 = computeTFIDF(tf0, idfs)
idf1 = computeTFIDF(tf1, idfs)
idf2 = computeTFIDF(tf2, idfs)
idf3 = computeTFIDF(tf3, idfs)
idf4 = computeTFIDF(tf4, idfs)
idf5 = computeTFIDF(tf5, idfs)
idf6 = computeTFIDF(tf6, idfs)

#putting it in a dataframe
idf= pd.DataFrame([idf0, idf1,idf2,idf3,idf4,idf5,idf6])
idf.to_csv('/content/idf_table.csv', sep=';',encoding='utf-8')

"""Get 50 hot topics per word doc"""

idf = idf[idf.columns.drop(list(idf.filter(regex='--')))]

print(idf)

top_n = 50
tfidf_top_topics = pd.DataFrame({n: idf.T[col].nlargest(top_n).index.tolist() 
                  for n, col in enumerate(idf.T)}).T
print(tfidf_top_topics)

tfidf_top_topics.to_csv('/content/top_topics_programmes.csv', sep=';')

"""Cosine distance"""

import gensim
import math

from gensim import corpora
import gensim.downloader as api
from gensim.utils import simple_preprocess
print(gensim.__version__)

import json
info = api.info()

nzz_articles = pd.read_csv('/content/article_features.csv',sep=';',encoding='latin-1')
nzz_articles = list(nzz_articles[:1000][nzz_articles.columns[1]])
print(nzz_articles)
print(len(nzz_articles))

"""Do we see any correlation between Swiss parties ?"""

print(idf)

from sklearn.metrics.pairwise import cosine_similarity
df2 = pd.DataFrame(cosine_similarity(idf, dense_output=True))
df2

"""For NZZ articles"""

test_article = nzz_articles[1]
print(test_article)

test_article = nlp(cleaning_pipeline(test_article))
print(test_article)

from gensim.similarities import WordEmbeddingSimilarityIndex
import gensim.downloader as api
from gensim import corpora
from gensim.similarities import SparseTermSimilarityMatrix, WordEmbeddingSimilarityIndex
from gensim.similarities import Similarity

#Trying with our 7 parties' programmes 

article = str(test_article).split()
programme = [programme_0,programme_1,programme_2,programme_3,programme_4,programme_5,programme_6]

for progr in programme:
  article = str(test_article).split()
  print('progr',progr)
  print('article',article)
  documents = [article,progr]
  
# Prepare a dictionary and a corpus.
  dictionary = corpora.Dictionary(documents)

# Prepare the similarity matrix
  similarity_index = WordEmbeddingSimilarityIndex(documents)
  similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary)

# Convert the sentences into bag-of-words vectors.
  article = dictionary.doc2bow(article)
  progr = dictionary.doc2bow(progr)

# Compute soft cosine similarity
  similarity = similarity_matrix.inner_product(article, progr, normalized=(True,True))
  print('similarity = %.4f' % similarity)

from sklearn.feature_extraction.text import TfidfVectorizer

tf = TfidfVectorizer(input=nzz_articles[0], analyzer='word', ngram_range=(1,6),
                     min_df = 0, stop_words = STOPWORDS, sublinear_tf=True)
tfidf_matrix =  tf.fit_transform(wordDict0)

tfidf_matrix

feature_names = tf.get_feature_names_out()
print(feature_names)
print(len(feature_names))

corpus_index = [n for n in wordDict0]
import pandas as pd
df = pd.DataFrame(tfidf_matrix.T.todense(), index=feature_names, columns=corpus_index)
print(len(df))
df.to_csv('/content/tfidf_nee_articles.csv',sep=';',encoding='utf8')



"""For NZZ articles

"""

import gensim
import pprint
from gensim import corpora
from gensim.utils import simple_preprocess

nzz_articles = pd.read_csv('/content/article_features.csv',sep=';',encoding='latin-1')
nzz_articles['text_processed'] = nzz_articles['text'].fillna('').astype(str).map(cleaning_pipeline)

print(nzz_articles.head())

doc_tokenized = [simple_preprocess(doc,min_len = 3,max_len=30) for doc in nzz_articles['text_processed']]

print(nzz_articles.head())

for i in range(len(doc_tokenized)):
  print(doc_tokenized[i])

"""
doc_tokenizer seems fine , let's try something else
https://medium.com/betacom/bow-tf-idf-in-python-for-unsupervised-learning-task-88f3b63ccd6d"""

#!pip install --upgrade gensim
import pandas as pd
import gensim
from gensim.parsing.preprocessing import preprocess_documents

text_corpus = programme_0 + programme_1 +programme_2 + programme_3 + programme_4 + programme_5+programme_6

processed_corpus = preprocess_documents(text_corpus)
dictionary = gensim.corpora.Dictionary(processed_corpus)
bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]

print(processed_corpus)
print(len(processed_corpus))

print(dictionary)

test_nzz = (nzz_articles['text_processed'][2])

tfidf = gensim.models.TfidfModel(bow_corpus, smartirs='npu')

index = gensim.similarities.MatrixSimilarity(tfidf[bow_corpus])
print(index)

new_doc = gensim.parsing.preprocessing.preprocess_string(test_nzz)
new_vec = dictionary.doc2bow(new_doc)
vec_bow_tfidf = tfidf[new_vec]
sims = index[vec_bow_tfidf]

for s in sorted(enumerate(sims), key=lambda item: -item[1])[:10]:
    print(f"{nzz_articles['text_processed'].iloc[s[0]]} : {str(s[1])}")



"""Testing https://github.com/varun21290/medium/blob/master/Document%20Similarities/Document_Similarities.ipynb"""

import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

df_articles = pd.read_csv('/content/article_features.csv',sep=';', encoding='latin1')

print(df_articles.head())

list_test_data = []
for i in range(100):
  doc = nlp(cleaning_pipeline(df_articles['text'][i]))
  print(str(i) + " "+str(doc))
  list_test_data.append(''+str(doc)+'')

list_test_data

documents_df=pd.DataFrame(list_test_data,columns=['documents'])

documents_df

documents_df['documents_cleaned']=documents_df.documents.apply(lambda x: " ".join(re.sub(r'[^a-zA-Z]',' ',w).lower() for w in x.split() if re.sub(r'[^a-zA-Z]',' ',w).lower() not in STOPWORDS) )

tfidfvectoriser=TfidfVectorizer(max_features=256)
tfidfvectoriser.fit(documents_df.documents_cleaned)
tfidf_vectors=tfidfvectoriser.transform(documents_df.documents_cleaned)

tfidf_vectors.shape

# Every vector is already normalised to have unit L2 norm
np.linalg.norm(tfidf_vectors[0],2)

tfidf_vectors=tfidf_vectors.toarray()
print (tfidf_vectors[0])

pairwise_similarities=np.dot(tfidf_vectors,tfidf_vectors.T)
pairwise_differences=euclidean_distances(tfidf_vectors)

print (tfidf_vectors[0])
print (pairwise_similarities.shape)
print (pairwise_similarities[0][:])

def most_similar(doc_id,similarity_matrix,matrix):
    print (f'Document: {documents_df.iloc[doc_id]["documents"]}')
    print ('\n')
    print (f'Similar Documents using {matrix}:')
    if matrix=='Cosine Similarity':
        similar_ix=np.argsort(similarity_matrix[doc_id])[::-1]
    elif matrix=='Euclidean Distance':
        similar_ix=np.argsort(similarity_matrix[doc_id])
    for ix in similar_ix:
        if ix==doc_id:
            continue
        print('\n')
        print (f'Document: {documents_df.iloc[ix]["documents"]}')
        print (f'{matrix} : {similarity_matrix[doc_id][ix]}')

most_similar(0,pairwise_similarities,'Cosine Similarity')



"""D2V embeddings"""

from gensim.models.doc2vec import Doc2Vec, TaggedDocument

tagged_data = [TaggedDocument(words=word_tokenize(doc), tags=[i]) for i, doc in enumerate(documents_df.documents_cleaned)]

print(tagged_data)

model_d2v = Doc2Vec(vector_size=100,alpha=0.025, min_count=1)
  
model_d2v.build_vocab(tagged_data)

for epoch in range(100):
    model_d2v.train(tagged_data,
                total_examples=model_d2v.corpus_count,
                epochs=model_d2v.epochs)

document_embeddings=np.zeros((documents_df.shape[0],100))

for i in range(len(document_embeddings)):
    document_embeddings[i]=model_d2v.docvecs[i]

pairwise_similarities=cosine_similarity(document_embeddings)
pairwise_differences=euclidean_distances(document_embeddings)

most_similar(0,pairwise_similarities,'Cosine Similarity')

