import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_v2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")



promt = ChatPromptTemplate(
    [
        ("system","You are helpfull assistand.give the appropriate answers for the following question."),
        ("user","question{question}"),
    ]
)

def generate_response(question,api_key,llm,temperature,max_tokens):
    parser = StrOutputParser()
    llm = ChatGroq(model=llm, groq_api_key=api_key)
    chain = promt | llm | parser
    response = chain.invoke({"question":question})
    return response

## #Title of the app
st.title("Enhanced Q&A Chatbot With GroqAPI")



## Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Groq API Key:",type="password")

## Select the OpenAI model
engine=st.sidebar.selectbox("Select the model",["deepseek-r1-distill-llama-70b","Gemma2-9b-It"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

## MAin interface for user input
st.write("Goe ahead and ask any question")
user_input=st.text_input("You:")

if user_input and api_key:
    response=generate_response(user_input,api_key,engine,temperature,max_tokens)
    st.write(response)

elif user_input:
    st.warning("Please enter the OPen AI aPi Key in the sider bar")
else:
    st.write("Please provide the user input")
