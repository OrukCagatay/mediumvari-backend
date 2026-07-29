class GeminiAPIError(Exception):
    """Gemini API'den beklenmedik bir hata döndü."""
    pass


class GeminiTimeoutError(Exception):
    """Gemini API zamanında yanıt vermedi."""
    pass


class GeminiEmptyResponseError(Exception):
    """Gemini boş veya geçersiz içerik döndürdü."""
    pass


class AIQuotaExceededError(Exception):
    """Kullanıcının günlük AI kullanım kotası doldu."""
    pass