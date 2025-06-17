import streamlit as st
import os
import base64
import tempfile
import io
from dotenv import load_dotenv
from textwrap import wrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from google import genai

load_dotenv()

VECTORSTORE_PATH = "vectorstore.index"
BACKGROUND_IMAGE_PATH = "background.png"

def set_background(image_path):
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def get_vectorstore(text_chunks, existing_vectorstore=None):
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-large")
    if existing_vectorstore:
        existing_vectorstore.add_texts([text_chunks])
        existing_vectorstore.save_local(VECTORSTORE_PATH)
        return existing_vectorstore
    else:
        vectorstore = FAISS.from_texts(texts=[text_chunks], embedding=embeddings)
        vectorstore.save_local(VECTORSTORE_PATH)
        return vectorstore

def load_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-large")
        return FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
    return None

def generate_pdf_report(text):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    left_margin = 50
    right_margin = 550
    wrapped_text = []
    for line in text.split("\n"):
        wrapped_text.extend(wrap(line, width=80))
    y_position = 750
    for line in wrapped_text:
        pdf.drawString(left_margin, y_position, line)
        y_position -= 20
        if y_position < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y_position = 750
    pdf.save()
    buffer.seek(0)
    return buffer

set_background(BACKGROUND_IMAGE_PATH)

st.markdown("<h1 style='text-align: center;'>CaseLink</h1>", unsafe_allow_html=True)

video_file = st.file_uploader("Upload a video to generate a report", type=["mp4", "avi", "mov", "mkv"])

if video_file is not None:
    st.video(video_file)

if video_file is not None:
    if st.button("Generate Report", use_container_width=True):
        st.warning("Processing... Please wait.")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(video_file.read())
            temp_file_path = temp_file.name
        try:
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            uploaded_file = client.files.upload(file=temp_file_path)
            prompt = """
            You are analyzing a full video. Provide the following details:

            1. Incident Overview: Describe what happened, environmental conditions (e.g., lighting, weather).
            2. Suspects: Provide details on their appearance, actions, and any distinguishing features.
            3. Victims/Witnesses: If visible, describe them, including their actions.
            4. Vehicles: Describe any vehicles, license plates, and their interaction with the crime scene.
            5. Affected Items: Describe items impacted during the incident (e.g., ATM, its condition before and after).
            6. Suspicious Activities: Identify illegal activities and summarize the sequence of events.
            7. Conversations/Sounds: Analyze any audible conversations or sounds relevant to the crime scene.
            8. Additional Details: Mention any visible landmarks, signboards, or other context about the scene.

            Summarize all information and generate a comprehensive report for the police investigation.
            """
            response = client.models.generate_content(model="gemini-2.0-flash", contents=[uploaded_file, prompt])
            if hasattr(response, 'text'):
                response_text = response.text
                existing_vectorstore = load_vectorstore()
                vectorstore = get_vectorstore(response_text, existing_vectorstore)
                st.session_state.vectorstore = vectorstore
                st.subheader("Generated Report:")
                st.write(response_text)
                pdf_buffer = generate_pdf_report(response_text)
                st.download_button(
                    label="Download Report (PDF)",
                    data=pdf_buffer,
                    file_name="Crime_Report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Failed to generate report. Please try again.")
        except Exception as e:
            st.error(f"Error encountered: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
elif video_file is None:
    st.warning("Please upload a video file.")
