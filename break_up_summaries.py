import pandas as pd
import pickle as pkl
import time
import sqlite3
from datetime import datetime
import re


#note evaluation of stuck points and potential barries to care both have subsections
subsections = ['Session Summary','Evaluation of Stuck Points','Identification','Refinement','Evidence Against Stuck Points','Alternative Perspectives',
    'Changes in Stuck Points','Emotional Changes','Symptoms and Changes','Potential Barriers to Care',
    'Internal Barriers','External Barriers','Analysis Goals']

def fetchAllSummaries():
    print('====/fetching summaries from db')
    con = sqlite3.connect("/Users/ryanschubert/Documents/llm_benchmarking/iterative_predictions.db")
    cur = con.cursor()
    sqlresponse = cur.execute("SELECT * FROM survey_removed_summaries")
    summaries = sqlresponse.fetchall()
    summaries = pd.DataFrame(summaries, columns =['PredictionId', 'PatientId', 'SessionNumber','message','model','CreateDate'])
    con.close()
    return summaries

def appendToSubsections(input_data):
    print('====/appending to pred db')
    con = sqlite3.connect("/Users/ryanschubert/Documents/embedding-clustering/embeddings.db")
    cur = con.cursor()
    cur.execute("INSERT INTO subsections VALUES(null, :PatientId, :SessionNumber, :Section, :message, :CreateDate)", input_data)
    con.commit()
    con.close()
    return

def fetchSubsection(PatientId,SessionNumber,Section):
    print('====/fetching subsection from db')
    con = sqlite3.connect("/Users/ryanschubert/Documents/embedding-clustering/embeddings.db")
    cur = con.cursor()
    sqlresponse = cur.execute("SELECT * FROM subsections WHERE PatientId == ? AND SessionNumber == ? AND Section == ?", [PatientId,SessionNumber,Section])
    summaries = sqlresponse.fetchall()
    con.close()
    return summaries

def extractSubsections(session_data):
    PatientId=session_data.PatientId[0]
    SessionNumber=session_data.SessionNumber[0]

    # print(session_data)
    subsections = ['Session Summary','Evaluation of Stuck Points','Evidence Against Stuck Points','Alternative Perspectives',
    'Changes in Stuck Points','Emotional Changes','Symptoms and Changes','Potential Barriers to Care','Analysis Goals']
    summary = session_data.message[0]
    # print(summary)
    split_summary =re.split('\n',summary)
    section_bounds = []
    for sub in subsections:
        index=[i for i,x in enumerate(split_summary) if sub in x]
        if len(index) == 0: continue
        section_bounds.append((sub,index))

    for i,section in enumerate(section_bounds):
        # print(section)
        section_name = section[0]
        section_start = section[1][0] + 1
        existing_sections=fetchSubsection(PatientId,SessionNumber,section_name)
        if len(existing_sections) != 0: 
            print('skipping')
            continue
        if i < (len(section_bounds)-1):
            try:
                section_end = section_bounds[i+1][1][0]
                text = ' '.join(split_summary[section_start:section_end])
                extracted_section = {
                    "PatientId": PatientId,
                    "SessionNumber": SessionNumber,    
                    "Section":section_name,
                    "message":text,
                    'CreateDate':datetime.now()
                }
                appendToSubsections(extracted_section)
            except Exception as e:
                print(e)
        else:
            try:
                text = ' '.join(split_summary[section_start:])
                extracted_section = {
                    "PatientId": session_data.PatientId[0],
                    "SessionNumber": session_data.SessionNumber[0],    
                    "Section":section_name,
                    "message":text,
                    'CreateDate':datetime.now()
                }
                appendToSubsections(extracted_section)
            except Exception as e:
                print(e)
    return


data = fetchAllSummaries()
patients_list = data.PatientId.unique()
session_list  = range(1,9)

for patient in patients_list:
    for session in session_list:
        session_data = data.loc[(data.PatientId == patient) & (data.SessionNumber == session)].reset_index()
        if session_data.empty:
            continue
        extractSubsections(session_data)

### Evaluation of Stuck Points
# **Identification:**
# **Refinement:**
### Evidence Against Stuck Points
### Alternative Perspectives
### Changes in Stuck Points
### Emotional Changes
### Symptoms and Changes
### Potential Barriers to Care
# **Internal Barriers**
# **External Barriers**
### Analysis Goals




