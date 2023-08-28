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
EXAMPLE = "Neutral colored Midi-length Dresses with Blazers."

SEARCH_SYSTEM_PROMPT = "You are a helpful assistant on an e-commerce " + INDUSTRY + " site that " + PURPOSE + " based on the human's query. Limit yourself to " + str(RESPONSE_LIMIT) + " recommendations at a time, where each recommendation is a short and direct sentence describing the recommendation. Example : '" + EXAMPLE + "'"
REFINE_SYSTEM_PROMPT = "You will receive two statements from the human as an input separated by '\n'. The second statement is a correction to be made to the first. Return the resultant statement by changing the first statement to include the second."

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

def write_search_response(rawResponse):
    response = rawResponse.content.splitlines()

    st.write(response[0])

    st.write(response[1])

    st.write(response[2])

    refine = st.button('Refine')
    explore = st.button('Explore')

    while True:
        if refine :
            selected_prompt = get_text("selected_refine")
            user_input = get_text("refine")
            return [REFINE_KEY,  response[int(selected_prompt) + "\n " + user_input]]
        
        if explore : 
            selected_prompt = get_text("selected_explore")
            return [EXPLORE_KEY, response[int(selected_prompt)]]

    st.write("We're out of write search")
    

def write_refine_response(rawResponse):
    response = rawResponse.content

    st.write(response)
    refine_r = st.button('Refine', key = 'refine_r')
    explore_r = st.button('Explore', key = 'explore_r')

    if refine_r:
        selected_prompt = get_text("selected_refine")
        user_input = get_text("refine")
        return [REFINE_KEY,  response[int(selected_prompt) + "\n " + user_input]]

    if explore_r:
        selected_prompt = get_text("selected_explore")
        return [EXPLORE_KEY, response[int(selected_prompt)]]


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
    nextAction = write_search_response(response)
    while nextAction[0] == REFINE_KEY:
        response = load_response(nextAction[1], REFINE_SYSTEM_PROMPT)
        nextAction = write_refine_response(response)

    if nextAction[1] == EXPLORE_KEY:
        st.header("Now exploring: "+ nextAction[1])
        state.submitted = False
        