from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages,StateGraph,START,END
from agents.research_agent import research_agent


#load environmental variables
load_dotenv()

#defined class state
class ResearchState(BaseModel):
    query:str
    research_findings:list=[]
    

#create node
def research_node(state:ResearchState):
    query=state.query
    output=research_agent(query)
    return {'research_findings':output}



#create graph
graph=StateGraph(ResearchState)

#add node
graph.add_node("research_node",research_node)

#add edge
graph.add_edge(START,"research_node")
graph.add_edge("research_node",END)

workflow=graph.compile()

response=workflow.invoke({"query": "Analyze the food delivery market in Nepal"})
print(response)


