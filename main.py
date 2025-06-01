from groq import Groq
import os
from dotenv import load_dotenv
import base64
import streamlit as st
from PIL import Image
import requests
import io

# Set Streamlit page config as the very first Streamlit command
st.set_page_config(
    page_title="OCR Image Analyzer",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Load variables from .env file
load_dotenv()

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "OIP.jpg"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#streamlit app title and description
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Custom CSS for a professional look
st.markdown(
    """
    <style>
    body {
        background-color: #f4f6fb;
    }
    .main {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(79,139,249,0.10);
        padding: 2.5em 2em 2em 2em;
        margin-top: 2em;
    }
    .stApp {
        background: #f4f6fb;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4F8BF9 0%, #356AC3 100%);
        color: #fff;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.7em 2.5em;
        font-size: 1.1em;
        margin-top: 1.5em;
        box-shadow: 0 2px 8px rgba(79,139,249,0.08);
        border: none;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #356AC3 0%, #4F8BF9 100%);
        color: #fff;
    }
    .stImage img {
        border-radius: 14px;
        box-shadow: 0 4px 24px rgba(79,139,249,0.10);
        margin-bottom: 1.5em;
    }
    .analysis-card {
        background: #f8fafd;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(79,139,249,0.08);
        padding: 2.5em 2em;
        margin-top: 2.5em;
        margin-bottom: 2em;
    }
    .title {
        font-size: 2.5em;
        font-weight: 800;
        color: #356AC3;
        margin-bottom: 0.2em;
        letter-spacing: -1px;
    }
    .subtitle {
        font-size: 1.2em;
        color: #4F8BF9;
        margin-bottom: 2em;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="title">OCR Image Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered image understanding</div>', unsafe_allow_html=True)
# Streamlit app to upload an image and analyze its content using Groq API

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,  use_container_width=True)

    # Convert uploaded image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    # Add a card-like container for the analysis section
    with st.container():
        st.markdown(
            """
            <style>
            .stButton>button {
                background-color: #4F8BF9;
                color: Black;
                font-weight: bold;
                border-radius: 8px;
                padding: 0.5em 2em;
                margin-top: 1em;
            }
            .stButton>button:hover {
                background-color: #356AC3;
                color: #fff;
            }
            .stImage {
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.12);
                margin-bottom: 1em;
            }
            .analysis-card {
                background: #f8fafd;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(79,139,249,0.08);
                padding: 2em 1.5em;
                margin-top: 2em;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="analysis-card"><h3 style="color:#4F8BF9;">Ready to analyze your image?</h3>'
            '<p style="color:#444;">Click the button below to get a detailed description of your image using AI.</p></div>',
            unsafe_allow_html=True,
        )
    if st.button("Analyze Image"):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What's in this image?"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                model="meta-llama/llama-4-scout-17b-16e-instruct",
            )
            st.subheader("Analysis Result")
            st.write(chat_completion.choices[0].message.content)
        except Exception as e:
            st.subheader("Analysis Result")
            st.write("Please try later")