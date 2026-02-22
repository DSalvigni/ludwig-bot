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

## 📝 Latest Updates
* **Reset Section:** Added clear instructions on how to "wipe" Ludwig's memory by deleting the `chroma_db` folder.
* **3-Step Procedure:** Provided a step-by-step guide to resetting the vector database and forcing a re-index.
* **Technical Detail:** Defined the `documenti_spazio` folder as the "primary knowledge source" for the RAG engine.

---

## 🚀 Getting Started

```bash
### 1. Clone the repository
git clone git@github.com:DSalvigni/ludwig-bot.git
cd ludwig-bot

### 2. Prepare Knowledge Base
Place your technical documents (PDF or TXT) inside the `documenti_spazio/` folder. Ludwig will automatically index these files on the next launch.

### 3. Build and Start the Containers
Run the following command to build the custom Streamlit image and start the services in detached mode:

```bash
docker compose up -d --build

### 4. View Live Debug Logs
In consolle run the following command
```bash
docker logs -f ludwig

### 5. Force Database Refresh (Full Reset)
```bash
# 1. Stop services
docker compose down

# 2. Delete the old vector database folder
rm -rf chroma_db

# 3. Restart and re-index
docker compose up -d


---
*Copyright © 2026 by Daniele S.*