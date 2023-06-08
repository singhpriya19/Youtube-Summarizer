import re
import nltk
import spacy
from string import punctuation
from transcript import get_transcript_of_yt_video
from translate import g_translate
from download import makeTextFile

nltk.download('stopwords')

def text_summarizer(text):
    """
    Function to summarize the given text.

    Args:
        text (str): The input text to be summarized.

    Returns:
        str: The summarized text.
    """

    from heapq import nlargest
    from nltk.corpus import stopwords

    nlp = spacy.load('en_core_web_sm')
    stop_words = stopwords.words('english')

    doc = nlp(text)

    # Calculate word frequencies
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stop_words:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    # Normalize word frequencies
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    # Split the text into sentences
    sentence_tokens = [sent for sent in doc.sents]

    # Calculate sentence scores
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Select top sentences for the summary
    select_length = int(len(sentence_tokens) * 0.3)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

    # Format the summary sentences
    summary = [re.sub('[.]', '', (word.text).replace("\n", ",").strip()).capitalize() for word in summary]
    final_text = '. '.join(summary)

    # Clean up the final summary
    final_summary = re.sub(',,|,\.|,\-|[\"]', '', final_text)

    return final_summary


def nlp_model(v_id):
    """
    Function to perform NLP tasks on a YouTube video transcript.

    Args:
        v_id (str): The YouTube video ID.

    Returns:
        tuple or str: A tuple containing the length of original text, length of final summary,
                      English summary, Hindi translated summary, and Gujarati translated summary.
                      If the transcript is not available, returns '0'.
    """

    transcript = get_transcript_of_yt_video(v_id)

    if transcript == '0':
        return '0'
    else:
        transcript_size = len(transcript)

        original_text = ' '.join([t['text'] for t in transcript])
        original_text_length = len(original_text)

        s_t = []

        result = ""

        for txt in range(0, transcript_size):
            if txt != 0 and txt % 100 == 0:
                result += ' ' + transcript[txt]['text']
                s_t.append(text_summarizer(result))
                result = ""
            else:
                result += ' ' + transcript[txt]['text']

            if txt == transcript_size - 1:
                result += ' ' + transcript[txt]['text']
                s_t.append(text_summarizer(result))

        english_summary = ' '.join(s_t) + '.'

        final_summary_length = len(english_summary)

        hindi_translated_summary = g_translate(english_summary, 'hi')

        gujarati_translated_summary = g_translate(english_summary, 'gu')

        makeTextFile("English", english_summary)
        makeTextFile("Hindi", hindi_translated_summary)
        makeTextFile("Gujarati", gujarati_translated_summary)

        return original_text_length, final_summary_length, english_summary, hindi_translated_summary, gujarati_translated_summary
