from bs4 import BeautifulSoup
from pathlib import Path
import zipfile
import glob
import tempfile


def epub_to_ssml(epub_filename):

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


    def process_html(filename):
        with open(filename, "r") as in_file:
            html_text = in_file.read()


        in_bs = BeautifulSoup(html_text, features="html.parser")


        processed_bs = recursive_processing(in_bs.body)


        out_bs = BeautifulSoup('', features="html.parser")
        speak_tag = out_bs.new_tag('speak')
        speak_tag.append(processed_bs)
        out_bs.append(speak_tag)

        
        return str(out_bs) if len(out_bs.get_text().strip()) > 0 else None


    def rename_filenames(dictionary):
        sorted_list =  sorted(dictionary.items())

        counter = 0
        sorted_dict = {}
        for item in sorted_list:
            sorted_dict[f'part_{counter:03}'] = item[1]
            counter += 1
        
        return sorted_dict


    ssml_texts = {}

    with tempfile.TemporaryDirectory() as tmp_dir:

        with zipfile.ZipFile(epub_filename, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)

        for html_filename in glob.glob(tmp_dir+'/*.html'):
            ssml = process_html(html_filename)
            if ssml is not None:
                ssml_texts[Path(html_filename).stem] = ssml


    return rename_filenames(ssml_texts)
