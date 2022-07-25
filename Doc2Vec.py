# -*- coding: utf-8 -*-
"""Doc2Vec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VCag7iTTh8V0IWBH8Gh-OUzi7HlI6dPp

Installing Gensim
"""

#!pip install --upgrade gensim

"""Installing dependencies"""

import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec
import nltk
import pandas as pd

nltk.download('punkt')

"""Data"""

data_test = ["The process of searching for a job can be very stressful, but it doesn’t have to be. Start with a\
        well-written resume that has appropriate keywords for your occupation. Next, conduct a targeted job search\
        for positions that meet your needs.",
        "Gardening in mixed beds is a great way to get the most productivity from a small space. Some investment\
        is required, to purchase materials for the beds themselves, as well as soil and compost. The\
        investment will likely pay-off in terms of increased productivity.",
        "Looking for a job can be very stressful, but it doesn’t have to be. Begin by writing a good resume with\
        appropriate keywords for your occupation. Second, target your job search for positions that match your\
        needs."]

data_programmes = pd.read_csv('polarization/Colab/programmes_processed.csv',sep=';',encoding='utf-8')
data_articles = pd.read_csv('polarization/Colab/articles_processed.csv',sep=';',encoding='utf-8')
data_programmes = list(data_programmes['programmes_processed'])
data_programmes

#data_articles = data_articles[:100]

"""Tagging data"""

tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data_programmes)]

"""Initialising Word2Vec"""

model = gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=2, epochs=150)

"""Building vocabulary"""

model.build_vocab(tagged_data)

"""Training doc2vec"""

model.train(tagged_data, total_examples=model.corpus_count, epochs=150)

"""Saving when training is done"""

model.save("d2v.model")

"""Most similar sentences"""

printcounter = 0
for i in range(len(data_articles['text_processed'])):
  test_data = word_tokenize(data_articles['text_processed'][i])
  if (printcounter == 1000):
        print('Progress report...')
        printcounter = 0
  v = model.infer_vector(test_data)
  similar_doc = model.dv.most_similar((v))
  data_articles.loc[i,'d2v_pred1']=similar_doc[0][0]
  data_articles.loc[i,'d2v_sim1']=similar_doc[0][1]

  data_articles.loc[i,'d2v_pred2']=similar_doc[1][0]
  data_articles.loc[i,'d2v_sim2']=similar_doc[1][1]

  data_articles.loc[i,'d2v_pred3']=similar_doc[2][0]
  data_articles.loc[i,'d2v_sim3']=similar_doc[2][1]
  printcounter +=1

data_articles.to_csv('polarization/Colab/articles_processed_d2v.csv', sep=';',encoding='utf-8')

data_articles.to_csv()
data_articles.to_csv()