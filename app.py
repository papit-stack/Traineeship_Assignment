import streamlit as st
from llm import workflow

st.title("Market Research Agent")
st.set_page_config(page_title="Market Research")


query=st.text_area("Enter a company or industry",placeholder="Example: Analyze the food delivery market in Nepal.")
if st.button("Research"):
    with st.spinner("Planning and researching..."):
        output=workflow.invoke({'query':query})
        brief = output["research_brief"]
        eval_ = output["evaluation"]
        st.subheader("Summary")
        st.write(brief.summary)
        st.subheader("Competitors")
        st.write(brief.competitors)
        st.subheader("Key Observations")
        st.write(brief.key_observation)
        st.subheader("Sources")
        st.write(brief.sources)
        st.subheader("Missing Information")
        st.write(brief.missing_information)
        # st.subheader("Review")
        # st.write(eval_.decision, eval_.feedback)