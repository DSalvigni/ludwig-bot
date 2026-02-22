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

# --- LOGIN PAGE ---
def login():
    # Usiamo container e colonne per centrare perfettamente
    _, col2, _ = st.columns([1, 2, 1])
    
    with col2:
        # Nota: Ho tolto st.title fuori dal box per evitare lo spazio vuoto
        st.markdown("""
            <div style="background-color: #262730; padding: 2rem; border-radius: 15px; border: 1px solid #464b5d; margin-top: 50px;">
                <h2 style="text-align: center; color: white; margin-bottom: 1.5rem;">Welcome to Ludwig RAG bot Login</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Gli input devono stare fuori dal blocco HTML sopra per funzionare con Streamlit
        user = st.text_input("Username", key="user_input")
        pwd = st.text_input("Password", type="password", key="pwd_input")
        
        if st.button("Login"):
            if user == "user" and pwd == "user":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid credentials")

if not st.session_state['logged_in']:
    login()
    st.stop()

# --- RAG LOGIC ---
@st.cache_resource
@st.cache_resource
def init_rag():
    embeddings = OllamaEmbeddings(model=MODEL, base_url=OLLAMA_URL)
    
    # Debug: Controllo se la cartella esiste
    if not os.path.exists(DOCS_PATH):
        print(f"DEBUG: Cartella {DOCS_PATH} non trovata. La creo.")
        os.makedirs(DOCS_PATH)

    # Debug: Lista i file trovati
    files = os.listdir(DOCS_PATH)
    print(f"DEBUG: File trovati in {DOCS_PATH}: {files}", flush=True)

    if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
        print(f"DEBUG: Database esistente trovato in {DB_PATH}. Caricamento...")
        return Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    
    print("DEBUG: Database non trovato. Inizio indicizzazione documenti...")
    
    pdf_loader = DirectoryLoader(DOCS_PATH, glob="./*.pdf", loader_cls=PyPDFLoader, silent_errors=True)
    txt_loader = DirectoryLoader(DOCS_PATH, glob="./*.txt", loader_cls=TextLoader)
    
    docs = pdf_loader.load() + txt_loader.load()
    
    if docs:
        print(f"DEBUG: Caricati {len(docs)} documenti.")
        for d in docs:
            print(f"DEBUG: Indicizzato file -> {d.metadata.get('source')}")
            
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = splitter.split_documents(docs)
        
        vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=embeddings, 
            persist_directory=DB_PATH
        )
        print("DEBUG: Database creato con successo!")
        return vectorstore
    else:
        print("DEBUG: ATTENZIONE! Nessun documento trovato. Ludwig risponderà senza contesto.")
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