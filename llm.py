from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from langgraph.graph import StateGraph,START,END
from agents.research_agent import research_agent
from agents.analyst_agent import analyst_agent
from agents.critic_agent import critic_agent
from schema import ResearchBrief,CriticSchema


#load environmental variables
load_dotenv()


#Shared state
class ResearchState(BaseModel):
    query:str   
    research_findings: Optional[list] = None
    research_brief: Optional[ResearchBrief] = None
    evaluation:Optional[CriticSchema]=None
    retries:int=0
    

#create node
def research_node(state:ResearchState):
    """Search on web and gather research findings"""
    query=state.query
    output=research_agent(query)
    return {'research_findings':output}

def analyst_node(state:ResearchState):
    """Generate or revise the research brief"""
    output=analyst_agent(state.query,state.research_findings,state.research_brief,
                         (state.evaluation.feedback if state.evaluation else None))
    retries=state.retries
    if state.evaluation is not None:
        retries+=1
    return {'research_brief':output,"retries":retries}

def critic_node(state:ResearchState):
    """Evaluate the draft"""
    output=critic_agent(state.query,state.research_findings,state.research_brief)
    return {'evaluation':output}

def critic_router(state:ResearchState):
    if state.evaluation.decision=="approved":
        return "end"
    if state.retries<1:
        return "need_improvement"
    return "end"


#create graph
graph=StateGraph(ResearchState)

#add node
graph.add_node("research_node",research_node)
graph.add_node("analyst_node",analyst_node)
graph.add_node("critic_node",critic_node)

#add edge
graph.add_edge(START,"research_node")
graph.add_edge("research_node","analyst_node")
graph.add_edge("analyst_node","critic_node")
graph.add_conditional_edges("critic_node",critic_router,{"end":END,"need_improvement":"analyst_node"})


workflow=graph.compile()

if __name__=="__main__":
    response=workflow.invoke({"query": "Analyze the e-commerce market in Nepal."})
    print(f"Summary: {response['research_brief'].summary} ")
    print(f"Competitiors: {response['research_brief'].competitors} ")
    print(f"Key Observation: {response['research_brief'].key_observation} ")
    print(f"Sources: {response['research_brief'].sources} ")
    print(f"Missing_information: {response['research_brief'].missing_information} ")
    print(f"Retries:{response['retries']}")

    print(f"Decision: {response['evaluation'].decision} ")
    print(f"Feedback: {response['evaluation'].feedback} ")
    print(f"Suggestion: {response['evaluation'].suggestion} ")
    print(f"Confidence_score: {response['evaluation'].confidence_score} ")


