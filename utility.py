import gradio as gr
import openai
import winsound
from elevenlabslib import *
from pydub import AudioSegment
from pydub.playback import play
import io

openai.api_key = "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"
api_key = "b2d757670a1471d09b747853916e036f"
from elevenlabslib import ElevenLabsUser
user = ElevenLabsUser("b2d757670a1471d09b747853916e036f")

messages = ["You are a Christian advisor. Please respond to all input in 50 words or less."]

def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append(f"\nUser: {transcript['text']}")

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

iface = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(source="microphone", type="filepath", placeholder="Please start speaking..."),
    outputs="text",
    title="⛪👨 Love God, am Your Preaching Assistant ⛪📖",
    description="🌟 Please ask me your question and I will respond both verbally and in text to you...",
    thumbnail="C:\Users\usaer\Desktop\love.jpg"
)

iface.launch(share=True)
