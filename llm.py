from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages,StateGraph,START,END


#load environmental variables
load_dotenv()


model=init_chat_model(model="gemini-3.5-flash-lite",model_provider="google_genai")


#defined class state
class ResearchState(BaseModel):
    messages:Annotated[list[AnyMessage], add_messages]


#create node
def research_data(state:ResearchState):
    output=model.invoke(state.messages)
    return {'messages':[output]}

#create graph
graph=StateGraph(ResearchState)

#add node
graph.add_node("research_node",research_data)

#add edge
graph.add_edge(START,"research_node")
graph.add_edge("research_node",END)

workflow=graph.compile()

response=workflow.invoke({'messages':"hello"})
print(response)