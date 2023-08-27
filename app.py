import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

def load_response(question):
    llm = ChatOpenAI()
    messages = [
        SystemMessage(content="You are a helpful assistant on an e-commerce fashion site that recommends combinations of outfits and clothes based on the human's query. Limit yourself to three recommendations at a time, where each recommendation is a sentence describing the recommendation."),
        HumanMessage(content=question)
    ]
    response = llm(messages)
    return response

st.set_page_config(page_title="Refined Search", page_icon=":robot:")
st.header("Refined Search")

def get_text(key):
    input_text = st.text_input("", key=key)
    return input_text

user_input=get_text("search1")
response = load_response(user_input)

submit = st.button('Generate')

if submit:
    st.subheader("Response: ")
    st.write(response.content)


user_input=get_text("refine1")
response = load_response(user_input)
submit = st.button('Refine')

if submit:
    st.subheader("Response: ")
    st.write(response.content)