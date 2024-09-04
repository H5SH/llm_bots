import nest_asyncio
from urllib.parse import quote_plus
from sqlalchemy import (create_engine)
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.core import SQLDatabase
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.indices.struct_store import NLSQLTableQueryEngine



def connect_model():    
    nest_asyncio.apply()
    llm = Groq(model="llama3-8b-8192")
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
    return query_engine