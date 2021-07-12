import base64
import json
from pathlib import Path

import requests

model_root = Path("../models/model_vqa/MICCAI19-MedVQA")

data = json.load(open(model_root / "data_RAD/testset.json"))
img_folder = model_root / "data_RAD/images/"

questions = {}
for entry in data:
    if entry["image_organ"] not in questions:
        questions[entry["image_organ"]] = []

    question = entry["question"]
    filename = img_folder / entry["image_name"]

    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    obj = {
        "image_b64": encoded_string,
        "name": entry["image_name"],
        "question": question,
        "expected_answer": entry["answer"],
    }
    questions[entry["image_organ"]].append(obj)

fail = 0
ok = 0
total = 0

requests_session = requests.Session()
server = "http://192.168.0.103:8000"

for tag in questions:
    if tag != "HEAD" and tag != "CHEST":
        continue

    for q in questions[tag]:
        payload = {
            "image_b64": q["image_b64"],
        }
        r = requests_session.post(server + "/prefilter", json=payload, timeout=60)

        data = json.loads(r.text)
        #print(data)
        result = data["answer"]

        # en caso no sea una imagen médica la ignoramos
        if not result["valid"]: 
            continue

        payload = {
            "question": q["question"],
            "image_b64": q["image_b64"],
        }
        r = requests_session.post(server + "/vqa", json=payload, timeout=60)

        data = json.loads(r.text)
        #print(data)
        result = data["answer"]

        matching = 0
        for hospital in result["hip"]:
            expected = str(q["expected_answer"]).lower()
            actual = str(result["hip"][hospital]["vqa"]).lower()
            if expected == actual:
                matching += 1

        total += 1
        if matching == 0:
            fail += 1
            print("\nFALLA: ", q["name"], "||  Respuesta esperada: ", q["expected_answer"], "||  Respuesta resultado: ",result)
        else:
            ok += 1
            print("\nOK: ", q["name"], "||  Pregunta: ", q["question"], "||  Respuesta resultado: ", expected)

print("Total ", total)
print("ok ", ok)
print("failed ", fail)
