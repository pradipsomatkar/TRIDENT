import speech_recognition as sr
import pyttsx3
import spacy
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup

# Load pre-trained NLP model for intent recognition and entity extraction
nlp = spacy.load("en_core_web_sm")

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize speech synthesis with a female voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# Define Ananya's personality
class Ananya:
    def __init__(self):
        self.name = "Ananya"
        self.context = {}  # Initialize context for maintaining conversation history
        self.user_preferences = {}  # Initialize user preferences

    # Define function for speech synthesis with Ananya's voice
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    # Define function for voice chat
    def chat(self):
        self.speak(f"Welcome! I'm {self.name}, your voice-enabled chatbot. How can I assist you today?")
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)
                    print("Recognizing...")
                    user_input = recognizer.recognize_google(audio).lower()
                    print("User:", user_input)
                    if user_input == 'quit':
                        self.speak("Goodbye!")
                        break
                    # Perform intent recognition and entity extraction using the pre-trained NLP model
                    intent, entities = self.recognize_intent_and_entities(user_input)
                    # Perform sentiment analysis on user input
                    sentiment = self.analyze_sentiment(user_input)
                    # Generate dynamic response based on intent, entities, and sentiment
                    response = self.generate_response(intent, entities, sentiment)
                    self.speak(response)
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand what you said. Please try again.")
            except sr.RequestError:
                self.speak("Sorry, I'm unable to access the Google Speech Recognition API at the moment.")
            except Exception as e:
                self.speak("Sorry, an error occurred. Please try again.")

    # Define function for intent recognition and entity extraction using the pre-trained NLP model
    def recognize_intent_and_entities(self, user_input):
        doc = nlp(user_input)
        # Placeholder logic for intent recognition and entity extraction based on NLP model
        intent = "unknown"
        entities = {}  # Placeholder for extracted entities
        if "greet" in [token.text.lower() for token in doc]:
            intent = "greeting"
        elif "weather" in [token.text.lower() for token in doc]:
            intent = "weather"
        elif "search" in [token.text.lower() for token in doc]:
            intent = "search"
            # Extract search query entity
            entities["query"] = " ".join([token.text for token in doc if token.text.lower() != "search"])
        # Placeholder for entity extraction logic
        # Extract entities such as date, location, etc.
        return intent, entities

    # Define function for sentiment analysis using TextBlob
    def analyze_sentiment(self, user_input):
        blob = TextBlob(user_input)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0.5:
            return "positive"
        elif sentiment_score < -0.5:
            return "negative"
        else:
            return "neutral"

    # Define function for generating response based on intent, entities, and sentiment
    def generate_response(self, intent, entities, sentiment):
        # Placeholder logic for response generation based on intent, entities, and sentiment
        if intent == "greeting":
            return f"Hello! How can I assist you today?"
        elif intent == "weather":
            # Placeholder for retrieving weather information based on location entity
            location = entities.get("india", "malegaon jahangir")
            return f"The weather forecast for {location} is sunny with a high of 25 degrees Celsius."
        elif intent == "search":
            query = entities.get("query", "")
            if query:
                # Perform web search and scrape relevant information from search results
                search_results = self.perform_web_search(query)
                if search_results:
                    return search_results
                else:
                    return "Sorry, I couldn't find any relevant information for your query."
            else:
                return "I'm sorry, I didn't catch the search query. Can you please repeat?"
        else:
            return "I'm sorry, I'm not sure how to respond to that."

    # Define function to perform web search and scrape relevant information
    def perform_web_search(self, query):
        try:
            # Perform web search using a search engine API or directly querying search engine websites
            # For demonstration purposes, we'll use a simple web scraping approach using requests and BeautifulSoup
            search_url = f"https://www.google.com/search?q={query}"
            response = requests.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
            if search_results:
                return search_results[0].text
            else:
                return None
        except Exception as e:
            print("Error performing web search:", e)
            return None

# Main function to start the chat
if __name__ == "__main__":
    ananya = Ananya()
    ananya.chat()
