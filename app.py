import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

RESPONSE_LIMIT = 3
REFINE_KEY = 0
EXPLORE_KEY = 1
INDUSTRY = "fashion"
PURPOSE = "recommends combinations of clothes"

SEARCH_SYSTEM_PROMPT = "You are a helpful assistant on an e-commerce " + INDUSTRY + " site that " + PURPOSE + " based on the human's query. Limit yourself to " + str(RESPONSE_LIMIT) + " recommendations at a time, where each recommendation is a sentence describing the recommendation."
REFINE_SYSTEM_PROMPT = SEARCH_SYSTEM_PROMPT + "The customer will give two queries separated by \n, the second will be a refined version of the first. Use the second to make adjustments to the first, and provide a response to the final resultant query."

def load_response(question, systemPrompt):
    llm = ChatOpenAI()
    messages = [
        SystemMessage(content=systemPrompt),
        HumanMessage(content=question)
    ]
    response = llm(messages)
    return response

def get_text(key):
    input_text = st.text_input("", key=key)
    return input_text

def write_response(rawResponse):
    response = rawResponse.content.splitlines()

    st.write(response[0])
    refine_0 = st.button('Refine', key = 'refine0')
    explore_0 = st.button('Explore', key = 'explore0')

    st.write(response[1])
    refine_1 = st.button('Refine', key = 'refine1')
    explore_1 = st.button('Explore', key = 'explore1')

    st.write(response[2])
    refine_2 = st.button('Refine', key = 'refine2')
    explore_2 = st.button('Explore', key = 'explore2')

    while(True):
        if refine_0 :
            return [REFINE_KEY, response[0]]
        elif explore_0 : 
            return [EXPLORE_KEY, response[0]]
        elif refine_1 :
            return [REFINE_KEY, response[1]]
        elif explore_1 : 
            return [EXPLORE_KEY, response[1]]
        elif refine_2 :
            return [REFINE_KEY, response[2]]
        elif explore_2 : 
            return [EXPLORE_KEY, response[2]]


state = st.session_state
if "submitted" not in state:
    state.submitted = False
    
st.set_page_config(page_title="Refined Search", page_icon=":robot:")
st.header("Refined Search")

user_input=get_text("search1")
response = load_response(user_input, SEARCH_SYSTEM_PROMPT)

search = st.button('Search')

if search or state.submitted:
    state.submitted = True
    nextAction = write_response(response)
    while nextAction[0] == REFINE_KEY:
        user_input = get_text("refine")
        refine_query = nextAction[1] + "\n" + user_input
        response = load_response(refine_query, REFINE_SYSTEM_PROMPT)
        nextAction = write_response(response)

    if nextAction[1] == EXPLORE_KEY:
        st.header("Now exploring: "+ nextAction[1])
        state.submitted = False
        