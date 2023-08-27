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
        SystemMessage(content="You are a helpful assistant on an e-commerce fashion site that recimmends combinations of outfits and clothes based on the human's query."),
        HumanMessage(content=question)
    ]
    response = llm(messages)

st.set_page_config(page_title="Refined Search", page_icon=":robot:")
st.header("Refined Search")

def get_text():
    input_text = st.text_input("", key="input")
    return input_text

user_input=get_text()
response = load_response(user_input)

submit = st.button('Generate')

if submit:
    st.subheader("Response: ")
    st.write(response.content)