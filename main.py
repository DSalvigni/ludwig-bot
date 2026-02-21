import streamlit as st
import ollama
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# CONFIGURATION
MODEL = "llama3.2:1b"
DOCS_PATH = "./documenti_spazio"
DB_PATH = "./chroma_db"
OLLAMA_URL = "http://127.0.0.1:11434"

st.set_page_config(page_title="Ludwig Bot", layout="wide")

# CSS per nascondere "Deploy" e centrare il Login
st.markdown("""
    <style>
    /* Nasconde il tasto Deploy e il menu in alto a destra */
    .stAppDeployButton {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Box di Login Centrale */
    .login-box {
        background-color: #262730;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #464b5d;
        width: 350px;
        margin: auto;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    # Creiamo tre colonne per centrare il box
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.subheader("Ludwig Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == "user" and pwd == "user":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state['logged_in']:
    login()
    st.stop()

# --- RAG LOGIC ---
@st.cache_resource
def init_rag():
    embeddings = OllamaEmbeddings(model=MODEL, base_url=OLLAMA_URL)
    if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
        return Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    
    if not os.path.exists(DOCS_PATH): os.makedirs(DOCS_PATH)
    pdf_loader = DirectoryLoader(DOCS_PATH, glob="./*.pdf", loader_cls=PyPDFLoader, silent_errors=True)
    txt_loader = DirectoryLoader(DOCS_PATH, glob="./*.txt", loader_cls=TextLoader)
    docs = pdf_loader.load() + txt_loader.load()
    
    if docs:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = splitter.split_documents(docs)
        return Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=DB_PATH)
    return None

vectorstore = init_rag()

# --- INTERFACE ---
st.sidebar.markdown("# Ludwig Chatbot\n**Created By Daniele S.**")
if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()

st.title("Ludwig: A simple RAG bot")

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    context = ""
    if vectorstore:
        results = vectorstore.similarity_search(prompt, k=2)
        context = "\n".join([r.page_content for r in results])

    full_prompt = f"Context: {context}\n\nQuestion: {prompt}\nAnswer in English with a cynical tone."

    with st.chat_message("assistant"):
        response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': full_prompt}])
        answer = response['message']['content']
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# Footer Copyright
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Copyright by Daniele S.</p>", unsafe_allow_html=True)