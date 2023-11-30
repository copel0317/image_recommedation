import googletrans

translator = googletrans.Translator()

def translate(text: str) -> str:
    try:
        Translated = translator.translate(text, dest='ko')
        if Translated.dest == "ko":
            return Translated.text
    except Exception as e:       
        return f"'translating error occured' : {e} 'entered : {text}'"
