from google.cloud import texttospeech as tts


class SsmlToMp3:
    def __init__(self):
        self.voice = tts.VoiceSelectionParams(
            language_code="pt-BR"
            # , name="pt-BR-Wavenet-B"
        )

        self.audio_config = tts.AudioConfig(
            audio_encoding=tts.AudioEncoding.MP3
        )

        self.client = tts.TextToSpeechClient()


    def convert(self, ssml_text):

        synthesis_input = tts.SynthesisInput(ssml=ssml_text)

        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=self.voice,
            audio_config=self.audio_config
        )

        return response.audio_content