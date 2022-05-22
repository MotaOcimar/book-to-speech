from epubToSsml import epub_to_ssml
from ssmlToMp3 import SsmlToMp3
import argparse


parser = argparse.ArgumentParser(description='Convert epub ebooks to mp3')
parser.add_argument('epub', help='Epub file to convert to mp3')
args = parser.parse_args()

ssml_to_mp3 = SsmlToMp3()

if __name__ == "__main__":
    ssml_texts = epub_to_ssml(args.epub)

    for filename in ssml_texts:

        print(filename)
        print(ssml_texts[filename])
        print()

        audio_content = ssml_to_mp3.convert(ssml_texts[filename])

        out_filename = "./output/" + filename + ".mp3"
        with open(out_filename, "wb") as out:
            out.write(audio_content)
            print('Audio content written to file "' + out_filename +'"')
