from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI with API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to initialize the Gemini Pro model and start chat
model = genai.GenerativeModel("gemini-1.5-pro-001")  # Correct model name
chat = model.start_chat(history=[])

def get_gemini_response(question):
    # Send the message to the chat session
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input for the question
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    # Get response from Gemini model
    response = get_gemini_response(input)
    
    # Add user query to session history
    st.session_state['chat_history'].append(("You", input))
    
    st.subheader("The Response is")
    # Display response chunks
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
