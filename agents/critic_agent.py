from langchain.agents import create_agent
from model.models import get_chat_model
from prompt import CRITIC_AGENT_PROMPT
from schema import CriticSchema


agent=create_agent(model=get_chat_model(),system_prompt=CRITIC_AGENT_PROMPT,response_format=CriticSchema)


def critic_agent(query:str,research_findings:list, draft):

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                Query: {query}

                Research findings:
                {research_findings}
                
                Analyst draft:
                {draft}

                Review the draft.
                """
            }
        ]
    })

    return response["structured_response"]