import streamlit as st
import requests

# Local URLs for default Flask server
RECOMMENDATION_URL = "http://127.0.0.1:5000/rag/professorRecommendation"
RESPONSE_URL = "http://127.0.0.1:5000/rag/professorResponse"

st.title("LLMs and Pedagogical Approaches in English Literature")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

sidebar = st.sidebar

sidebar.title("Select which course you would like to focus on:")

course = sidebar.radio(
    "Course",
    [
        "Introduction to the Theory of Literature",
        "Milton",
        "Modern Poetry",
        "The American Novel Since 1945",
    ],
)

recommendation_title = sidebar.title("Recommendation")
default_recommendation = sidebar.markdown(
    "Chat with me more to have a detailed recommendation of a text."
)

if st.session_state.messages:
    default_recommendation.empty()

    previous_messages = [m["content"] for m in st.session_state.messages]

    recommendation_data = {"course": course, "messages": tuple(previous_messages)}

    recommendation = requests.post(RECOMMENDATION_URL, json=recommendation_data)

    if recommendation.status_code == 200:
        recommendation_text = recommendation.json()
        sidebar.markdown(recommendation_text)
    else:
        sidebar.markdown("Error obtaining recommendation")

if query := st.chat_input(
    "Enter a question you have from your English literature coursework."
):
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    previous_responses_list = [
        msg["content"] for msg in st.session_state.messages if msg["role"] == "ai"
    ]

    previous_responses = tuple(previous_responses_list)

    response_data = {
        "course": course,
        "query": query,
        "previous_responses": previous_responses,
    }

    response = requests.post(RESPONSE_URL, json=response_data)

    with st.chat_message("ai"):
        if response.status_code == 200:
            response_text = response.json()
            st.markdown(response_text)
            st.session_state.messages.append({"role": "ai", "content": response_text})
        else:
            st.markdown("The application was unable to send your query.")