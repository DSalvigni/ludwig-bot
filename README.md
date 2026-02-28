# Ludwig Bot 🤖
**"A simple RAG bot based on Ollama & Llama"**

Ludwig Bot is a specialized AI assistant designed for technical document analysis, specifically optimized for space engineering or anz generic training can be provided via txt files, infact It uses a Retrieval-Augmented Generation (RAG) engine to process local documents privately and securely within a Dockerized environment.

Built by **Daniele S. - 2026**

---

## 🛠️ Technical Stack
* **LLM Engine:** [Ollama](https://ollama.com/) (Running `llama3.2:1b` locally).
* **RAG Framework:** [LangChain](https://www.langchain.com/).
* **Vector Database:** [ChromaDB](https://www.trychroma.com/) (Persistent local storage).
* **UI/Interface:** [Streamlit](https://streamlit.io/) with "Gemini-style" custom CSS and custom sidebar branding.
* **Logging System:** Python `logging` module with dual-output (Console + Rotating `.log` files).
* **Deployment:** Docker & Docker Compose with persistent volumes.

---

## ✨ Key Features
* **Bilingual Intelligence:** Automatically detects and responds in the user's language (English or Italian).
* **Source Citations:** Every response includes references to the specific files (e.g., `Sources: training.txt`) used for context. In the following repo I setup 2 files (test and test_02) to train the model about PMS content and Cakes. This will instruct the bot about these 2 contest. No "Railguards" have been setup.
* **Branded Interface:** Sidebar featuring the **Ludwig Bot** logo and technical subtitles.
* **Advanced Logging:** All operations are tracked in `./logs/log_YYYYMMDD_HHMMSS.log` for audit and debugging.
* **Secure Access:** Integrated credential-based login system (Default: `user / user`).

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone git@github.com:DSalvigni/ludwig-bot.git
cd ludwig-bot
```

### 2. Prepare & Enrich Knowledge Base
```bash
Place your technical documents (PDF or TXT) inside the documenti_spazio/ folder.
To enrich your knowledge and enable precise referencing, use numerical markers:

    Example in training.txt:
    [1] The PMS unit handles payload telemetry. [2] LEO orbit is below 2000km. etc..
```

### 3. Build and Start the Containers
```bash
Run the following command to build the environment and start services:
Bash

    docker compose up -d --build
```

### 4. Pull the AI Model
```bash
Initialize the local LLM inside the Ollama container:

    docker exec -it ollama ollama pull llama3.2:1b
```

### 5. Open the Interface
```bash
Access the bot through your browser at:

    👉 http://localhost:8501

```

### 6. 🛠️ Maintenance & Debugging 🛠️
```bash
Monitoring Live Logs

To see exactly what Ludwig is doing (indexing progress, query retrieval, system status):

    Terminal (Live): docker logs -f ludwig

    Log Files: Check the ./logs/ directory for time-stamped files: log_20260228_123000.log.
```

### 7. Force Database Refresh (Full Reset)
```bash
If you update your documents and want Ludwig to re-index everything from scratch:

# 1. Stop services
docker compose down

# 2. Delete the old vector database folder
rm -rf chroma_db

# 3. Restart and re-index
docker compose up -d
```

INFO ABOUT VOLUME:
Docker Volume Mapping

The docker-compose.yaml is configured to persist data and logs:

    ./ollama_data: Stores the AI models.

    ./chroma_db: Stores the vector knowledge.

    ./logs: Stores the execution history for audit and debugging.

Copyright © 2026 by Daniele S.


---

### Un piccolo check finale per te:
The following structure must be followed
```text
ludwig-bot/
├── space_document/ (here files for training with the format tranining_01.txt, .._02.txt etc...)
├── logs/             (self created)
├── chroma_db/        (self created)
├── main.py
├── Dockerfile
├── docker-compose.yaml
└── README.md