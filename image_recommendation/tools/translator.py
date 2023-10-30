import googletrans             #googletrans 3.1.0a0이 아닐 경우 오류 발생.
                                #pip uninstall googletrans
                                #pip install googletrans==3.1.0a0 
        
        
translator = googletrans.Translator()

def translatetoKr(description):
    description = translator.translate(description, dest='ko', src='auto').text
    return description

def translatetoEn(description):
    description = translator.translate(description, dest='en', src='auto').text
    return description
