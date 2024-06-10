import concurrent.futures as cf
import io
import os
from pathlib import Path
from typing import List, Literal

import gradio as gr
from loguru import logger
from openai import OpenAI
from promptic import llm
from pydantic import BaseModel, ValidationError
from pypdf import PdfReader
from tenacity import retry, retry_if_exception_type


class DialogueItem(BaseModel):
    text: str
    speaker: Literal["female-1", "male-1", "female-2"]

    @property
    def voice(self):
        return {
            "female-1": "alloy",
            "male-1": "onyx",
            "female-2": "shimmer",
        }[self.speaker]


class Dialogue(BaseModel):
    scratchpad: str
    dialogue: List[DialogueItem]


@retry(retry=retry_if_exception_type(ValidationError))
@llm(model="gemini/gemini-1.5-flash")
def generate_dialogue(text: str) -> Dialogue:
    """
    Your task is to take the input text provided and turn it into an engaging, informative podcast dialogue. The input text may be messy or unstructured, as it could come from a variety of sources like PDFs or web pages. Don't worry about the formatting issues or any irrelevant information; your goal is to extract the key points and interesting facts that could be discussed in a podcast.

    Here is the input text you will be working with:

    <input_text>
    {text}
    </input_text>

    First, carefully read through the input text and identify the main topics, key points, and any interesting facts or anecdotes. Think about how you could present this information in a fun, engaging way that would be suitable for an audio podcast.

    <scratchpad>
    Brainstorm creative ways to discuss the main topics and key points you identified in the input text. Consider using analogies, storytelling techniques, or hypothetical scenarios to make the content more relatable and engaging for listeners.

    Keep in mind that your podcast should be accessible to a general audience, so avoid using too much jargon or assuming prior knowledge of the topic. If necessary, think of ways to briefly explain any complex concepts in simple terms.

    Use your imagination to fill in any gaps in the input text or to come up with thought-provoking questions that could be explored in the podcast. The goal is to create an informative and entertaining dialogue, so feel free to be creative in your approach.

    Write your brainstorming ideas and a rough outline for the podcast dialogue here.
    </scratchpad>

    Now that you have brainstormed ideas and created a rough outline, it's time to write the actual podcast dialogue. Aim for a natural, conversational flow between the host and any guest speakers. Incorporate the best ideas from your brainstorming session and make sure to explain any complex topics in an easy-to-understand way.

    <podcast_dialogue>
    Write your engaging, informative podcast dialogue here, based on the key points and creative ideas you came up with during the brainstorming session. Use a conversational tone and include any necessary context or explanations to make the content accessible to a general audience. Rather than adding variable brackets like `[Host Name]` or `[Guest Name]`, use made-up names for the host and any guest speakers to create a more engaging and immersive experience for listeners as your output will be used to generate audio.
    </podcast_dialogue>
    """


def get_mp3(text: str, voice: str, api_key: str = None) -> bytes:
    client = OpenAI(
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
    )

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        input=text,
    ) as response:
        with io.BytesIO() as file:
            for chunk in response.iter_bytes():
                file.write(chunk)
            return file.getvalue()


def generate_audio(file: str, openai_api_key: str = None) -> bytes:

    if not os.getenv("OPENAI_API_KEY", openai_api_key):
        raise gr.Error("OpenAI API key is required")

    with Path(file).open("rb") as f:
        reader = PdfReader(f)
        text = "\n\n".join([page.extract_text() for page in reader.pages])

    llm_output = generate_dialogue(text)

    audio = b""
    transcript = ""

    characters = 0

    with cf.ThreadPoolExecutor() as executor:
        futures = []
        for line in llm_output.dialogue:
            transcript_line = f"{line.speaker}: {line.text}"
            logger.info(transcript_line)
            future = executor.submit(get_mp3, line.text, line.voice, openai_api_key)
            futures.append((future, transcript_line))
            characters += len(line.text)

        for future, transcript_line in futures:
            audio_chunk = future.result()
            audio += audio_chunk
            transcript += transcript_line + "\n\n"

    logger.info(f"Generated {characters} characters of audio")

    return audio, transcript


description = """
<p style="text-align:center">
  <strong>Convert any PDF into a podcast episode! Experience research papers, websites, and more in a whole new way.</strong>
  <br>
  <a href="https://github.com/knowsuchagency/pdf-to-podcast">knowsuchagency/pdf-to-podcast</a>
</p>
"""

demo = gr.Interface(
    title="PDF to Podcast",
    description=description,
    fn=generate_audio,
    examples=[[str(p)] for p in Path("examples").glob("*.pdf")],
    inputs=[
        gr.File(
            label="PDF",
        ),
        gr.Textbox(
            label="OpenAI API Key",
            visible=not os.getenv("OPENAI_API_KEY"),
        ),
    ],
    outputs=[
        gr.Audio(label="Audio", format="mp3"),
        gr.Textbox(label="Transcript"),
    ],
    allow_flagging=False,
    clear_btn=None,
    head=os.getenv("HEAD"),
    concurrency_limit=20,
    cache_examples="lazy",
)

demo.launch(
    show_api=False,
)
