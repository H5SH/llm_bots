import nest_asyncio
from fastapi import FastAPI
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex

nest_asyncio.apply()

llm = Groq(model="llama3-8b-8192")
embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')

index = VectorStoreIndex.from_documents()

Settings.llm = llm
Settings.embed_model = embed_model

documents = SimpleDirectoryReader(input_files=['C:\H5SH\other\projects\ML_projects\sql_bot\\assests\Cms1500 manual.pdf']).load_data()

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=3)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/cmsform/validation")
def validate_form():
    return {'valid': True}