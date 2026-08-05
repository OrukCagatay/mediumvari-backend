from langdetect import detect, LangDetectException


SUPPORTED_LANGUAGES = {"en", "tr", "fr", "zh-cn"}


def detect_language(text: str) -> str:
    try:
        detected = detect(text)
    except LangDetectException:
        return "en"  # tespit edilemezse varsayılan İngilizce

    # langdetect Çince için "zh-cn" / "zh-tw" gibi kodlar dönebilir, normalize edelim
    if detected.startswith("zh"):
        return "zh-cn"

    if detected not in SUPPORTED_LANGUAGES:
        return "en"  # desteklemediğimiz bir dilse, varsayılana düş

    return detected