# Ludwig Bot 🤖
**"A simple RAG bot"**

Ludwig is a specialized AI assistant designed to analyze technical documents (such as ESA/ECSS standards) with a unique personality: a brilliant but cynical space engineer. Named in honor of the physicist **Ludwig Boltzmann**, this bot doesn't just provide answers—it provides them with an attitude.

Built by **Daniele S.**

---

## 🛠️ Technical Stack
* **LLM Engine:** [Ollama](https://ollama.com/) (Running `llama3.2:1b` locally).
* **Orchestrator/RAG:** [LangChain](https://www.langchain.com/) (Python).
* **Vector Database:** [ChromaDB](https://www.trychroma.com/) (Local persistent storage).
* **UI/Interface:** [Streamlit](https://streamlit.io/) (Web-based chat interface with custom CSS).
* **Deployment:** Docker & Docker Compose.

## ✨ Key Features
* **Web-Based UI:** Accessible via browser with a sleek, centered login interface and rounded design. Basic user "user/user" for basic login.
* **RAG (Retrieval-Augmented Generation):** Automatically indexes PDF and TXT documents from the source folder.
* **Persistent Memory:** Vector embeddings are saved locally in `chroma_db`, avoiding re-indexing at every launch.
* **Bilingual & Cynical:** Responds in English with a sharp, engineering-focused wit.
* **Secure Access:** Integrated credential-based login system.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone