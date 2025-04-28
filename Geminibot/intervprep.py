import streamlit as st
import os
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import random
import re
import pandas as pd
import time
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

# Setup NLTK
nltk.download("punkt")
nltk.download("vader_lexicon")

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro-001")
chat = model.start_chat(history=[])

# Filler word-based clarity evaluation
def evaluate_clarity(transcript):
    FILLER_WORDS = {"uh", "um", "like", "you know", "actually", "basically", "so", "I mean"}
    words = word_tokenize(transcript.lower())
    sentences = sent_tokenize(transcript)

    total_words = len(words)
    filler_count = sum(words.count(filler) for filler in FILLER_WORDS)
    sentence_count = len(sentences)

    filler_penalty = min(filler_count / max(total_words, 1), 1)
    fluency_bonus = min(sentence_count / max((total_words / 20), 1), 1)

    clarity_score = max(0, 5 * (1 - filler_penalty)) * fluency_bonus
    clarity_score = round(min(clarity_score, 5), 2)

    return {
        "word_count": total_words,
        "filler_count": filler_count,
        "sentence_count": sentence_count,
        "clarity_score": clarity_score,
    }

def get_gemini_response(prompt):
    try:
        response = chat.send_message(prompt, stream=True)
        return response
    except Exception as e:
        st.error(f"Error getting response from Gemini: {e}")
        return []

# UPDATED recognize_voice function
def recognize_voice():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.0  # Short pause between words/phrases
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.5

    with sr.Microphone() as source:
        st.write("🎤 Listening... (Auto-stops after 5 seconds of silence at the end OR after 10 minutes)")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=600)
            st.success("🛑 Recording stopped. Now transcribing...")

            # After capturing, simulate extra 5-sec pause handling
            st.info(" ⌛ ⌛ ⌛ ")
            time.sleep(5)

            with st.spinner("🧠 Transcribing..."):
                text = recognizer.recognize_google(audio)
            st.write(f"Recognized Text: {text}")
            return text

        except sr.WaitTimeoutError:
            st.error("⏳ No speech detected. Please try again.")
        except sr.UnknownValueError:
            st.error("🤔 Could not understand audio. Try again.")
        except sr.RequestError as e:
            st.error(f"🔌 API error: {e}")

        return None

@st.cache_data
def load_questions(role):
    df = pd.read_csv(f"questions/{role.replace(' ', '_').lower()}_questions.csv")
    return df["question"].dropna().tolist()

# Streamlit App
st.set_page_config(page_title="Gemini AI App")
st.header("🧑‍💼 AI Interview Preparation")

roles = ["Software Engineer", "Data Analyst", "Project Manager", "HR Executive"]
role = st.selectbox("Select Interview Role:", roles)
input_mode = st.radio("Choose answer mode:", ["Text", "Voice"])

if f"interview_{role}_questions" not in st.session_state:
    questions = load_questions(role)
    st.session_state[f"interview_{role}_questions"] = random.sample(questions, len(questions))
    st.session_state[f"interview_{role}_index"] = 0
    st.session_state[f"interview_{role}_score"] = 0
    st.session_state[f"interview_{role}_feedback"] = []
    st.session_state[f"interview_{role}_timing"] = []
    st.session_state.voice_inputs = []

questions = st.session_state[f"interview_{role}_questions"]
index = st.session_state[f"interview_{role}_index"]

st.progress(index / len(questions))

