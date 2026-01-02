## Project Overview
The Synthetic Radio Host converts Wikipedia articles into natural Hinglish radio-style conversations and audio.

## Architecture
User input is processed via Wikipedia API, passed to an LLM for script generation, approved via GUI, and converted to audio using ElevenLabs.

## Tech Stack
Python, OpenAI, ElevenLabs, ipywidgets, Pydub

## Setup Instructions
Install dependencies using requirements.txt and run the Colab notebook.

## Assumptions
Internet access and valid API keys are required.

## Error Handling
Script validation ensures valid dialogue before audio generation.
