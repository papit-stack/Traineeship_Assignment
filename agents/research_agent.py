from model.models import get_chat_model
from langchain.agents import create_agent
from prompt import RESEARCH_AGENT_PROMPT
from langchain_tavily import TavilySearch
import json

tavily=TavilySearch(max_results=5)

agent=create_agent(model=get_chat_model(),tools=[tavily],system_prompt=RESEARCH_AGENT_PROMPT)

def research_agent(query:str):
    """Searches the web and gather information"""
    response=agent.invoke({"messages": query})
    results=[]
    for message in response["messages"]:
        if message.type == "tool" and message.name=="tavily_search":
            tool_data = json.loads(message.content)

            # Extract search results
            for data in tool_data["results"]:
                results.append({
                    "url": data["url"],
                    "title": data["title"],
                    "content": data["content"]
                })
    return results

if __name__=="__main__":
    response=research_agent("Analyze the food delivery market in Nepal")
    print(response)
