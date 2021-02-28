import argparse
import json

BREAK_TO_CHAR = {
    'SPACE': ' ',
    'EOL_SURE_SPACE': '\n',
    'LINE_BREAK': '\n',
    'SURE_SPACE': ' ',
    'HYPHEN': '-',
}

def read_ocr(path, debug_invisible=False):
    with open(path, 'r') as ocr_file:
        contents = json.load(ocr_file)
    
    pages = contents['fullTextAnnotation']['pages']
    assert len(pages) == 1
    page = pages[0]
    
    for block in page['blocks']:
        new_paragraph = False
        for paragraph in block['paragraphs']:
            new_paragraph = True
            for word in paragraph['words']:
                word_chars = []
                for symbol in word['symbols']:
                    text = symbol.get('text')
                    if text:
                        word_chars.append(text)

                    break_type = symbol.get('property', {}).get('detectedBreak', {}).get('type')
                    languages = symbol.get('property', {}).get('detectedLanguages', [])

                    if break_type:
                        if debug_invisible:
                            word_chars.append('<' + break_type + '>')
                        word_chars.append(BREAK_TO_CHAR[break_type])

                    #for language in languages:
                    #    lang = language.get('languageCode')
                    #    if lang and lang != 'hu':
                    #        print('    LANG({})    '.format(lang))
                # print(' ', end='')
                word_str = ''.join(word_chars)
                if new_paragraph and len(word_str.strip()) > 1 and word_str.strip().isupper():
                    print('\n', end='')
                    
                new_paragraph = False
                print(word_str, end='')


def generate_page_tree(path, debug_invisible=False):
    with open(path, 'r') as ocr_file:
        contents = json.load(ocr_file)
    
    tree = {}
    tree_paragraphs = tree.setdefault('paragraphs', [])

    pages = contents['fullTextAnnotation']['pages']
    assert len(pages) == 1
    page = pages[0]

    for block in page['blocks']:
        new_paragraph = False
        tree_paragraph = {}
        tree_paragraphs.append(tree_paragraph)
        div_text = []
        tree_div = {'text': div_text}
        tree_paragraph.setdefault('divs', []).append(tree_div)

        for paragraph in block['paragraphs']:

            new_paragraph = True
            for word in paragraph['words']:
                word_chars = []
                for symbol in word['symbols']:
                    text = symbol.get('text')
                    if text:
                        word_chars.append(text)

                    break_type = symbol.get('property', {}).get('detectedBreak', {}).get('type')
                    languages = symbol.get('property', {}).get('detectedLanguages', [])

                    if break_type:
                        if debug_invisible:
                            word_chars.append('<' + break_type + '>')
                        word_chars.append(BREAK_TO_CHAR[break_type])

                    #for language in languages:
                    #    lang = language.get('languageCode')
                    #    if lang and lang != 'hu':
                    #        print('    LANG({})    '.format(lang))
                # print(' ', end='')
                word_str = ''.join(word_chars)
                if new_paragraph and len(word_str.strip()) > 1 and word_str.strip().isupper():
                    tree_paragraph = {}
                    tree_paragraphs.append(tree_paragraph)
                    div_text = []
                    tree_div = {'text': div_text}
                    tree_paragraph.setdefault('divs', []).append(tree_div)

                new_paragraph = False
                div_text.append(word_str)
    return tree


def print_tree(page_tree):
    for paragraph in page_tree['paragraphs']:
        for div in paragraph['divs']:
            print(''.join(div['text']), end='')
        print('\n', end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate structural text tree from the OCR result')
    parser.add_argument('json_path',
                        help='Path to the input json (OCR result)')

    args = parser.parse_args()
    page_tree = generate_page_tree(args.json_path)

    print_tree(page_tree)

    with open('out.json', 'w') as tree_file:
        json.dump(page_tree, tree_file)
