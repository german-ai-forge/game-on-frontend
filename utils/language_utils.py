from langdetect import detect, LangDetectException


def is_english_query(text: str) -> bool:
    try:
        return detect(text) == "en"
    except LangDetectException:
        return False
