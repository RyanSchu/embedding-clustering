import sqlite3
import pickle as pkl
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib import cm, colors

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


pcl_data =  pd.read_csv('/Users/ryanschubert/Documents/LLM-PCL-Modeling/Deidentified_Survey_Disc_Removed_transcripts_with_psychometrics.txt',sep='|')
pcl_data = pcl_data.drop('transcript',axis=1)
pcl_data['pcl_delta'] = pcl_data.pcl5_score_pastmonth_intake - pcl_data.pcl5_score_pastday_day_5

for section in subsections:

    byte_embeddings_list = fetchEmbeddings(section)
    embeddings_list = [preprocessDatapoint(x) for x in byte_embeddings_list]
    embeddings_df = pd.DataFrame(embeddings_list)


    # pca = PCA()
    cosine_tsne = TSNE(n_components=2,random_state = 0, n_iter = 1000, metric = 'cosine')
    embeddings_tsne=cosine_tsne.fit_transform(embeddings_df)
    # embedding_pca = pca.fit_transform(embeddings_df)
    # euclidian_tsne = TSNE(random_state = 0, n_iter = 1000)
    # print(pca.components_)
    # print(embedding_pca.explained_variance_ratio_)
    # print(len(embedding_pca.components_))

    # principal_components = pd.DataFrame(data = embedding_pca)
    # print(principal_components[1])
    # embeddings2d = pca.components_

    embeddingsdf = pd.DataFrame()
    embeddingsdf['EmbeddingId'] = [x[0] for x in byte_embeddings_list]
    embeddingsdf['PatientId'] = [x[2] for x in byte_embeddings_list]
    embeddingsdf['SessionNumber'] = [x[3] for x in byte_embeddings_list]
    embeddingsdf['Section'] = [x[4] for x in byte_embeddings_list]
    embeddingsdf['x'] = embeddings_tsne[:,0]
    embeddingsdf['y'] = embeddings_tsne[:,1]

    embeddingsdf= pd.merge(embeddingsdf,pcl_data,on=['PatientId','SessionNumber'],how='inner')

    groups = embeddingsdf.groupby("SessionNumber")
    fig, ax = plt.subplots()
    ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
    for name, group in groups:
        ax.scatter(group.x, group.y, marker='o', linestyle='',label=name,alpha=.5)
        ax.legend()

    # fig, ax = plt.subplots()
    # ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
    # ax.scatter(embeddingsdf.x, embeddingsdf.y, marker='o', linestyle='', c=embeddingsdf.pcl_delta,alpha=.5,cmap='magma')
    # ax.legend()
    # cbar = fig.colorbar(cm.ScalarMappable(cmap='magma'), ax=ax)
    # cbar.ax.set_yticklabels([str(embeddingsdf.pcl_delta.max), str(embeddingsdf.pcl_delta.min)])
    plt.title('Scatter plot of ' + section + ' embeddings using TSNE')
    plt.savefig('/Users/ryanschubert/Documents/embedding-clustering/' + section + '_embeddings_TSNE_scatterplot_color_by_session_number.png')

