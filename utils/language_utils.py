from langdetect import detect


def is_english_query(text):
    try:
        return detect(text) == "en"
    except Exception:
        return True
