import nest_asyncio
from llama_index.llms.groq import Groq

nest_asyncio.apply()


llm = Groq(model="llama3-70b-8192")


q = ''
while True:
    print("Ask Anything")
    q = input()
    if(q=='q'):
        break
    response = llm.complete(q)
    print(str(response))
