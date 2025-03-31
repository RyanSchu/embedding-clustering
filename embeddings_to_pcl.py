import sqlite3
import pickle as pkl
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

subsections = ['Session Summary','Evaluation of Stuck Points','Evidence Against Stuck Points','Alternative Perspectives',
    'Changes in Stuck Points','Emotional Changes','Symptoms and Changes','Potential Barriers to Care','Analysis Goals']

def fetchEmbeddings(section):
    print('====/fetching embeddings from db')
    con = sqlite3.connect("/Users/ryanschubert/Documents/embedding-clustering/embeddings.db")
    cur = con.cursor()
    sqlresponse = cur.execute("SELECT * FROM embeddings where Section = ?",[section])
    response = sqlresponse.fetchall()
    con.close()
    return response


pcl_data =  pd.read_csv('/Users/ryanschubert/Documents/LLM-PCL-Modeling/Deidentified_Survey_Disc_Removed_transcripts_with_psychometrics.txt',sep='|')


subsections[0]

#color by end point pcl
#color by start point pcl
#color by total change in pcl
#color by next day pcl
#color by change between days pcl