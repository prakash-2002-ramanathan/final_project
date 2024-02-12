from deep_translator import GoogleTranslator

def translate_text_to_language(text, lang, source_lang='en'):
    try:
        translation = GoogleTranslator(source=source_lang, target=lang).translate(text)
        return translation
    except Exception as e:
        # Handle the exception or print an error message
        #print(e)
        return None


#print(translate_text_to_language("soil type", "hi", "en"))


