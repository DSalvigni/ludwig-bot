import ollama

def chat():
    client = ollama.Client(host='http://127.0.0.1:11434')
    
    # Personalità cinica e spaziale
    SYSTEM_PROMPT = "Sei un ingegnere spaziale geniale e cinico. Rispondi in modo diretto e brutale. Parla Italiano e Inglese."

    print("\n--- BOT LEGGERO ATTIVO (Llama 3.2 1B) ---")
    while True:
        try:
            user_input = input("TU > ")
            if user_input.lower() in ['exit', 'quit']: break
            
            # USIAMO IL MODELLO DA 1B (molto più leggero)
            response = client.chat(
                model='llama3.2:1b', 
                messages=[
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': user_input},
                ]
            )
            print(f"\nBOT > {response['message']['content']}\n")
        except Exception as e:
            print(f"Errore: {e}")
            break

if __name__ == "__main__":
    chat()