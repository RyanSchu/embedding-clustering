import sqlite3
import pickle as pkl
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def fetchEmbeddings():
    print('====/fetching embeddings from db')
    con = sqlite3.connect("/Users/ryanschubert/Documents/embedding-clustering/embeddings.db")
    cur = con.cursor()
    sqlresponse = cur.execute("SELECT * FROM embeddings")
    response = sqlresponse.fetchall()
    con.close()
    return response


    # "EmbeddingId" INTEGER PRIMARY KEY, 
    # "SectionId" INTEGER,
    # "PatientId" VARCHAR(500),
    # "SessionNumber" Integer,
    # "Section" VARCHAR(5000),
    # "message" VARCHAR(5000),
    # "Embedding" VARBINARY,
    # "CreateDate" DATETIME

def preprocessDatapoint(vec):
    embeddings = pkl.loads(vec[6])
    return (embeddings)


byte_embeddings_list = fetchEmbeddings()
embeddings_list = [preprocessDatapoint(x) for x in byte_embeddings_list]
embeddings_df = pd.DataFrame(embeddings_list)
print(embeddings_df)

# print(pcl_dat.columns)
pca = PCA()
# cosine_tsne = TSNE(n_components=2,random_state = 0, n_iter = 1000, metric = 'cosine')
embedding_pca = pca.fit_transform(embeddings_df)
# euclidian_tsne = TSNE(random_state = 0, n_iter = 1000)
# print(pca.components_)
# print(embedding_pca.explained_variance_ratio_)
# print(len(embedding_pca.components_))

principal_components = pd.DataFrame(data = embedding_pca)
print(principal_components[1])
# embeddings2d = pca.components_


pcl_data =  pd.read_csv('/Users/ryanschubert/Documents/LLM-PCL-Modeling/Deidentified_Survey_Disc_Removed_transcripts_with_psychometrics.txt',sep='|')
pcl_data = pcl_data.drop('transcript',axis=1)

embeddingsdf = pd.DataFrame()
embeddingsdf['EmbeddingId'] = [x[0] for x in byte_embeddings_list]
embeddingsdf['PatientId'] = [x[2] for x in byte_embeddings_list]
embeddingsdf['SessionNumber'] = [x[3] for x in byte_embeddings_list]
embeddingsdf['Section'] = [x[4] for x in byte_embeddings_list]
embeddingsdf['x'] = principal_components[0]
embeddingsdf['y'] = principal_components[1]
embeddingsdf['z'] = principal_components[2]

embeddingsdf= pd.merge(embeddingsdf,pcl_data,on=['PatientId','SessionNumber'],how='inner')

# print(embeddingsdf.head())

# # # Scatter points, set alpha low to make points translucent
# # # fig, ax = plt.subplots()
# # # ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
# # # ax.scatter(embeddingsdf.x, embeddingsdf.y, c=embeddingsdf.SessionNumber, cmap='magma',alpha=.5)
# # # plt.colorbar()
# # # plt.title('Scatter plot of document embeddings using t-SNE')
# # # plt.show()


fig, ax = plt.subplots()
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
ax.scatter(embeddingsdf.x, embeddingsdf.y, marker='o', linestyle='', c=embeddingsdf.pcl5_score_pastday_day_5,alpha=.5,cmap='magma')
plt.title('Scatter plot of document embeddings using PCA')
plt.show()




