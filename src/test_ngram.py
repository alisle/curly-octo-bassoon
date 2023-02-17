import logging
import ngram
import unicodedata
import re
from pprint import pprint


# Ripped from stack overflow. We need to change this.
def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def text_to_id(text):
    """
    Convert input text to id.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = strip_accents(text.lower().strip())
    text = re.sub('[ ]+', ' ', text)
    text = re.sub('[^0-9a-zA-Z_-]', ' ', text)
    return text

def main():
    logging.basicConfig(level=logging.INFO)
    clean_names = []

    gram = ngram.NGram()
    with open("possible_names.txt", "r") as possible_names:
        names = possible_names.readlines()

        for name in names:
            clean_name =  text_to_id(name)
            clean_names.append(clean_name)
            gram.update([clean_name])

            print(f"Before cleanup:{name.strip()} -> {clean_name}")
    print("Doing Stuff:") 
    for name in clean_names:
        potentials = gram.search(name)
        for (potential_name, potential_score) in potentials:
            if potential_score >= 0.2:
                print(f"{name} P-> {potential_name}:{potential_score}")


if __name__ == '__main__':
    main()