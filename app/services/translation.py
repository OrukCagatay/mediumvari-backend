from deep_translator import GoogleTranslator


LANGUAGE_CODE_MAP = {
    "en": "en",
    "tr": "tr",
    "fr": "fr",
    "de": "de",
}

MAX_CHUNK_SIZE = 1500


class TranslationError(Exception):
    """Çeviri işlemi başarısız olduğunda fırlatılır."""
    pass


def _split_into_chunks(text: str, max_size: int) -> list[str]:
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 <= max_size:
            current_chunk = f"{current_chunk}\n\n{paragraph}" if current_chunk else paragraph
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def translate_text(text: str, source_language: str, target_language: str) -> str:
    source_code = LANGUAGE_CODE_MAP.get(source_language, "auto")
    target_code = LANGUAGE_CODE_MAP.get(target_language)

    if target_code is None:
        raise TranslationError(f"Unsupported target language: {target_language}")

    try:
        translator = GoogleTranslator(source=source_code, target=target_code)

        if len(text) <= MAX_CHUNK_SIZE:
            return translator.translate(text)

        chunks = _split_into_chunks(text, MAX_CHUNK_SIZE)
        translated_chunks = [translator.translate(chunk) for chunk in chunks]
        return "\n\n".join(translated_chunks)

    except Exception as e:
        raise TranslationError(f"Translation failed: {str(e)}")


def translate_post_content(
    title: str,
    content: str,
    source_language: str,
    target_language: str,
) -> tuple[str, str]:
    translated_title = translate_text(title, source_language, target_language)
    translated_content = translate_text(content, source_language, target_language)
    return translated_title, translated_content