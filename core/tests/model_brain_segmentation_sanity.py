import base64
import os
import requests
import json
from PIL import Image
from io import BytesIO
from skimage.io import imsave
import cv2
import numpy as np
import matplotlib.pyplot as plt

samples = "./samples/"

requests_session = requests.Session()
server = "http://192.168.0.103:8000/segmentation" #"http://127.0.0.1:8000/segmentation"


for subdir, dirs, files in os.walk(samples):
    for f in files:
        path = subdir + f
        print(path)

        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        payload = {
            "image_b64": encoded_string,
        }

        r = requests_session.post(server, json=payload, timeout=60)

        data = json.loads(r.text)
        output = data["answer"]["hip"]

        #print(output.values())
        bools = [False if b == {} else True for b in list(output.values())]
        if any(bools): 
            for source in output:
                string = output[source]['segmentation']
                decoded = base64.b64decode(string)
                decoded = BytesIO(decoded)
                img = Image.open(decoded)
                plt.imshow(img)
                plt.show()
        
        