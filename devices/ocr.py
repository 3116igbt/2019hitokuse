from google.cloud import vision
from google.cloud.vision import types
from PIL import Image
from PIL import ImageDraw
import sys
import datetime
import analogy_detector

def view_results(path, save_dir, texts):
    # 画像表示
    im = Image.open(path)
    (im_w, im_h) = im.size
    draw = ImageDraw.Draw(im)
    
    print('Texts:')
    for text in texts:
        poly_xy =[] 
        print('\n"{}"'.format(text.description))
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))
        for vertex in text.bounding_poly.vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
            poly_xy.append((vertex.x, vertex.y))
        draw.polygon(poly_xy, outline=(255, 0, 0))

    # 画像保存
    now = datetime.datetime.now()
    save_path = save_dir + "result_" + now.strftime("%y%m%d%H%M%S") + ".jpg"
    im.save(save_path)
    return im_w

def recognize_text(path):
    client = vision.ImageAnnotatorClient()
    # road img
    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    texts = client.text_detection(image=image).text_annotations
        
    return texts

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Err : image_file, and save_dir is not set.")
        sys.exit(1)
    path = sys.argv[1]
    save_dir = sys.argv[2]
    texts = recognize_text(path)
    view_results(path, save_dir, texts)
