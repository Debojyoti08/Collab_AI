from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import speech_recognition as sr

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
st.set_page_config(page_title="Q&A Demo with Voice Input")
st.header("🎤 Chatbot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Add a radio button to select between Text or Voice input
input_mode = st.radio("Choose input method:", ["Text", "Voice"])

# Function for voice-to-text conversion
def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening for your question...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen to the microphone
        try:
            st.write("⏳ Processing your voice input...")
            text = recognizer.recognize_google(audio)  # Use Google Web Speech API for recognition
            st.write(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError as e:
            st.write(f"Error with Speech Recognition service: {e}")
            return None

# User input for the question based on the selected input mode
if input_mode == "Text":
    user_input = st.text_input("Input your question:", key="input")
    submit_button = st.button("Ask the question")

    if submit_button and user_input:
        # Get response from Gemini model
        response = get_gemini_response(user_input)
        
        # Add user query to session history
        st.session_state['chat_history'].append(("You", user_input))
        
        st.subheader("The Response is")
        # Display response chunks
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

elif input_mode == "Voice":
    if st.button("Start Voice Recognition"):
        recognized_text = recognize_voice()  # Capture voice and convert to text
        
        if recognized_text:
            # Get response from Gemini model
            response = get_gemini_response(recognized_text)
            
            # Add user query to session history
            st.session_state['chat_history'].append(("You (Voice)", recognized_text))
            
            st.subheader("The Response is")
            # Display response chunks
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
st.subheader("🗂️ Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
