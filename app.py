import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage

from src.llm_chain import system_message, llm, agent

st.title("Чат-бот лікарні")

user_query = st.chat_input("Ваше повідомлення")

if "history" not in st.session_state:
    st.session_state.history = [system_message]

if user_query:
    human_message = HumanMessage(user_query)

    messages = st.session_state['history']
    messages.append(human_message)

    result = agent.invoke({"messages": messages})

    ai_message = result["messages"][-1]
    messages.append(ai_message)

    for message in messages:
        if isinstance(message, SystemMessage):
            continue

        if isinstance(message, HumanMessage):
            role = "human"
            avatar = None
        else:
            role = "ai"
            avatar = "🏥"

        with st.chat_message(role, avatar=avatar):
            st.markdown(message.text)