from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from langchain_core.messages import AnyMessage
from langgraph.graph import StateGraph,START,END
from agents.research_agent import research_agent
from agents.analyst_agent import analyst_agent
from schema import ResearchBrief


#load environmental variables
load_dotenv()


#defined class state
class ResearchState(BaseModel):
    query:str   
    research_findings: Optional[list] = None
    research_brief: Optional[ResearchBrief] = None

    

#create node
def research_node(state:ResearchState):
    """Search on web and gather research findings"""
    query=state.query
    output=research_agent(query)
    return {'research_findings':output}

def analyst_node(state:ResearchState):
    """Writes research brief based on query and research findings"""
    output=analyst_agent(state.query,state.research_findings)
    return {'research_brief':output}

#create graph
graph=StateGraph(ResearchState)

#add node
graph.add_node("research_node",research_node)
graph.add_node("analyst_node",analyst_node)

#add edge
graph.add_edge(START,"research_node")
graph.add_edge("research_node","analyst_node")
graph.add_edge("analyst_node",END)

workflow=graph.compile()

if __name__=="__main__":
    response=workflow.invoke({"query": "Analyze the food delivery market in Nepal"})
    print(f"Summary: {response['research_brief'].summary} ")
    print(f"Competitiors: {response['research_brief'].competitors} ")
    print(f"Key Observation: {response['research_brief'].key_observation} ")
    print(f"Sources: {response['research_brief'].sources} ")
    print(f"Missing_information: {response['research_brief'].missing_information} ")