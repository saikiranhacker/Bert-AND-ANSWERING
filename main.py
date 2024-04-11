import streamlit as st
import requests
from bs4 import BeautifulSoup
from read_files import document_reader
import os

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract text from all paragraphs in the webpage
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

def file_uploader():
    uploaded_file = st.sidebar.file_uploader('Prefer .txt file')
    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)
        text = document_reader('docs')        
        return text

def save_uploaded_file(uploadedfile):
    with open(os.path.join("docs", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

st.sidebar.title('BERT Question-Answering System by Sai') 

option = st.sidebar.selectbox(
    'Select input type',
    ['Webpage URL', 'Upload Document', 'Copy paste document']
)

if option == 'Webpage URL':
    url = st.text_input(label='Enter the URL of the webpage')
    if url:
        document = extract_text_from_url(url)
        st.text_area("document", value=document, height=60, max_chars=None, key=None)

elif option == 'Upload Document':
    document = file_uploader()
    st.text_area("document", value=document, height=60, max_chars=None, key=None)
    files = os.listdir('docs')
    for f in files:
        try:
            os.remove(os.path.join('docs', f))
        except:
            pass

elif option == 'Copy paste document':
    document = st.text_area(label='Paste your text')

task = st.sidebar.selectbox(
    'Select option',
    ['None', 'Question Answering', 'Text Summarization']
)

if task == 'Question Answering':
    question = st.text_area(label='Write your Question')

    QA_input = {
        'question': question,
        'context': document
    }

    import transformers
    from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

    model_name = "distilbert-base-uncased-distilled-squad"
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    res = nlp(QA_input)
    st.write(f"Answer: {res['answer']}")
