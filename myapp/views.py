from django.http import JsonResponse
from google.cloud import translate_v2 as translate
import os
import google.generativeai as genai

# Replace with your API key
api_key = "AIzaSyDFfv9bSCsmELltZ_Id9SK8mk2BRlcTmfY"

# Configure the API key
genai.configure(api_key=api_key)

# Function to translate text from Shona to English
def translate_shona_to_english(shona_text, credentials_file):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
    translate_client = translate.Client()
    translation = translate_client.translate(shona_text, source_language='sn', target_language='en')
    english_translation = translation['translatedText']

    prompt = f"Provide a list of synonyms for the word '{english_translation}' in the context of its use as a noun."

    response = genai.generate_text(
        prompt=prompt,
    )
    synonyms = response.result.split("\n")

    return [english_translation, synonyms]

# Function to translate text from English to Shona
def translate_english_to_shona(english_text, credentials_file):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
    translate_client = translate.Client()
    translation = translate_client.translate(english_text, source_language='en', target_language='sn')
    shona_translation = translation['translatedText']
    return shona_translation

def translate_view(request):
    shona_text = request.GET.get('text')
    credentials_file = "./abc.json"
    english_text, synonyms = translate_shona_to_english(shona_text, credentials_file)

    return JsonResponse({
        'translated_text': english_text,
        'synonyms': synonyms
    })

def summarise_view(request):
    shona_text = request.GET.get('text')
    credentials_file = "./abc.json"
    english_text = translate_shona_to_english(shona_text, credentials_file)[0]

    prompt = f"Summarize the following statement to 50 words: {english_text}"
    response = genai.generate_text(
        prompt=prompt,
    )
    summary = response.result

    translated_summary = translate_english_to_shona(summary, credentials_file)

    return JsonResponse({'summarised_text': translated_summary})

def paraphrase_view(request):
    shona_text = request.GET.get('text')
    credentials_file = "./abc.json"
    english_text = translate_shona_to_english(shona_text, credentials_file)[0]

    prompt = f"Paraphrase the following statement: {english_text}"
    response = genai.generate_text(
        prompt=prompt,
    )
    paraphrased_text = response.result

    translated_paraphrase = translate_english_to_shona(paraphrased_text, credentials_file)

    return JsonResponse({'paraphrased_text': translated_paraphrase})
