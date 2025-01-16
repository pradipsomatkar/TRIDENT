import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import smtplib

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user
def greet():
    current_hour = datetime.datetime.now().hour
    if 0 <= current_hour < 12:
        speak("Good morning!")
    elif 12 <= current_hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am trident, your personal assistant. How can I assist you today?")

# Function to take voice command
def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an issue with the service.")
        return ""

# Function to send email
def send_email(receiver, subject, body):
    # Configure your email settings here
    email_address = "somatkarpradip54email@gmail.com"
    email_password = "your_email_password"
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_address, email_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(email_address, receiver, message)
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the email.")

# Function to respond to user commands
def respond(command):
    if command == " hi trident":
        speak("Please say the password to proceed.")
        password = take_command()
        if password == "hi":
            speak("Password accepted. How can I assist you?")
            command = take_command()
            if "wikipedia" in command:
                speak("Searching Wikipedia...")
                query = command.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            elif "open youtube" in command:
                webbrowser.open("https://www.youtube.com")
            elif "open google" in command:
                webbrowser.open("https://www.google.com")
            elif "open stackoverflow" in command:
                webbrowser.open("https://stackoverflow.com")
            elif "play music" in command:
                music_dir = "path_to_your_music_directory"
                songs = os.listdir(music_dir)
                random_song = random.choice(songs)
                os.startfile(os.path.join(music_dir, random_song))
            elif "what's the time" in command:
                current_time = datetime.datetime.now().strftime("%H:%M")
                speak(f"The current time is {current_time}")
            elif "send email" in command:
                speak("To whom you want to send the email?")
                receiver = take_command()
                speak("What is the subject of the email?")
                subject = take_command()
                speak("What should be the content of the email?")
                body = take_command()
                send_email(receiver, subject, body)
            elif "exit" in command or "quit" in command:
                speak("Goodbye!")
                exit()
            elif "how are you" in command:
                speak("I'm doing great, thank you for asking!")
            elif "who created you" in command:
                speak("I was created by pradip somatkar. He designed me to assist you.")
            elif "tell me a joke" in command:
                jokes = ["engineering is very easy ha ha ha ha ha " 
                        ]
                speak(random.choice(jokes))
            else:
                speak("I'm sorry, I don't understand that command.")
        else:
            speak("Incorrect password. Access denied.")
    else:
        speak("I'm sorry, I only respond when you say 'trident'.")

# Main function
def main():
    greet()

    while True:
        respond(take_command())

if __name__ == "__main__":
    main()
