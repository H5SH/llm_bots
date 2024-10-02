import nest_asyncio
from fastapi import FastAPI
from llama_index.core import (
    Settings, 
    VectorStoreIndex,
    SimpleDirectoryReader 
)
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pathlib import Path
import os
from pypdf import PdfReader

nest_asyncio.apply()

file_paths = [
    'C:\H5SH\other\projects\ML_projects\sql_bot\\assests\Cms1500 manual.pdf',
    'C:\H5SH\other\projects\ML_projects\sql_bot\\assests\cms1500.pdf'
]

output_dir = 'C:\H5SH\other\projects\ML_projects\sql_bot\\cms'

for file_path in file_paths:
    # page = next(iter())
    name = os.path.splitext(os.path.basename(file_path))[0]
    reader = PdfReader(file_path)
    print(len(reader.pages))
    page = reader.pages[0] 
    text = page.extract_text()

    cms_path = Path('cms')
    if not cms_path.exists():
        Path.mkdir(cms_path)
    
    with open(cms_path / f'{name}.txt', 'w') as fp:
        fp.write(text)

# llm = Groq(model="llama3-8b-8192")
# embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')

# index = VectorStoreIndex.from_documents()

# Settings.llm = llm
# Settings.embed_model = embed_model

# documents = SimpleDirectoryReader(input_files=['C:\H5SH\other\projects\ML_projects\sql_bot\\assests\Cms1500 manual.pdf']).load_data()

# index = VectorStoreIndex.from_documents(documents)
# query_engine = index.as_query_engine(similarity_top_k=3)

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/cmsform/validation")
# def validate_form():
#     return {'valid': True}