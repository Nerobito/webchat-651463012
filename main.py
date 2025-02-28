import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from aift import setting
from aift.nlp.longan import tokenizer
from aift.multimodal import textqa
from aift.nlp.translation import en2th
from aift.nlp.translation import zh2th
from aift.nlp.translation import th2zh
from aift.nlp import ner
from aift.nlp import soundex

from dotenv import load_dotenv



# โหลดตัวแปรจาก .env
load_dotenv()

# ตั้งค่า API Key จาก .env
setting.set_api_key(os.getenv("AIFORTHAI_API_KEY"))

app = FastAPI()

# อนุญาตให้ React เรียก API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/tokenize")
async def tokenize_text(request: TextRequest):
    tokens = tokenizer.tokenize(request.text)
    return {"tokens": tokens}


@app.post("/textqa")
async def qa_text(request: TextRequest):
    response = textqa.generate(request.text)
    return {"answer": response["content"]}

@app.post("/en2th")
async def en2th_text(request: TextRequest):
    response = en2th.translate(request.text)
    return {"translate": response}

@app.post("/th2zh")
async def th2zh_text(request: TextRequest):
    response = th2zh.translate(request.text)
    return {"translate": response}


@app.post("/zh2th")
async def zh2th_text(request: TextRequest):
    response = zh2th.translate(request.text)
    return {"translate": response}


@app.post("/ner")
async def ner_text(request: TextRequest):
    try:
        response = ner.analyze(request.text)
        return {"entities": response}
    except Exception as e:
        return {"error": f"NER Error: {str(e)}"}
    





