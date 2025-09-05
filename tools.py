from langchain_community.tools import WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool 

search=DuckDuckGoSearchRun()
search_tool=Tool(
    name='search',
    func=search.run,
    description='search the web for infomation'
)

api_wraper=WikipediaAPIWrapper(top_k_results=1,doc_content_char_max=256)

wiki_tool=WikipediaQueryRun(api_wrapper=api_wraper)