import os

from fastapi import FastAPI

from proto import QuestionProto, ImageProto, NLPProto
from proxy import Proxy, Filter
from mocks import generate_mocks
from nlp import NLP

app = FastAPI()
proxy = Proxy()
nlp = NLP()

for hip_mock in generate_mocks():
    proxy.register(hip_mock)


@app.get("/sources")
def get_sources():
    return proxy.sources()


@app.get("/capabilities")
def get_sources():
    return proxy.capabilities()


@app.post("/vqa")
def vqa_task(q: QuestionProto):
    try:
        prefilter = proxy.prefilter(q.image_b64)
        if not prefilter["valid"]:
            return {"error": "imagen inválida"}

        result = proxy.ask(q.question, q.image_b64, prefilter["topic"])
        result = proxy.aggregate(result)
        return {"answer": result}
    except BaseException as e:
        return {"error": str(e)}


@app.post("/segmentation")
def segmentation_task(q: ImageProto):
    try:
        prefilter = proxy.prefilter(q.image_b64)
        if not prefilter["valid"]:
            return {"error": "imagen inválida"}

        result = proxy.segment(q.image_b64, prefilter["topic"])
        return {"answer": result}
    except BaseException as e:
        return {"error": str(e)}


@app.post("/prefilter")
def prefilter_task(q: ImageProto):
    try:
        
        result = proxy.prefilter(q.image_b64)
        
        if not result["valid"]:
            return {"answer": result}

        result["anomalies"] = proxy.anomalies(q.image_b64, result["topic"])

        return {"answer": result}
    except BaseException as e:
        return {"error": str(e)}


@app.post("/nlp")
def nlp_task(q: NLPProto):
    try:
        return {"answer": nlp.ask(q.data)}
    except BaseException as e:
        return {"error": str(e)}

