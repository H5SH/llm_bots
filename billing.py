import nest_asyncio
from llama_index.core import (
    Settings, 
    VectorStoreIndex,
)
from llama_parse import LlamaParse
from llama_index.llms.groq import Groq
from llama_index.core import SimpleDirectoryReader
from llmsherpa.readers.file_reader import LayoutPDFReader
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.schema import Document
import os

nest_asyncio.apply()

llm = Groq(model="llama3-70b-8192")
embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')


Settings.llm = llm
Settings.embed_model = embed_model

# doc_menual = LlamaParse(result_type='text').load_data("C:\H5SH\other\projects\ML_projects\llm_bot\\assests\Cms1500 manual.pdf")
# doc_cms = LlamaParse(result_type='text').load_data("C:\H5SH\other\projects\ML_projects\llm_bot\\assests\\form-cms.pdf")

# doc_both = LlamaParse(result_type='text').load_data("C:/H5SH/other/projects/ML_projects/llm_bot/assests/Cms1500-manual.pdf")
llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
pdf_reader = LayoutPDFReader(llmsherpa_api_url)

print(pdf_reader.parser_api_url)

doc_form = pdf_reader.read_pdf('C:/H5SH/other/projects/ML_projects/llm_bot/assests/form-cms1500.pdf')
# doc_manual = pdf_reader.read_pdf('C:/H5SH/other/projects/ML_projects/llm_bot/assests/Cms1500-manual_merged.pdf')

# index = VectorStoreIndex([])
# for chunk in doc_form.chunks():
#     index.insert(Document(text=chunk.to_context_text(), extra_info={}))
# query_engine = index.as_query_engine()

# response = query_engine.query("how many fields in the document ?")

# print(str(response))

# documents = SimpleDirectoryReader(
#     input_files=[
#         'C:/H5SH/other/projects/ML_projects/llm_bot/assests/form-cms1500.pdf',
#         'C:/H5SH/other/projects/ML_projects/llm_bot/assests/Cms1500-manual_merged.pdf'
#     ]
# ).load_data()

# index = VectorStoreIndex.from_documents(documents)

# query_engine = index.as_query_engine(similarity_top_k=3)


## picking 10 fields  

# vector_tool = QueryEngineTool(
#     index.as_query_engine(),
#     metadata=ToolMetadata(
#         name="vector_search",
#         description="Useful for searching for specific facts."
#     )
# )

# summary_tool = QueryEngineTool(
#     index.as_query_engine(response_mode="tree_summarize"),
#     metadata=ToolMetadata(
#         name="summary",
#         description="Useful for summarizing an entire document."
#     )
# )

# query_engine = RouterQueryEngine.from_defaults(
#     [vector_tool, summary_tool], select_multi=True, verbose=True, llm=llm
# )

# q = ''

# while(q != 'q'):
#     print('Ask anything related to cmsform')
#     q = input()
#     response = query_engine.query(q)
#     print(str(response))



# print(str(response))


# index = VectorStoreIndex.from_documents(documents)
# query_engine = index.as_query_engine(similarity_top_k=3)

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/cmsform/validation")
# def validate_form():
#     return {'valid': True}