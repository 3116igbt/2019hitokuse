#import picamera
import sys
import subprocess
import datetime
import time
from PIL import Image as im

import ocr
import record_detector
import firebase_client


# Raspberry Piで撮影
# def take_photo():
#     # セットアップ、解像度を(1280, 720)に
#     camera = picamera.PiCamera()
#     camera.resolution = (1280, 720)
#     # ファイル名セット
#     now = datetime.datetime.now()
#     pname = "/home/pi/img/"+ now.strftime("%y%m%d%H%M%S") + ".jpg"
#     triname = "/home/pi/img/"+ now.strftime("%y%m%d%H%M%S") + "_tri.jpg"
#     # 撮影
#     camera.capture(pname)
#     print("Photo taken filename : {}".format(pname))
#     # トリミング
#     org_img = im.open(pname)
#     w, h = org_img.size
#     tri_img = org_img.crop((w * 0.3, h * 0.2, w * 0.8, h * 0.6))
#     tri_img.save(triname)
#     print("Trimmed filename : {}".format(triname))
#     return triname

def execute(firebase_client, imgpath, save_dir, collection_name):
    # GCP Object Loclizerを呼び出して結果を取得
    detected_texts = ocr.recognize_text(imgpath)
    # 結果表示
    img_width = ocr.view_results(imgpath, save_dir, detected_texts)
    post_data = record_detector.get_detected_record(detected_texts, img_width)
    
    # firebase clientで書き込み
    firebase_client.set_firebase(collection_name, post_data)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Err : collection_name, and save_dir is not set.")
        sys.exit(1)
    collection_name = sys.argv[1]
    save_dir = sys.argv[2]
    #execute(take_photo(), save_dir, collection_name)
    imgpath = sys.argv[3]
    fcli = firebase_client.Firebase_client()
    while True:
        execute(fcli, imgpath, save_dir, collection_name)
        time.sleep(15)