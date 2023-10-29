#!/usr/bin/env python3

#Using Cosine Similarity with Cache on SQLite

import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ascii_art = """ 
										  #    ### 
	 ####    ##    ####  #    # ######   # #    #  
	#    #  #  #  #    # #    # #       #   #   #  
	#      #    # #      ###### #####  #     #  #  
	#      ###### #      #    # #      #######  #  
	#    # #    # #    # #    # #      #     #  #  
	 ####  #    #  ####  #    # ###### #     # ### v.1.0 2023
"""

# Stampa l'articolazione ASCII
print(ascii_art)

# Creare un vettorizzatore TF-IDF
# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

def get_response(prompt):
	conn = sqlite3.connect('cache.db')
	cursor = conn.cursor()
	
	# Recupera tutte le domande e le risposte dalla cache
	# Retrieves all questions and answers from cache
	cursor.execute("SELECT prompt, response FROM cache")
	cached_data = cursor.fetchall()
	cached_prompts = [row[0] for row in cached_data]
	
	# Calcola la similarità del coseno tra la nuova domanda e quelle in cache
	# Calculate the cosine similarity between the new question and the cached ones
	if cached_prompts:
			tfidf_matrix = vectorizer.fit_transform([prompt] + cached_prompts)
			similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
			print("Similarity:", similarity)  # Stampa i valori di similarità
		
			# Tuning soglia threshold
			# Tuning parameter threshold
			threshold = 0.215  
			if similarity.max() > threshold:
				similar_prompt_index = similarity.argmax()
				response = cached_data[similar_prompt_index][1]
				conn.close()
				return response
		
	conn.close()
	# Aggiungi la chiamata alla API (OpenAI, Bard...) e aggiungi la risposta in cache
	#add API calls (OpenAI, BARD,...)
	#add cache (prompt, OpenAI Response)
	return "No similar questions in cache...make call to OpenAI, Bard or other model APIs!" 



# Add a question and answer to the cache, use differend DB (e.g. MySql for prodcution use)	
def add_to_cache(prompt, response):
	conn = sqlite3.connect('cache.db')
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS cache (prompt TEXT UNIQUE, response TEXT)")
		
	cursor.execute("SELECT * FROM cache WHERE prompt = ?", (prompt,))
	data = cursor.fetchone()
		
	if data is None:
		cursor.execute("INSERT INTO cache (prompt, response) VALUES (?, ?)", (prompt, response))
		conn.commit()
			
	conn.close()	

# Delete cache.db
def delete_cache():
	conn = sqlite3.connect('cache.db')
	cursor = conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS cache")
	conn.commit()
	conn.close()	
	


def main():
	# Clear the cache with delete_cache() 
#Initialize the cache by adding data
#question/answer pairs to cache	
	questions_answers=[
		["Come cucino il risotto?", "Ecco una ricetta per il risotto..."],
		["Cosa è OWASP?", "OWASP è una metodologia per la programmazione sicura..."],
		["Cosa è OWASP Mobile?", "OWASP è una metodologia per la programmazione sicura in ambito mobile"],
		["Possedete delle certificazioni?", "Si, abbiamo la certificazione ISO 27001 e siamo certificati anche PCI DSS"],
		["Le password e i dati sono protetti con algoritmi di cifratura?", "Si, utilizziamo SHA256 per le password e altri algoritmi di cifratura per gli altri dati"],
		["Ogni quanto vengono cambiate le password?", "Le password vengono cambiate ogni 90 giorni"],
		["È possibile utilizzare dispositivi USB personali per il trasferimento di dati Aziendali?", "No, non è possibile usare dispositivi USB"],
		["I dispositivi USB personali possono contenere dati aziendali?", "No, non è possibile usare dispositivi USB"]
	]
	
#question/answer pairs added to cache	
	for q_a in questions_answers:
		add_to_cache(q_a[0],q_a[1])
		

#Prompt - list of questions on which we check if there are similarities with those in cache
	questions=["Qual è una buona ricetta per il risotto?","Chi è Dante Alighieri?","Owasp a cosa serve?","Cosa uso per la sicurezza mobile?","Avete delle certificazioni?","I dati sono cifrati?","Con quale frequenza vengono cambiate le password?","Come è normato l'utilizzo di dispositivi USB?","E' possibile copiare dati aziendali su dispositivi USB personali?"]
	
	for prompt in questions:
		print (prompt)
		print( get_response(prompt)+"\n")
	
		
	
	while True:
		command = input("Enter a command (Q to exit, D to clear table): ")
		if command.upper() == 'Q':
			print ("Thank you!")
			break
		elif command.upper() == 'D':
			delete_cache()
			print("Table Deleted.")
		else:
			print("Command not recognized. Try again")	
	
	
	
if __name__ == "__main__":
	main()		
		
		
		