from django.utils import translation


class AcceptLanguageMiddleware:
    """Set language from Accept-Language header or user preference."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            lang = getattr(request.user, 'preferred_language', None)
            if lang:
                translation.activate(lang)
                request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        return response
