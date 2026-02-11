import streamlit as st
from chat_bot import chatbot
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage 


if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []

thread_id='1'

CONFIG=config={'configurable':{'thread_id':thread_id}}
for messages in st.session_state['messages_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])

user_input=st.chat_input('Type your ')

if user_input:

    st.session_state['messages_history'].append({'role':'User','content':user_input})
    with st.chat_message('User'):
        st.text(user_input)

    response=chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=config)

    ai_message=response['messages'][-1].content

    st.session_state['messages_history'].append({'role':'AI Assistant','content':ai_message})
    with st.chat_message('AI'):
        st.text(ai_message)
