from elevenlabs.client import ElevenLabs
import gradio as gr
import os
from elevenlabs import play

client = ElevenLabs(
#   api_key="YOUR_API_KEY", # Defaults to ELEVEN_API_KEY
)

female_voice = "nDJIICjR9zfJExIFeSCN"
male_voice = "1m3E2x7boso3AU9J3woJ"

def talk():

    # Define the dialogue text and assign different voices
    dialogue = [
        {"text": "Hello! How are you today?", "voice": female_voice},
        {"text": "I'm doing well, thank you! How about you?", "voice": male_voice},
        {"text": "I'm great, thanks for asking!", "voice": female_voice},
    ]

    # Generate and play the dialogue
    for line in dialogue:
        audio = client.generate(
            text=line["text"],
            voice=line["voice"],
            model="eleven_monolingual_v1",
        )
        # play(audio)
        yield audio

def speak():
    clips = [b"".join(audio) for audio in talk()]
    return b"".join(clips)

def get_interface():
    with gr.Blocks() as blocks:
        gr.Audio(value=speak)
    return blocks


if __name__ == '__main__':
    demo = get_interface()
    demo.launch()
