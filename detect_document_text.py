import argparse
import io
import json

from google.cloud import vision
from google.protobuf.json_format import MessageToJson


def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    serialized = MessageToJson(response)
    with open(path.split('.')[0]+'.json', 'w') as out_file:
        out_file.write(serialized)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect text in image of a document with google vision OCR')
    parser.add_argument('image_path',
                        help='Path to the input image')

    args = parser.parse_args()
    detect_text(args.image_path)
