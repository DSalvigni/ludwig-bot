# Ludwig Bot 🤖

AI model used to analyze **ESA documents**, capable of speaking in both **Italian** and **English**. 
This bot is named **Ludwig**, in honor of the great physicist **Ludwig Boltzmann**.

---

## 🛠️ Technical Stack

The project leverages the following technologies:

* **LLM Engine:** [Ollama](https://ollama.ai/) (handles the offline model).
* **Orchestrator/RAG:** [LangChain](https://www.langchain.com/) or [LlamaIndex](https://www.llamaindex.ai/) (Python).
* **Vector DB:** [ChromaDB](https://www.trychroma.com/) or [Qdrant](https://qdrant.tech/) for *Spatial RAG* (runs locally).
* **UI/Interface:** [Open WebUI](https://openwebui.com/) (ChatGPT-like experience, runs via Docker).

---

## 🚀 Getting Started

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/DSalvigni/ludwig-bot.git](https://github.com/DSalvigni/ludwig-bot.git)

2. **Docker Compose and Ollama Download:**
    docker compose up -d --build

3. **Docker exec:**
    ddocker exec -it ollama ollama pull llama3.2:1b

4. **Start to itneract:**
docker attach ludwig