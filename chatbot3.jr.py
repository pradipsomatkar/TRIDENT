import speech_recognition as sr
import pyttsx3
import spacy
from textblob import TextBlob
import datetime
import random

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
        self.speak(f"Hello! I'm {self.name}, your voice-enabled chatbot. How can I assist you today?")
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
        for token in doc:
            if token.dep_ == "attr" and token.head.text == "you":
                intent = "flirting"
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
        if intent == "flirting":
            return "Well, thank you! You're quite charming yourself. Now, how can I assist you further?"
        elif "weather" in entities:
            # Placeholder for retrieving weather information based on location entity
            location = entities.get("Malegaon jhangir", "your location")
            weather_info = self.get_weather(location)
            if weather_info:
                return weather_info
            else:
                return f"Sorry, I couldn't find the weather for {location}."
        else:
            if "greet" in entities:
                return random.choice(["Hello! How can I help you today?", "Hey there! What can I do for you?", "Hi! What's on your mind?"])
            elif "goodbye" in entities:
                return random.choice(["Goodbye! Have a great day!", "See you later! Take care!", "Farewell! Come back soon!"])
            else:
                return random.choice(["I'm sorry, I didn't catch that. Could you please repeat?", "Hmm, I'm not sure I understand. Can you rephrase that?", "Pardon me, could you say that again?"])

    # Define function to retrieve weather information
    def get_weather(self, location):
        try:
            # Get today's date
            today_date = datetime.datetime.now().strftime("%Y-%m-%d")
            # Placeholder logic to retrieve weather information from an API or web scraping
            # For demonstration purposes, we'll use a simple message
            return f"The weather forecast for {location} on {today_date} is sunny with a high of 25 degrees Celsius."
        except Exception as e:
            print("Error retrieving weather information:", e)
            return None

# Main function to start the chat
if __name__ == "__main__":
    ananya = Ananya()
    ananya.chat()
