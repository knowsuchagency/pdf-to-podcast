# PDF to Podcast

## Overview

This project provides a tool to convert any PDF document into a podcast episode! Using OpenAI's text-to-speech models and Google Gemini, this tool processes the content of a PDF, generates a natural dialogue suitable for an audio podcast, and outputs it as an MP3 file.

## Features

- **Convert PDF to Podcast:** Upload a PDF and convert its content into a podcast dialogue.
- **Engaging Dialogue:** The generated dialogue is designed to be informative and entertaining.
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
   python -m venv .venv
   source .venv/bin/activate
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

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for more information.
