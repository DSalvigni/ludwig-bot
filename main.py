import ollama
import os

# Il System Prompt per la personalità "deviata"
SYSTEM_PROMPT = """
Sei un ingegnere aerospaziale cinico e geniale. 
Rispondi in modo diretto, brutale e senza filtri di cortesia. 
Se il codice fa schifo, dillo. Parla italiano e inglese.
Usa i dati sullo spazio per risolvere problemi complessi.
"""

def chat():
    print("--- BOT SPAZIALE OFFLINE ATTIVO (Scrivi 'exit' per uscire) ---")
    while True:
        user_input = input("Tu: ")
        if user_input.lower() == 'exit':
            break
        
        response = ollama.chat(model='llama3.1', messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_input},
        ])
        
        print(f"\nBot: {response['message']['content']}\n")

if __name__ == "__main__":
    chat()