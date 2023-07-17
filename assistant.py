import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
from datetime import datetime
import phonenumbers
from phonenumbers import carrier, geocoder
import smtplib
from email.message import EmailMessage

listener = sr.Recognizer()
siri = pyttsx3.init()

def speak(text):
    siri.say(text)
    siri.runAndWait()

def get_time():
    current_time = datetime.now().strftime('Now the time is %H:%M')
    speak(current_time)
    return current_time

def search_song(command):
    return pywhatkit.playonyt(command)

def search_web(command):
    return pywhatkit.search(command)

def summary(command):
    query = command.strip().lower()

    if 'summary of' in query:
        keyword = query.replace('summary of', '').strip()
        info = wikipedia.summary(keyword, sentences=1)
        speak(info)
        return info
    else:
        info = pywhatkit.search(query)
        speak(info)
        return info

def country_pro():
    number = input("Enter your number: ")
    parsed_number = phonenumbers.parse(number, "IN")  # Replace "IN" with the appropriate default region
    location = geocoder.description_for_number(parsed_number, "en")
    print("Location:", location)

    service_provider = carrier.name_for_number(parsed_number, "en")
    print("Service Provider:", service_provider)

def send_mail():
    receiver = input("Enter recipient's email: ")
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("your-email@gmail.com", "your-password")  # Replace with your email and password

    email = EmailMessage()
    email["From"] = "your-email@gmail.com"  # Replace with your email
    email["To"] = receiver
    email["Subject"] = subject
    email.set_content(body)

    server.send_message(email)
    server.quit()

siri.say("Welcome! I am Siri, your virtual assistant. How can I help you?")
siri.runAndWait()

print("Welcome! I am Siri, your virtual assistant.")
print("---------------------------------------------")

while True:
    with sr.Microphone() as source:
        listener.pause_threshold = 1  # Adjust the pause threshold as needed
        listener.energy_threshold = 1000  # Adjust the energy threshold as needed
        listener.dynamic_energy_adjustment_ratio = 1.5  # Adjust the dynamic energy adjustment ratio as needed

        speak("I am listening.")
        print("I am listening...")

        try:
            voice = listener.listen(source, timeout=40, phrase_time_limit=5)  # Set the timeout value to 40 seconds, and phrase time limit to 5 seconds
            command = listener.recognize_google(voice)
            print(command)
            command = command.lower()

            if 'play song' in command or 'play music' in command:
                search_song(command)
                input("Press enter to continue...")
            elif 'search' in command:
                search_web(command)
                input("Press enter to continue...")
            elif 'send email' in command:
                send_mail()
                input("Press enter to continue...")
            elif 'phone number' in command:
                speak("Enter your mobile number.")
                country_pro()
                input("Press enter to continue...")
            elif 'summary of' in command:
                command = command.replace('summary of', '')
                summary(command)
                input("Press enter to continue...")
            elif 'time' in command:
                get_time()
                input("Press enter to continue...")
            elif 'exit' in command:
                speak("Thanks for coming. Goodbye!")
                break
            else:
                speak("Please choose valid options.")
        except sr.WaitTimeoutError:
            print("Timeout reached. Listening again...")
        except sr.UnknownValueError:
            print("Speech not recognized. Please try again.")