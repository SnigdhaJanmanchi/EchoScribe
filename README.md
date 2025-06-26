# 🎥 EchoScribe: Smart Video Transcriber (English Only)

**EchoScribe** is an AI-powered web app built with 🤗 Hugging Face Transformers and Gradio. It lets you upload an English-language video, automatically transcribe the speech, restore punctuation, generate a summary, and download subtitle and transcript files — all in a simple browser-based UI.

---

## 🌍 English-Only Support

> ⚠️ This app currently supports **only English** speech.
> If the uploaded video contains non-English audio, it will be translated to English using `language='en'` in Whisper.

---

## ✨ Features

- 🎬 Upload `.mp4` videos with spoken content
- 🧠 Speech transcription using Whisper (`openai/whisper-large`)
- ✍️ Punctuation restoration using T5 (`vennify/t5-base-grammar-correction`)
- 📝 Summarization with BART (`facebook/bart-large-cnn`)
- 📁 Download:
  - Cleaned transcript (.txt)
  - Summary (.txt)
  - Subtitles (.srt)
- ⚡ Built with Gradio for a fast, interactive web interface

---

## 🧠 Models Used

| Task              | Model Used                                       |
|------------------|--------------------------------------------------|
| Speech to Text   | [`openai/whisper-large`](https://huggingface.co/openai/whisper-large) |
| Punctuation      | [`vennify/t5-base-grammar-correction`](https://huggingface.co/vennify/t5-base-grammar-correction) |
| Summarization    | [`facebook/bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn) |

---

## 🧰 Tech Stack

- **Gradio** — UI framework for web apps
- **Transformers** — Access to pretrained Hugging Face models
- **Torch** — Deep learning backend
- **MoviePy** — Extract audio from video
- **Pydub** — Audio handling helper
- **FFmpeg** — Required backend for MoviePy/Pydub
- **srt** — Subtitle (.srt) file generation

---

## 📦 Dependencies

Here’s the `requirements.txt` used in this project:

```
gradio
transformers
torch
moviepy==1.0.3
pydub
ffmpeg-python
srt
```

---

## 🚀 How to Deploy on Hugging Face Spaces

You can easily deploy this project to Hugging Face Spaces in minutes:

### 1. Create a Space

- Go to [https://huggingface.co/spaces](https://huggingface.co/spaces)
- Click **"Create new Space"**
- Choose:
  - **Space Name**: `echoscribe` (or any name you prefer)
  - **SDK**: `Gradio`
  - **License**: MIT or other
  - **Visibility**: Public or Private

### 2. Upload Your Files

Upload the following three files:

- `app.py` – Contains the full pipeline and Gradio UI
- `requirements.txt` – Specifies dependencies
- `README.md` – Describes your app and how to deploy it

### 3. Auto Deployment

Hugging Face will automatically install dependencies and launch the app.
You’ll see a live preview in your browser within 1–3 minutes.

---

## 💡 Future Ideas

- 🌐 Support for multilingual audio
- 🎙️ Live microphone-based transcription
- 🧑‍💼 Speaker separation (diarization)
- 📄 Export to `.vtt` subtitle format
## 🚩 Live Demo

Try out the EchoScribe app live on Hugging Face Spaces:  
[https://huggingface.co/spaces/Sjanmanchi/EchoScribe](https://huggingface.co/spaces/Sjanmanchi/EchoScribe)
