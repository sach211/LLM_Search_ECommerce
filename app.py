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

def get_text(key):
    input_text = st.text_input("", key=key)
    return input_text

def write_response(rawResponse):
    response = rawResponse.content.splitlines()
    for idx, item in enumerate(response):
        format_response_with_explore_refine(item, idx)

def format_response_with_explore_refine(responseItem, index):
    st.write(responseItem.content)
    refine = st.button('Refine', key = 'refine'+str(index))
    explore = st.button('Explore', key = 'refine'+str(index))


st.set_page_config(page_title="Refined Search", page_icon=":robot:")
st.header("Refined Search")

user_input=get_text("search1")
response = load_response(user_input)

search = st.button('Search')

if search:
    write_response(response)
    

    


    
    '''while refine and not explore:
        refine = not refine
        user_input=get_text("refine1")
        response = load_response(user_input)
        refine = st.button('Refine')
        explore = st.button('Explore')

        while refine and not explore:
            refine = not refine
        st.subheader("Response: ")
        st.write(response.content)'''