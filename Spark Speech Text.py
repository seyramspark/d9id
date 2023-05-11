from gtts import gTTS
import openai
import winsound
import speech_recognition as sr
from elevenlabslib import ElevenLabsUser
from pydub import AudioSegment
from pydub.playback import play
import io
import streamlit as st

openai.api_key = "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"
api_key = "b2d757670a1471d09b747853916e036f"
user = ElevenLabsUser(api_key)

messages = ["You are a Christian advisor. Please respond to all input in 50 words or less."]

def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(audio_file)
    with audio_data as source:
        audio = recognizer.record(source)
    transcript = recognizer.recognize_google(audio)

    messages.append(f"\nUser: {transcript}")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=messages[-1],
        max_tokens=80,
        n=1,
        stop=None,
        temperature=0.5,
    )

    system_message = response["choices"][0]["text"]
    messages.append(f"{system_message}")

    voice = user.get_voices_by_name("Antoni")[0]
    audio = voice.generate_audio_bytes(system_message)

    audio = AudioSegment.from_file(io.BytesIO(audio), format="mp3")
    audio.export("output.wav", format="wav")

    winsound.PlaySound("output.wav", winsound.SND_FILENAME)

    chat_transcript = "\n".join(messages)
    return chat_transcript

def app():
    st.set_page_config(page_title="⛪👨 Love God, am Your Preaching Assistant ⛪📖",
                       page_icon=r"C:\Users\usaer\Desktop\love.jpg")
    st.title("⛪👨 Love God, am Your Preaching Assistant ⛪📖")

    st.write("🌟 Please ask me your question and I will respond both verbally and in text to you...")

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
            chat_transcript = transcribe(audio)
            bot_response = chat_transcript.split("\n")[-2].split(":")[1].strip()

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

app()

