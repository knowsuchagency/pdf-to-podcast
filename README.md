# PDF to Podcast Converter

## Overview

This project provides a tool to convert any PDF document into a podcast episode! Using OpenAI's text-to-speech models and Google Gemini, this tool processes the content of a PDF, generates a natural dialogue suitable for an audio podcast, and outputs it as an MP3 file.

## Features

- **Convert PDF to Podcast:** Upload a PDF and convert its content into a podcast dialogue.
- **Engaging Dialogue:** The generated dialogue is designed to be informative and entertaining.
- **Multiple Voice Options:** Choose from different voices to narrate the podcast.
- **User-friendly Interface:** Simple interface using Gradio for easy interaction.

## Installation

To set up the project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/knowsuchagency/pdf-to-podcast.git
   cd pdf-to-podcast
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Set up API Key(s):**
   Ensure you have an Google Gemini API key. You can get yours at https://aistudio.google.com/app/apikey.
   Use it as the value to `GEMINI_API_KEY`.
   You'll also need an api key for OpenAI which you can either pass through the interface or set as the `OPENAI_API_KEY` environment variable.

   Gemini flash is used as the LLM and OpenAI is used for text-to-speech.

2. **Run the application:**
   ```bash
   python main.py
   ```
   This will launch a Gradio interface in your web browser.

3. **Upload a PDF:**
   Upload the PDF document you want to convert into a podcast.

4. **Enter OpenAI API Key:**
   Provide your OpenAI API key in the designated textbox.

5. **Generate Audio:**
   Click the button to start the conversion process. The output will be an MP3 file containing the podcast dialogue.

## Project Structure

- **main.py:** Main application script.
- **requirements.txt:** List of dependencies.
- **README.md:** Project documentation (this file).

## Code Explanation

### Dialogue Models

Defines the structure of the dialogue using Pydantic models.

```python
class DialogueItem(BaseModel):
    text: str
    voice: Literal["alloy", "onyx", "fable"]

class Dialogue(BaseModel):
    scratchpad: str
    dialogue: List[DialogueItem]
```

### LLM Function

Generates dialogue based on the input text using the `promptic` decorator.

```python
@llm(model="gemini/gemini-1.5-flash")
def generate_dialogue(text: str) -> Dialogue:
    # Function to generate podcast dialogue
```

### TTS Function

Converts text to speech using OpenAI's text-to-speech model.

```python
def get_mp3(text: str, voice: str, api_key: str = None) -> bytes:
    # Function to generate MP3 from text
```

### Main Function

Processes the PDF, generates dialogue, and converts it to audio.

```python
def generate_audio(file: bytes, openai_api_key: str) -> bytes:
    # Main function to process PDF and generate audio
```

### Gradio Interface

Creates a user-friendly interface for uploading PDFs and generating podcasts.

```python
demo = gr.Interface(
    title="PDF to Podcast",
    description="Convert any PDF document into an engaging podcast episode!",
    fn=generate_audio,
    inputs=[
        gr.File(label="Input PDF", type="binary"),
        gr.Textbox(label="OpenAI API Key", placeholder="Enter your OpenAI API key here"),
    ],
    outputs=[
        gr.Audio(format="mp3"),
    ],
)

demo.launch(show_api=False)
```

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for more information.
