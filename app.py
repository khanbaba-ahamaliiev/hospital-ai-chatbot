import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage

from src.config import settings
from src.llm_chain import system_message, agent

st.title("Чат-бот лікарні")

user_query = st.chat_input("Ваше повідомлення")

if "history" not in st.session_state:
    st.session_state.history = [system_message]

if user_query:
    human_message = HumanMessage(user_query)

    messages = st.session_state['history']
    messages.append(human_message)

    if len(messages) > settings.chat.max_history_turns + 1:
        st.session_state.history = [system_message] + messages[-settings.chat.max_history_turns:]
        messages = st.session_state.history

    with st.spinner("Шукаю інформацію..."):
        result = agent.invoke({"messages": messages})

    ai_message = result["messages"][-1]
    messages.append(ai_message)

    for message in messages:
        if isinstance(message, SystemMessage):
            continue

        if isinstance(message, HumanMessage):
            role = "human"
            avatar = "👤"

        else:
            role = "ai"
            avatar = "🏥"

        with st.chat_message(role, avatar=avatar):
            st.markdown(message.text)