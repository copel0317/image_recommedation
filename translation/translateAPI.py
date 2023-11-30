from fastapi import FastAPI, HTTPException, Body
from translators import google, papago
from transformers import pipeline
import uvicorn
import requests


app = FastAPI()
pipe = pipeline("text2text-generation", model="QuoQA-NLP/KE-T5-En2Ko-Base")

@app.get('/test')
def return_hello():
    return {"message": "hello"}

@app.post('/translation')
def translate(text: str = Body(..., description="The text to be translated"), 
              translation_service : str = Body(..., description="The translation service to use ('google', 'papago', 'model')")):
    
    if translation_service.lower() == "google" :
        translated_text = google.translate(text)
    elif translation_service.lower() == "papago" :
        translated_text = papago.translate(text)
    elif translation_service.lower() == "model" : 
        response = requests.get("http://localhost:8895/model", json={"text": text})
        translated_text = response.json()["translated_text"]
    else :
        raise HTTPException(
            status_code= 400, 
            detail = f"'translation_service'(query parameter) must be one of 'google', 'papago', model', input 'translation_service' : {translation_service}"
        )
    
    return {
        "original_text" : text, 
        "translated_text" : translated_text,
        "translation_service" : translation_service.lower()
    }


@app.get('/model')
def modeltranslate(text: str = Body(..., title="Text to translate"), max_length: int = Body(1000, title="Maximum Length")):
    return {
        "translated_text" : pipe(text,max_length)[0]['generated_text'],
    }


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8895)
