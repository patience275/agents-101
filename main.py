import os
from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from tools import search_tool,wiki_tool

mistral_api=os.getenv('MISTRAL_API_KEY')
llm=init_chat_model(model='mistral-small-latest',model_provider='mistralai')
response=llm.invoke('whats the capital of france?')
print(response)

from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

class llmresponse(BaseModel):
    topic:str
    summary:str
    sources: list[str]
    tools_used:list[str]

parser=PydanticOutputParser(pydantic_object=llmresponse)

from langchain_core.prompts import ChatPromptTemplate
prompt=ChatPromptTemplate.from_messages([
    ('system',
    """
    you are a research assistant that will help in writing the research paper. answer the user quey and use necessary tools. 
    wrap the output inthis format and provide no other text \n{format_instructions}
    """),
    ('placeholder','{chat_history}'),
    ('human','{query}'),
    ('placeholder','{agent_scratchpad}')]
    ).partial(format_instructions=parser.get_format_instructions())

from langchain.agents import create_tool_calling_agent, AgentExecutor
tools=[search_tool,wiki_tool]
agent=create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )
agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)
query=input('what are you interesetd in knowing today? ')
agent_testing=agent_executor.invoke({
        'query':query
    })

try:
    structured_response = parser.parse(agent_testing['output'].strip("`").replace("json\n", "", 1))
    print(structured_response)
except Exception as e:
    print('error parsing respose')



  