import sqlite3
import pickle as pkl

con = sqlite3.connect("/Users/ryanschubert/Documents/embedding-clustering/embeddings.db")
cur = con.cursor()
sqlresponse = cur.execute("SELECT embedding FROM embeddings")
response = sqlresponse.fetchall()

unpickled=pkl.loads(response[0][0])
print(unpickled)

con.commit()
con.close()


