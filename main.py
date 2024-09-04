import uvicorn
import nest_asyncio
from typing import Union
from fastapi import FastAPI
from urllib.parse import quote_plus
from llama_index.core import Settings
from sqlalchemy import (create_engine)
from llama_index.llms.groq import Groq
from llama_index.core import SQLDatabase
from fastapi.middleware.cors import CORSMiddleware
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.indices.struct_store import NLSQLTableQueryEngine
from llama_index.core.indices.struct_store import NLSQLTableQueryEngine

app = FastAPI()

origins = [
    'http://doctorsapp.test:81'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

nest_asyncio.apply()
llm = Groq(model="llama3-70b-8192")
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.llm = llm
Settings.embed_model = embed_model 
engine = create_engine("mysql+pymysql://root:%s@localhost:3306/doctorsapp" % quote_plus("1234hello1234"))
sql_database = SQLDatabase(engine)
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["patients", "providers", "labs", "invoices", "ledgers", "manufacturers", "medicines", "migrations", "model_has_permissions", "model_has_roles", "options", "prescriptions", "provider_schedules", "providers", "vitals"],
    llm=llm
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/doctors/bot/patient/vitals/{patient_id}")
def read_item(patient_id: str, q: Union[str, None] = None):
    response = query_engine.query(f"can you give me the vitals data of patient with this uuid {patient_id} ?")
    return {"patient_id": patient_id, "response": response}

if __name__ == '__main__':
    uvicorn.run(app)