if index < len(questions):
    current_question = questions[index]
    st.write(current_question)

    if f"start_time_{index}" not in st.session_state:
        st.session_state[f"start_time_{index}"] = time.time()

    start_time = st.session_state[f"start_time_{index}"]

    user_answer = ""
    if input_mode == "Text":
        user_answer = st.text_area("Your answer:", key=f"text_input_{index}")
    else:
        if st.button("🎙️ Record Answer"):
            user_answer = recognize_voice()
            if user_answer:
                st.session_state.voice_inputs.append(user_answer)
                st.session_state.voice_input = user_answer
        user_answer = st.session_state.get("voice_input", "")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("📤 Submit Answer") and user_answer:
            time_taken = time.time() - start_time

            eval_prompt = f"""
            You are a professional technical interviewer.

            Evaluate the following candidate's answer:
            Question: {current_question}
            Answer: {user_answer}

            Give:
            1. Score out of 10.
            2. Technical correctness feedback.
            3. Clarity and communication feedback.
            4. Suggestions for improvement.
            """
            with st.spinner("💬 Evaluating your answer..."):
                response = get_gemini_response(eval_prompt)

                response_text = ""
                for chunk in response:
                    if hasattr(chunk, "parts") and chunk.parts:
                        for part in chunk.parts:
                            response_text += part.text

            match = re.search(r"(?i)score\D*(\d+(\.\d+)?)", response_text)
            score = float(match.group(1)) if match else 0

            st.session_state[f"interview_{role}_score"] += score
            st.session_state[f"interview_{role}_feedback"].append((current_question, user_answer, response_text))
            st.session_state[f"interview_{role}_timing"].append(round(time_taken, 2))

            st.success("Answer submitted! Proceed to next question or click 'Submit and View Scores'.")
            st.session_state[f"interview_{role}_index"] += 1
            st.session_state.voice_input = ""
            st.rerun()

    with col2:
        if st.button("➡️ Skip Question"):
            st.session_state[f"interview_{role}_index"] += 1
            st.rerun()

    with col3:
        if st.button("✅ Submit and View Scores"):
            if user_answer:
                time_taken = time.time() - start_time
                eval_prompt = f"""
                You are a professional technical interviewer.

                Evaluate the following candidate's answer:
                Question: {current_question}
                Answer: {user_answer}

                Give:
                1. Score out of 10.
                2. Technical correctness feedback.
                3. Clarity and communication feedback.
                4. Suggestions for improvement.
                """
                with st.spinner("💬 Evaluating your answer..."):
                    response = get_gemini_response(eval_prompt)

                    response_text = ""
                    for chunk in response:
                        if hasattr(chunk, "parts") and chunk.parts:
                            for part in chunk.parts:
                                response_text += part.text

                match = re.search(r"(?i)score\D*(\d+(\.\d+)?)", response_text)
                score = float(match.group(1)) if match else 0

                st.session_state[f"interview_{role}_score"] += score
                st.session_state[f"interview_{role}_feedback"].append((current_question, user_answer, response_text))
                st.session_state[f"interview_{role}_timing"].append(round(time_taken, 2))

            st.session_state[f"interview_{role}_index"] = len(questions)
            st.rerun()

else:
    st.success("✅ Interview Completed!")
    total_questions = len(st.session_state[f"interview_{role}_feedback"])
    avg_score = st.session_state[f"interview_{role}_score"] / total_questions if total_questions else 0
    st.subheader(f"📊 Final Score: {avg_score:.2f} / 10")

    # Voice Clarity Feedback
    voice_inputs = st.session_state.get("voice_inputs", [])
    if voice_inputs:
        st.subheader("🗣️ Voice Clarity Feedback")
        clarity_score_total = 0
        valid_count = 0
        for answer in voice_inputs:
            if answer.strip():
                clarity_result = evaluate_clarity(answer)
                clarity_score_total += clarity_result["clarity_score"]
                valid_count += 1
        avg_clarity_score = clarity_score_total / valid_count if valid_count else 0
        st.markdown(f"**Average Clarity Score**: 🌟 **{avg_clarity_score:.2f} / 5**")

        confidence_level = round((avg_clarity_score / 5) * 100, 2)
        st.subheader(f"🔎 Overall Confidence Level: {confidence_level:.2f}%")

        st.info("🧾 **How Clarity is Evaluated:**\n"
                "- Filler words like 'um', 'uh', 'like' reduce your clarity score.\n"
                "- Fluency is boosted when you speak in complete sentences.\n"
                "- The final clarity score is computed on a 5-point scale based on these factors.")

    # Show Feedbacks
    for i, (q, user_ans, fb) in enumerate(st.session_state[f"interview_{role}_feedback"]):
        with st.expander(f"Feedback for Q{i+1}: {q}"):
            st.markdown(fb)
            st.caption(f"⏱️ Time taken: {st.session_state[f'interview_{role}_timing'][i]} seconds")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔁 Restart Interview"):
            del st.session_state[f"interview_{role}_questions"]
            del st.session_state[f"interview_{role}_index"]
            del st.session_state[f"interview_{role}_score"]
            del st.session_state[f"interview_{role}_feedback"]
            del st.session_state[f"interview_{role}_timing"]
            st.session_state.voice_inputs = []
            st.rerun()

    with col2:
        if st.button("🔄 Load More Questions"):
            more_questions = load_questions(role)
            additional_questions = random.sample(more_questions, len(more_questions))
            st.session_state[f"interview_{role}_questions"].extend(additional_questions)
            st.rerun()

    st.caption("✨ Tip: You can switch roles above to try interview questions for other job profiles!")
