# PDF to Podcast

## Overview

This project provides a tool to convert any PDF document into a podcast episode! Using Google's Gemini for dialogue generation and OpenAI's text-to-speech models, this tool processes the content of a PDF, generates a natural dialogue suitable for an audio podcast, and outputs it as an MP3 file.

## Features

- **Convert PDF to Podcast:** Upload a PDF and convert its content into a podcast dialogue.
- **AI-Powered Dialogue:** Uses Google's Gemini LLM to create engaging, natural conversations.
- **High-Quality Audio:** Leverages OpenAI's text-to-speech for lifelike voices.
- **User-friendly Interface:** Simple interface using Gradio for easy interaction.

## Installation

To set up the project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/knowsuchagency/pdf-to-podcast.git
   cd pdf-to-podcast
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

## Usage

1. **Set up API Key(s):**

   You'll need an api key for OpenAI which you can either pass through the interface or set as the `OPENAI_API_KEY` environment variable.

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
