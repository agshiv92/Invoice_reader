from dotenv import load_dotenv
import os
load_dotenv()

import streamlit as st
import os
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
from PIL import Image

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")

def get_gemini_response(question, img, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([question, img[0], prompt], stream=True)
    response.resolve()
    return response.text

st.header("Ask Question about your invoice")
input=st.text_input("Input: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image="" 

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption='Uploaded Image', use_column_width=True)

submit=st.button("Tell me about the image")


input_prompt = """You are an expert in understading invoices
                    You will receive input image as invoice &
                    You will have to answer questions based on the input image
                    Answer only specific question asked"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)


