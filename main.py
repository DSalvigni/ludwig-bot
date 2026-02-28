import streamlit as st
import ollama
import os
import logging
import re
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# --- CONFIGURATION & LOGGING ---
MODEL = "llama3.2:1b"
DOCS_PATH = "./space_document"
DB_PATH = "./chroma_db"
LOG_DIR = "./logs"
IMG_PATH = "./img/missile.png" 
OLLAMA_URL = "http://ollama:11434"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_filename = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_filename), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Ludwig Bot", layout="wide")

# --- CSS GEMINI STYLE FOR LOOK & FEEL ---
st.markdown("""
    <style>
    .stAppDeployButton {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stChatMessage { border-radius: 20px; padding: 15px; margin-bottom: 10px; }
    [data-testid="stChatMessageUser"] { background-color: #2b2c2e !important; border: 1px solid #444; }
    [data-testid="stChatMessageAssistant"] { background-color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.header("Ludwig Bot Portal")
            st.markdown("Please enter your credentials to access the RAG engine.")
            user = st.text_input("Username", placeholder="e.g. admin")
            pwd = st.text_input("Password", type="password")
            if st.button("Sign In"):
                if user == "user" and pwd == "user":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Access Denied")

if not st.session_state['logged_in']:
    login()
    st.stop()

# --- RAG ENGINE ---
@st.cache_resource
def init_rag():
    logger.info("🚀 Initializing RAG Engine...")
    embeddings = OllamaEmbeddings(model=MODEL, base_url=OLLAMA_URL)
    
    # If db exists, we load it. Otherwise, we build it from the documents. This allows us to keep the db persistent across runs and only re-index if we change the docs.
    if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
        logger.info(f"📂 Loading existing database from {DB_PATH}")
        return Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    
    logger.info("🆕 Database not found or wiped. Starting fresh indexing...")
    
    # We upload TXT or PDF. TXT formatted like the ones available in this sample (including training_00, training_01, ecc.)
    pdf_loader = DirectoryLoader(DOCS_PATH, glob="./*.pdf", loader_cls=PyPDFLoader)
    txt_loader = DirectoryLoader(DOCS_PATH, glob="./*.txt", loader_cls=TextLoader)
    
    docs = pdf_loader.load() + txt_loader.load()
    
    if not docs:
        logger.error(f"⚠️ No documents found in {DOCS_PATH}! Check your files.")
        return None
        
    # LOG TO FILES DETECTED
    file_names = list(set([os.path.basename(d.metadata.get('source', 'Unknown')) for d in docs]))
    logger.info(f"📄 FILES DETECTED: {file_names}")

    # We increase chunk size to 1000 and overlap to 150 to create more meaningful chunks that can capture entire sections or paragraphs, while still allowing for some context overlap between them. We also add separators to try to break on double newlines first, which often indicate new sections or paragraphs, helping to preserve the structure of the documents and potentially improving the relevance of retrieved chunks during similarity search.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""] # Try to split on double newlines first, then single newlines, then spaces, and as a last resort, split anywhere if the chunk is too long. This helps preserve the natural structure of the text and can lead to more coherent chunks.
    )
    
    splits = splitter.split_documents(docs)
    logger.info(f"✂️ Created {len(splits)} text chunks from {len(docs)} files.")
    
    # Generation of vectors and persistence in ChromaDB. This is the most time-consuming step, especially with larger documents and more chunks, so we log it accordingly.
    logger.info("🧠 Generating embeddings (this might take a while)...")
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=DB_PATH
    )
    
    logger.info("✅ Database build complete and persisted locally.")
    return vectorstore

vectorstore = init_rag()

# --- SIDEBAR ---
st.sidebar.title("Ludwig Bot")

if os.path.exists(IMG_PATH):
    st.sidebar.image(IMG_PATH, use_container_width=True)

if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()

# --- CHAT ---
st.title("Ludwig Bot")
st.subheader("A simple RAG bot based on Ollama & llama3.2:1b")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    context_parts = []
    formatted_sources = set()
    
    if vectorstore:
        # K is set to 5 to retrieve the top 5 most relevant chunks, which should provide a good balance between relevance and breadth of context for the model to generate a comprehensive answer. Depending on the size and quality of your documents, you might want to adjust this number up or down.
        results = vectorstore.similarity_search(prompt, k=5) 
        for res in results:
            context_parts.append(res.page_content)
            
            raw_source = os.path.basename(res.metadata.get('source', 'Unknown'))
            file_name = os.path.splitext(raw_source)[0]
            
            match = re.search(r'\[(\d+)\]', res.page_content)
            ref_num = match.group(1) if match else "?"
            
            formatted_sources.add(f"[{file_name} - [{ref_num}]]")
    
    context = "\n\n".join(context_parts)
    source_footer = " ".join(list(formatted_sources))

    system_instruction = (
        "You are Ludwig Bot, a helpful technical assistant. "
        "Use the provided context to answer. Detect the language and respond accordingly."
    )
    
    full_prompt = f"{system_instruction}\n\nContext: {context}\n\nQuestion: {prompt}"

    with st.chat_message("assistant"):
        response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': full_prompt}])
        answer = response['message']['content']
        
        # Adding references to the answer if we have formatted sources. This provides transparency about where the information is coming from and allows users to trace back the answer to the original documents, which can be especially important for technical or factual queries.
        if formatted_sources:
            answer += f"\n\n**References:** {source_footer}"
            
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("---")
st.markdown("<p style='text-align: center; opacity: 0.5;'>© 2026 Ludwig Bot Project by Daniele S.</p>", unsafe_allow_html=True)