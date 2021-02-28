import argparse
import json


def is_title(text):
    parts = text.strip().split(' ')
    for part in parts:
        if not part.isupper() or ':' in part:
            return False
    return True


def is_abbrev(text):
    parts = text.strip().split(' ')
    return len(parts) == 1 and parts[0][0].isupper() and not parts[0].isupper()


def is_page_number(text):
    text = text.strip()
    return text.isdigit() and len(text) < 4


def new_chapter(tree):
    chapter = {}
    tree['chapters'].append(chapter)
    return chapter


def generate_page_tree(json_path):
    with open(json_path, 'r') as ocr_file:
        contents = json.load(ocr_file)

    header = {}
    chapters = []
    tree = {'header': header, 'chapters': chapters}

    text = contents['fullTextAnnotation']['text']

    for line in text.split('\n'):
        # if no div and no header
        if not header.get('name') and is_title(line) and len(tree['chapters']) == 0:
            header['name'] = line.strip()
        else if not header.get('abbrev') and is_abbrev(line) and len(tree['chapters']) == 0:
            header['abbrev'] = line.strip()
        else:
            # TODO


    return tree


def print_page(tree):
    print(json.dumps(tree, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate structural text tree from the OCR result')
    parser.add_argument('json_path',
                        help='Path to the input json (OCR result)')

    args = parser.parse_args()
    page_tree = generate_page_tree(args.json_path)

    print_page(page_tree)

    with open('out.json', 'w') as tree_file:
        json.dump(page_tree, tree_file)


"""
-page
  -header [name, abbrev]

  -chapter
    -title [name, abbrev]
    -div
  -page_number
"""
