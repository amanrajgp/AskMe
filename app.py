import time
import io
import pytesseract as tess
from PIL import Image
import streamlit as st
import google.generativeai as genai
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.output_parser import StrOutputParser
import asyncio

# Configure Google Generative AI
google_api_key = "AIzaSyBoxsa2ARTumKvRL5wLEfRoKm4Xc6zoKq0"
# genai.configure(api_key=google_api_key)

# Setup the Tesseract executable path
tess.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Create the Google Generative AI model
# Note: Ensure this uses a synchronous approach


# Define the main function


def main():
    st.title("AskMe")

    question = st.text_input("Ask Question:")
    img_file_buffer = st.camera_input("Take a picture")

    def gettext(img_file_buffer):
        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            img = Image.open(io.BytesIO(bytes_data))  # Convert bytes to PIL Image
            text = tess.image_to_string(img)
            return text
        else:
            return None 

    async def generate_response(text, question):

        prompt = ChatPromptTemplate.from_template("""
            <s>[INSTRUCT]
            Role: As a contract generation specialist, your primary function is to analyze the provided Text {text} and answer the question {question} given by user.

            **Additional Instructions:**
            *Give answer in details as much as possible.

            **Internet Use:**
            *You may fetch information from the internet related to question to ensure relevance.

            **Important**
            * Do not provide any information if you are not able to find.
            [/INSTRUCT]</s>
        """)
        model = ChatGoogleGenerativeAI(
            model="gemini-pro", temperature=0.8, google_api_key=google_api_key)
        output_parser = StrOutputParser()
        chain = prompt | model | output_parser

        response = chain.invoke({"text": text, "question": question})
        return response

    if st.button("Go"):

        if question and img_file_buffer:
            st.success("Generating...")
            text = gettext(img_file_buffer)

            # Run the asynchronous function and wait for the result
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                generate_response(text, question))

            st.write("**Generated Response:**")
            st.write(response)
        else:
            st.error("Please provide both a question and an image.")


# Run the main function
if __name__ == "__main__":
    main()
