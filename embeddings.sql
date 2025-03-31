CREATE TABLE embeddings (
    "EmbeddingId" INTEGER PRIMARY KEY, 
    "PatientId" VARCHAR(500),
    "SessionNumber" Integer,    
    "embeddings" VARCHAR(5000),
    "model" TEXT,
    "CreateDate" DATETIME
); 

CREATE TABLE subsections (
    "SectionID" INTEGER PRIMARY KEY, 
    "PatientId" VARCHAR(500),
    "SessionNumber" Integer,    
    "Section" VARCHAR(5000),
    "message" VARCHAR(5000),
    "CreateDate" DATETIME
); 

 CREATE TABLE embeddings ( 
    "EmbeddingId" INTEGER PRIMARY KEY, 
    "SectionId" INTEGER,
    "PatientId" VARCHAR(500),
    "SessionNumber" Integer,
    "Section" VARCHAR(5000),
    "message" VARCHAR(5000),
    "Embedding" VARBINARY,
    "CreateDate" DATETIME
 );
