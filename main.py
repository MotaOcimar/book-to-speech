from google.cloud import texttospeech as tts
from epubToSsml import *

client = tts.TextToSpeechClient()

ssml_texts = epub_to_ssml("books/Coen.epub")

for filename in ssml_texts:

    synthesis_input = tts.SynthesisInput(ssml=ssml_texts[filename])

    voice = tts.VoiceSelectionParams(
        language_code="pt-BR"
        # , name="pt-BR-Wavenet-B"
    )

    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    out_filename = "./output/" + filename + ".mp3"
    with open(out_filename, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "' + out_filename +'"')
