from googletrans import Translator


def g_translate(text, lang):
    """
    Function to translate text from English to the specified language using Google Translate API.

    Args:
        text (str): The text to be translated.
        lang (str): The target language code for translation.

    Returns:
        str: The translated text.
    """

    translator = Translator()

    # Split the text into parts (sentences)
    text_parts = text.split('. ')
    translated_text = []

    # Translate each part separately
    for parts in text_parts:
        translated_text.append(translator.translate(parts, src='en', dest=lang).text)

    # Join the translated parts and add a period at the end
    return ' '.join(translated_text) + '.'
