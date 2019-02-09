from google.cloud import vision
from google.cloud.vision import types
from PIL import Image
from PIL import ImageDraw
import sys
import datetime
import analogy_detector

def recognize_text(path):
    client = vision.ImageAnnotatorClient()
    # road img
    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    texts = client.text_detection(image=image).text_annotations

    print('Texts:')
    for text in texts:
        print('\n"{}"'.format(text.description))
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Err : image_file is not set.")
        sys.exit(1)
    path = sys.argv[1]
    recognize_text(path)