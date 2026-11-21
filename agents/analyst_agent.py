from model.models import get_chat_model
from langchain.agents import create_agent
from prompt import ANALYST_AGENT_PROMPT
from schema import ResearchBrief


agent=create_agent(model=get_chat_model(),system_prompt=ANALYST_AGENT_PROMPT,response_format=ResearchBrief)


def analyst_agent(query:str,research_findings:list,previous_draft:ResearchBrief=None,feedback:str=None):
    """Generate or revise a market research brief."""

    if feedback and previous_draft:
        task_instruction = f"""
        You previously generated the following research brief:

        {previous_draft.model_dump_json(indent=2)}

        The Critic reviewed your brief and provided this feedback:

        {feedback}

        Your task is to REVISE your previous brief.

        Instructions:
        - Address the Critic's feedback.
        - Preserve sections that are already correct.
        - Correct unsupported or inaccurate claims.
        - Use only the provided research findings.
        - Do not invent statistics or information.
        - If information is unavailable, explicitly mention it.
        - Return the complete revised research brief.
        """

    else:

        task_instruction = """
        Generate an market research brief.

        Analyze the available research findings and produce
        a concise, evidence-based report.

        Do not invent information.
        Explicitly identify unavailable information.
        """

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                Original research query:
                {query}

                Research findings:
                {research_findings}

                {task_instruction}
                """
            }
        ]
    })

    return response["structured_response"]

