import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os

# Your existing code to define the bot's functionality
# ...

# Define a function to handle user input and generate bot responses
def generate_response(input_text):
    # Your existing code to generate responses
    # ...

# Define the Streamlit app
def app():
    st.title("Bot App")

    # Create a text input for the user to type their input
    user_input = st.text_input("Enter your input:")

    # Create a button to submit the user's input
    if st.button("Submit"):
        # Generate the bot's response
        bot_response = generate_response(user_input)

        # Display the bot's response in text
        st.write("Bot: ", bot_response)

        # Convert the bot's response to speech and play it
        tts = gTTS(text=bot_response, lang='en')
        tts.save("bot_response.mp3")
        os.system("mpg321 bot_response.mp3")

    # Create a button to allow the user to speak their input
    if st.button("Speak"):
        # Use speech recognition to get the user's spoken input
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Speak now...")
            audio = r.listen(source)
            st.write("Processing...")

        # Convert the user's spoken input to text
        try:
            user_input = r.recognize_google(audio)
            st.write("You: ", user_input)

            # Generate the bot's response
            bot_response = generate_response(user_input)

            # Display the bot's response in text
            st.write("Bot: ", bot_response)

            # Convert the bot's response to speech and play it
            tts = gTTS(text=bot_response, lang='en')
            tts.save("bot_response.mp3")
            os.system("mpg321 bot_response.mp3")

        except sr.UnknownValueError:
            st.write("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            st.write("Sorry, there was an error processing your request. Please try again later.")
