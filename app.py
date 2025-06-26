import warnings 
warnings.filterwarnings("ignore")

import gradio as gr
from transformers import pipeline
import tempfile
import torch
import os
import shutil
from moviepy.editor import VideoFileClip
import srt
import datetime

# Select CPU or GPU
device = 0 if torch.cuda.is_available() else -1

# Load Hugging Face pipelines
whisper = pipeline("automatic-speech-recognition", model="openai/whisper-large", device=device)
punctuate = pipeline("text2text-generation", model="vennify/t5-base-grammar-correction")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Extract audio from uploaded video file
def extract_audio(video_path):
    video = VideoFileClip(video_path)
    audio_path = tempfile.mktemp(suffix=".wav")
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    return audio_path

# Generate basic subtitle file
def generate_srt(transcript_text):
    lines = transcript_text.strip().split(". ")
    subs = []
    for i, line in enumerate(lines):
        start = datetime.timedelta(seconds=i * 2)
        end = datetime.timedelta(seconds=(i + 1) * 2)
        subs.append(srt.Subtitle(index=i + 1, start=start, end=end, content=line.strip()))
    srt_data = srt.compose(subs)
    srt_path = tempfile.mktemp(suffix=".srt")
    with open(srt_path, "w") as f:
        f.write(srt_data)
    return srt_path

# Main pipeline
def transcribe_pipeline(video_file):
    try:
        # Copy uploaded file to temp location
        video_path = tempfile.mktemp(suffix=".mp4")
        shutil.copy(video_file, video_path)

        # Extract audio from video
        audio_path = extract_audio(video_path)

        # Transcribe with Whisper (force English)
        result = whisper(audio_path, return_timestamps=True, generate_kwargs={"language": "en"})
        raw_text = " ".join([chunk['text'] for chunk in result['chunks']])

        # Add punctuation
        punctuated = punctuate(raw_text)[0]["generated_text"]

        # Summarize
        summary = summarizer(punctuated, max_length=60, min_length=20, do_sample=False)[0]["summary_text"]

        # Generate subtitle file
        srt_path = generate_srt(punctuated)

        # Save files for download
        raw_txt_path = tempfile.mktemp(suffix=".txt")
        punct_txt_path = tempfile.mktemp(suffix=".txt")
        summary_txt_path = tempfile.mktemp(suffix=".txt")

        with open(raw_txt_path, "w") as f:
            f.write(raw_text)
        with open(punct_txt_path, "w") as f:
            f.write(punctuated)
        with open(summary_txt_path, "w") as f:
            f.write(summary)

        return raw_text, punctuated, summary, punct_txt_path, summary_txt_path, srt_path

    except Exception as e:
        print("❌ Pipeline Error:", e)
        return "Error", "Error", "Error", None, None, None

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as iface:
    gr.Markdown("# 🎥 EchoScribe: Smart Video Transcriber")
    gr.Markdown("Upload a video to extract transcript, add punctuation, and generate a summary. You can also download the .srt subtitle file.")

    with gr.Row():
        video_input = gr.Video(label="🎬 Upload your video")

    with gr.Row():
        raw_output = gr.Textbox(label="🧾 Raw Transcript", lines=6)
        punct_output = gr.Textbox(label="📄 Punctuated Transcript", lines=6)

    summary_output = gr.Textbox(label="📝 Summary", lines=4)

    with gr.Row():
        download_transcript = gr.File(label="⬇️ Download Transcript (.txt)")
        download_summary = gr.File(label="⬇️ Download Summary (.txt)")
        download_srt = gr.File(label="⬇️ Download Subtitles (.srt)")

    submit_btn = gr.Button("🚀 Transcribe & Summarize")

    submit_btn.click(
        fn=transcribe_pipeline,
        inputs=video_input,
        outputs=[
            raw_output,
            punct_output,
            summary_output,
            download_transcript,
            download_summary,
            download_srt,
        ],
    )

    gr.Markdown("---")
    gr.Markdown("Built with ❤️ by Snigdha’s AI Lab")

iface.launch(share=True)