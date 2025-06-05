# transcriber for .mp3/.mp4 files.
# make sure you install whisper (pip install git+https://github.com/openai/whisper.git)

import whisper

# Load the model
model = whisper.load_model("medium")

# Transcribe the file (ensure it's also in ultra-research/scripts or adjust path)
result = model.transcribe("1.mp4")

# Save the transcription in the same folder
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print("Transcription complete. Output saved to transcription.txt.")
