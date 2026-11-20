from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages,StateGraph,START,END
from model.models import get_chat_model
from langchain_tavily import TavilySearch


#load environmental variables
load_dotenv()


model=get_chat_model()

output=model.invoke("hello")
print(output)



# #defined class state
# class ResearchState(BaseModel):
#     query:str
#     research_findings:list=[]


    
# tavily=TavilySearch(max_results=5)

# #create node
# def research_node(state:ResearchState):
#     query=state.query
#     output=tavily.invoke({'query':query})
#     return {'research_findings':output}


# #create graph
# graph=StateGraph(ResearchState)

# #add node
# graph.add_node("research_node",research_node)

# #add edge
# graph.add_edge(START,"research_node")
# graph.add_edge("research_node",END)

# workflow=graph.compile()

# response=workflow.invoke({"query": "Latest developments in artificial intelligence"})
# print(response.research_findings)


