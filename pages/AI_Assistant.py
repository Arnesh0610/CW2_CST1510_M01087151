#Import necessary modules
import streamlit as st
from data.incidents import get_all_incidents
from data.tickets import get_all_tickets
from data.datasets import get_all_datasets
from data.db import connect_database
from google import genai

#Check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    # Stop execution
    st.stop()
else:
    #Configure Streamlit page
    st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
    )
    #Initialize Gemini client using API key from Streamlit secrets
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    #Connect to database
    conn = connect_database()

    #Fetching data from database
    incidents = get_all_incidents()
    tickets = get_all_tickets(conn)
    datasets = get_all_datasets(conn)
    
    #Close connection
    conn.close()

    #Initialize AI assistant configurations if not in session
    if "ai_data" not in st.session_state:
        st.session_state.ai_data = {
        0: { #Cyber incidents assistant configuration
            "title": "🤖 Cyber Incidents Assistant",
            "system_prompt": f"""
           You are given the table of all incidents:
           {incidents.to_string()}

            You are a cybersecurity expert assistant.
            - Analyze incidents and threats
            - Explain attack vectors & mitigations
            - Use MITRE ATTACK and CVE terminology
            - Give actionable recommendations
            """,
            "history": []
            },
        1: { #IT tickets assistant configuration
            "title": "🤖 IT Tickets Assistant",
            "system_prompt": f"""
           You are given the table of all tickets:
           {tickets.to_string()}

            You are an IT Operation expert assistant.
            - Ticket triage & prioritization
            - Troubleshooting guidance
            - Infrastructure best practices
            """,
            "history": []
            },
        2: {  #Datasets assistant configuration
            "title": "🤖 Datasets Metadata Assistant",
            "system_prompt": f"""
           You are given the table of all datasets:
           {datasets.to_string()}

            You are a Data Science expert assistant.
            - Dataset analysis & insights
            - Visualization recommendations
            - ML technique suggestions
            """,
            "history": []
            }
           }

    if "ai_index" not in st.session_state:
        st.session_state.ai_index = None

    #Creating three buttons for assistant selection
    col1, col2, col3 = st.columns(3)

    if col1.button("Cyber Incidents Assistant"):
        st.session_state.ai_index = 0
        st.rerun()

    if col2.button("IT Tickets Assistant"):
        st.session_state.ai_index = 1
        st.rerun()

    if col3.button("Datasets Metadata Assistant"):
        st.session_state.ai_index = 2
        st.rerun()

    if st.session_state.ai_index is None:
        st.info("Choose one AI assistant")
        st.stop()

    assistant = st.session_state.ai_data[st.session_state.ai_index]
    st.title(assistant["title"])

    #Display chat history
    for msg in assistant["history"]:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["text"])

    prompt = st.chat_input("Ask anything.")

    if prompt:
        # Show user message
        with st.chat_message("user"):
            st.markdown(prompt)

        assistant["history"].append({"role": "user", "text": prompt})

        #Build Gemini-compatible conversation
        contents = [
         {
        "role": "user",  # system prompt is treated as a user message
        "parts": [{"text": assistant["system_prompt"]}]
        }
        ]
        #
        for msg in assistant["history"]:
            if msg["role"] == "user":
                contents.append({"role": "user", "parts": [{"text": msg["text"]}]})
            else:
                contents.append({"role": "model", "parts": [{"text": msg["text"]}]})

        try:
            #Stream Gemini response
            stream = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=contents
           )
            
            reply = ""
            for chunk in stream:
                if chunk.text:
                    reply += chunk.text
        except Exception as e:
            reply = f"AI service is not available.:{e}"

        # Show AI reply
        with st.chat_message("assistant"):
            st.markdown(reply)

        assistant["history"].append({"role": "assistant", "text": reply})

    if st.button("Clear Conversation"):
        assistant["history"].clear()
        st.rerun()

# 
models = client.models.list()
for m in models:
    print(m.name)