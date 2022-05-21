from epubToSsml import epub_to_ssml
from ssmlToMp3 import SsmlToMp3


ssml_texts = epub_to_ssml("books/test.zip")

ssml_to_mp3 = SsmlToMp3()

for filename in ssml_texts:
    audio_content = ssml_to_mp3.convert(ssml_texts[filename])

    out_filename = "./output/" + filename + ".mp3"
    with open(out_filename, "wb") as out:
        out.write(audio_content)
        print('Audio content written to file "' + out_filename +'"')
    