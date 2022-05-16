from bs4 import BeautifulSoup
from pathlib import Path
import zipfile
import shutil
import glob



def tag_handler(element):
    bs = BeautifulSoup('', features="html.parser")
    after_tag = None
    tag = bs
    before_tag = None
    
    if element.name == 'blockquote' or element.name == 'span':

        after_tag = bs.new_tag("break")
        after_tag['time'] = "500ms"

        tag = bs.new_tag("s")

    if element == 'p':
        tag = bs.new_tag('p')
    
    return before_tag, tag, after_tag


def recursive_processing(element):
    processed_element = BeautifulSoup('', features="html.parser")

    if hasattr(element, 'contents'):
        
        before, tag, after = tag_handler(element)

        if before is not None:
            processed_element.append(before)

        for child in element.contents:
            tag.append(recursive_processing(child))

        processed_element.append(tag)

        if after is not None:
            processed_element.append(after)

    else:
        processed_element.append(element.get_text())

    return processed_element


def process_file(filename):
    with open(filename, "r") as in_file:
        html_text = in_file.read()


    in_bs = BeautifulSoup(html_text, features="html.parser")


    processed_bs = recursive_processing(in_bs.body)


    out_bs = BeautifulSoup('', features="html.parser")
    speak = out_bs.new_tag('speak')
    speak.append(processed_bs)
    out_bs.append(speak)

    return str(speak)


def epub_to_ssml(filename):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall("./tmp/")


    ssml_texts = {}

    for filename in glob.glob('./tmp/*.html'):
        ssml_texts[Path(filename).stem] = process_file(filename)

    shutil.rmtree('./tmp/')

    return ssml_texts
