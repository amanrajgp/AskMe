################################### Working Code ###############################################
import time
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
# Ensure pytesseract can find the tesseract executable
# This step might not be necessary on Streamlit Cloud if tesseract is correctly installed and in the PATH
tess.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
# Create the Google Generative AI model
# Note: Ensure this uses a synchronous approach
def main():
    st.markdown(
        """
        <style>
        .header-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .name-header {
            font-family: 'Raleway', sans-serif;
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-top: 20px;
        }
        .subheader {
            font-family: 'Raleway', sans-serif;
            font-size: 20px;
            color: white;
            text-align: center;
            margin-bottom: 20px;
        }
        .subsubheader {
            font-family: 'Raleway', sans-serif;
            font-size: 15px;
            color: #555;
            text-align: center;
            margin-bottom: 20px;
        }
        
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@700&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True)
        
    st.title("AskMe")
    info_expander = st.expander("About")
    with info_expander:
        st.markdown('''
        AskMe is Your personal knowledge assistant powered by GenAI. 
        Upload image,ask questions, and receive insightful answers instantly!
        ''')
    image_path = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    question = st.text_input("Ask Question:")

    
    def gettext(image_path):
        try:
            img = Image.open(image_path)
            
            text = tess.image_to_string(img)
            return text
        except tess.TesseractNotFoundError:
            st.error("Tesseract OCR is not installed or found.")
            return ""
    async def generate_response(text, question):
        prompt = ChatPromptTemplate.from_template("""
            <s>[INSTRUCT]
            Role: As a knowledge expert, your primary function is to analyze the provided Text {text} and answer the question {question} given by user.
  
            **Additional Instructions:**
            *Give answer in details as much as possible.
            **Internet Use:**
            *You may fetch information from the internet related to question to ensure relevance.
            **Important**
            * Do not provide any information if you are not able to find.
            [/INSTRUCT]</s>
        """)
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.8, google_api_key=google_api_key)
        output_parser = StrOutputParser()
        chain = prompt | model | output_parser
        response = chain.invoke({"text": text, "question": question})
        return response

    if st.button("Go"):
        if question and image_path:
            progress_bar=st.progress(0)
            text = gettext(image_path)
            progress_bar.progress(30)
            if text:
                # Run the asynchronous function and wait for the result
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                progress_bar.progress(70)
                response = loop.run_until_complete(generate_response(text, question))
                progress_bar.progress(100)
                st.write("**Generated Response:**")
                st.write(response)
            else:

    
          
            
    

          
       
    
    
  
                st.error("Failed to extract text from the image.")
        else:
            st.error("Please provide both a question and an image.")

    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.markdown('<div class="subsubheader">Developed by</div>', unsafe_allow_html=True)
    st.markdown('<div class="name-header">Aman Raj</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Data Scientist</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
# Run the main function
if __name__ == "__main__":
    main()
