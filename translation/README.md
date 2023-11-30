# translation

/translation 에 json 형태로 post 요청
{ 
    "text" : text (to translate)
    "translation_service" : (google / mozilla / papago)
}
# return json
return {
        "original_text" : text, 
        "translated_text" : translated_text,
        "translation_service" : translation_service.lower()
    }
