from google.cloud import texttospeech as tts
from epubToSsml import *

client = tts.TextToSpeechClient()



synthesis_input = tts.SynthesisInput(ssml=process_file("books/index_split_004.html"))

voice = tts.VoiceSelectionParams(
    language_code="pt-BR", name="pt-BR-Wavenet-B"
)

audio_config = tts.AudioConfig(
    audio_encoding=tts.AudioEncoding.MP3
)

# response = client.synthesize_speech(
#     input=synthesis_input, voice=voice, audio_config=audio_config
# )

# with open("output.mp3", "wb") as out:
#     out.write(response.audio_content)
#     print('Audio content written to file "output.mp3"')
