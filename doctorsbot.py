import json
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
from llama_index.program.lmformatenforcer import (
    LMFormatEnforcerPydanticProgram
)
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pydantic import BaseModel, Field
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.core import (
    VectorStoreIndex
)
from llama_index.core.query_engine import RetrieverQueryEngine
from langchain_experimental.llms import LMFormatEnforcer
import sys
from pydantic import BaseModel, Field
from typing import List

from llama_index.program.lmformatenforcer import (
    LMFormatEnforcerPydanticProgram
)


class BetterText(BaseModel):
    changed: str
    changes: str
    
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
llm = Groq(model="llama3-8b-8192")
screen_name = {
    "name": str
}
llm.output_parser = {"name": Field(max_length=12, type=str)} 
llm.pydantic_program_mode = True 
# llm = LlamaCPP()
# embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
# Settings.llm = llm
# Settings.embed_model = embed_model 
# engine = create_engine("mysql+pymysql://root:%s@localhost:3306/doctorsapp" % quote_plus("1234hello1234"))
# sql_database = SQLDatabase(engine)
# query_engine = NLSQLTableQueryEngine(
#     sql_database=sql_database,
#     tables=["patients", "providers", "labs", "invoices", "ledgers", "manufacturers", "medicines", "migrations", "model_has_permissions", "model_has_roles", "options", "prescriptions", "provider_schedules", "providers", "vitals"],
#     llm=llm
# )

# program = LM
screens = [
    'patient',
    'provider',
    'prescription',
    'vitals',
    'appointment',
    'invoice'
]



# regex = r'"Navigate To: (?P<name>[a-zA-Z]*)\."'
# regex_parser = lmformatenforcer.RegexParser(regex)
# lm_format_enforcer_fn = build_lm_format_enforcer_function(llm, regex_parser)

# program = LMFormatEnforcerPydanticProgram(
#     output_cls=ScreenName,
#     prompt_template_str=(
#         "Your response should be name of a screen from this array: {screens}\n"
#         "{query}\n"
#     ),
#     llm=llm,
# )

# def attach_to_session(executor_url, session_id):
#     original_execute = WebDriver.execute
#     def new_command_execute(self, command, params=None):
#         if command == "newSession":
#             # Mock the response
#             return {'success': 0, 'value': None, 'sessionId': session_id}
#         else:
#             return original_execute(self, command, params)
#     WebDriver.execute = new_command_execute
#     driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
#     driver.session_id = session_id
#     WebDriver.execute = original_execute
#     return driver


# driver = attach_to_session('http://127.0.6533.119:9515','bdef6783a05f0b3f885591e7d2c7b2aec1a89dea')

# for controlling webpage
# driver = webdriver.Chrome()
# driver.get('http://doctorsapp.test:81/patient')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/doctors/bot/patient/vitals/{patient_id}")
def read_item(patient_id: str, q: Union[str, None] = None):
    return {"patient_id": patient_id, "response": json.loads(response.source_nodes[0].node.text.replace('(', '').replace(')', ''))}

@app.get("/doctors/bot/database/model/")
def sql_connection(q: Union[str, None] = None):
    query_engine.query(q)

@app.get("/chat/doctors/bot")
def navigation_test(q: Union[str, None]=None):
    # output = program(query=q, screens=screens)
    output = llm.complete(f"answer in single word, which screen to open from patient, provider, prescription, vitals, invoice and appointment according to {q}")
    # json_data = json.loads(output)['name of screen']['name']
    # name_of_screen = json_data['name of screen']
    # name = json_data['name of screen']['name'] 
    name = str(output).lower()
    print(name, output, 'name')
    if name in screens or name == 'appointments':
        id = name == 'appointments' and 'appointment' or name
        navigate_button = driver.find_element(By.XPATH, f'//a[@id="sidebar_{id}"]')
        if(navigate_button):
            navigate_button.click()
            return {"output": ""}
    else:
        return {"output": str(output)}
    
# @app.get('/enforcer/test')
# def enforcer_test(q: Union[str, None]=None):
#     output = program(query=f"single word answer which screen to open from patient, provider, prescription, vitals, invoice and appointment according to {q}")
#     return {'result': str(output)}


@app.get("/improve/input")
def improve_input(q: Union[str, None]=None):
    # program = LMFormatEnforcerPydanticProgram(
    #     output_cls=BetterText,
    #     prompt_template_str=(
    #         "Your response should be according to the following json schema: \n"
    #         "{json_schema}\n"
    #         "change should consist of the new response whiles changes should consist of the changes you made"
    #     ),
    #     llm=llm,
    #     verbose=True
    # )
    response = llm.complete(f"make it better '{q}'")
    return {'response': str(response)}

if __name__ == '__main__':
    uvicorn.run(app)