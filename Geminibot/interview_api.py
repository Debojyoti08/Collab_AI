# filename: interview_api.py

from fastapi import FastAPI
from pydantic import BaseModel
import os
import random
import google.generativeai as genai
from dotenv import load_dotenv
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# NLTK Setup
nltk.download("punkt")
nltk.download("vader_lexicon")

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-001")
chat = model.start_chat(history=[])

# FastAPI app
app = FastAPI()

# Filler word evaluation function
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

# Load and generate interview questions using Gemini
@app.get("/questions/{role}")
def get_questions(role: str):
    # Create a prompt for generating questions based on the role
    prompt = f"Generate 5 interview questions for the role of {role}. Make sure the questions are technical and relevant to {role}."

    # Send the prompt to Gemini for question generation
    response = chat.send_message(prompt, stream=True)

    # Collect response text
    questions_text = ""
    for chunk in response:
        if hasattr(chunk, "parts") and chunk.parts:
            for part in chunk.parts:
                questions_text += part.text

    # Split the response into questions (assuming the response gives a list of questions)
    questions = questions_text.strip().split("\n")

    # Clean and return the list of questions
    questions = [q.strip() for q in questions if q.strip()]
    return {"questions": questions}

# Request Models for Answer Evaluation
class AnswerRequest(BaseModel):
    role: str
    question: str
    user_answer: str

# Request model for clarity check
class ClarityRequest(BaseModel):
    text: str

# API Endpoint for evaluating the candidate's answer
@app.post("/evaluate/")
def evaluate_answer(req: AnswerRequest):
    prompt = f"""
    You are a professional technical interviewer.

    Evaluate the following candidate's answer:
    Question: {req.question}
    Answer: {req.user_answer}

    Give:
    1. Score out of 10.
    2. Technical correctness feedback.
    3. Clarity and communication feedback.
    4. Suggestions for improvement.
    """

    response = chat.send_message(prompt, stream=True)

    response_text = ""
    for chunk in response:
        if hasattr(chunk, "parts") and chunk.parts:
            for part in chunk.parts:
                response_text += part.text

    return {"evaluation": response_text}

# API Endpoint for checking answer clarity (filler words, sentence structure)
@app.post("/clarity/")
def clarity_check(req: ClarityRequest):
    clarity = evaluate_clarity(req.text)
    return {"clarity_evaluation": clarity}

@app.get("/")
def home():
    return {"message": "Welcome to AI Interview Preparation API!"}

