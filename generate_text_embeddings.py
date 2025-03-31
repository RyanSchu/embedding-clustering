from azure_gpt_instance import getAzureGptClient
import app_global
import pandas as pd
import pickle as pkl
import time
import sqlite3
from datetime import datetime


def fetchAllSubsection():
    print('====/fetching all subsections from db')
    con = sqlite3.connect("/Users/ryanschubert/Documents/embedding-clustering/embeddings.db")
    cur = con.cursor()
    sqlresponse = cur.execute("SELECT * FROM subsections")
    summaries = sqlresponse.fetchall()
    con.close()
    return summaries


def fetchEmbeddings(SectionId):
    print('====/fetching embeddings from db')
    con = sqlite3.connect("/Users/ryanschubert/Documents/embedding-clustering/embeddings.db")
    cur = con.cursor()
    sqlresponse = cur.execute("SELECT * FROM embeddings WHERE SectionId = ? ",[SectionId])
    response = sqlresponse.fetchall()
    con.close()
    return response

def appendEmbeddings(input_data):
    print('====/appending to embeddings db')
    # print(input_data)
    con = sqlite3.connect("/Users/ryanschubert/Documents/embedding-clustering/embeddings.db")
    cur = con.cursor()
    cur.execute("INSERT INTO embeddings VALUES(null, :SectionId, :PatientId, :SessionNumber, :Section, :message, :embedding,:CreateDate)", input_data)
    con.commit()
    con.close()
    return

#function that runs openai model
def generateEmbeddings(input):
    SectionId, PatientId, SessionNumberByte,Section,message, date = input
    existing_embeddings = fetchEmbeddings(SectionId)
    if len(existing_embeddings) == 0:
        gptmodel_instance = getAzureGptClient()
        openai_instance  = gptmodel_instance.get_azure_gpt_client()
        gpt_model = app_global.GPT_MODEL
        gpt_response = openai_instance.embeddings.create(input = [message], model=gpt_model).data[0].embedding    
        response = { 
                "SectionId":SectionId,
                "PatientId":PatientId,
                "SessionNumber":int.from_bytes(SessionNumberByte,byteorder='little'),
                "Section":Section,
                "message":message,
                "embedding": pkl.dumps(gpt_response),
                "CreateDate":datetime.now()
                }
        appendEmbeddings(response)
    else:
        print("skipped")
    return






data = fetchAllSubsection()

subsections = ['Session Summary','Evaluation of Stuck Points','Identification','Refinement','Evidence Against Stuck Points','Alternative Perspectives',
    'Changes in Stuck Points','Emotional Changes','Symptoms and Changes','Potential Barriers to Care',
    'Internal Barriers','External Barriers']
[generateEmbeddings(x) for x in data]

# for i in data:
#     print()
    # print(int.from_bytes(i[2],byteorder='little'))

# for patient in patients_list:
#     for session in session_list:
#         session_data = data.loc[(data.PatientId == patient) & (data.SessionNumber == session)].reset_index()
#         if session_data.empty:
#             continue
#         extractSubsections(session_data)