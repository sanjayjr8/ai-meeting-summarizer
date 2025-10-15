import whisper

# Make sure to replace 'your_audio_file.mp3' with the actual name of your file
AUDIO_FILE_PATH = "Meeting.mp3" 

print("Loading the Whisper model...")
# We use the "base" model because it's small and fast. 
# For higher accuracy, you can use "medium" or "large", but they are slower.
model = whisper.load_model("base") 
print("Model loaded. Starting transcription...")

# Transcribe the audio file
result = model.transcribe(AUDIO_FILE_PATH)

# Print the resulting text
print("\n--- Transcription Result ---")
print(result["text"])
print("--------------------------")