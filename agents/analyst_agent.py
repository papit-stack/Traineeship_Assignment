from model.models import get_chat_model
from langchain.agents import create_agent
from prompt import ANALYST_AGENT_PROMPT
from schema import ResearchBrief


agent=create_agent(model=get_chat_model(),system_prompt=ANALYST_AGENT_PROMPT,response_format=ResearchBrief)


def analyst_agent(query:str,research_findings:list):
    """Write short desc based on research finding"""
    response=agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                Original research query:
                {query}

                Research findings collected by the Researcher:
                {research_findings}

                Analyze these findings and create the market
                research brief.
                """
            }
        ]
    })

    return response["structured_response"]


