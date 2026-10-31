# Intercepta errores generales y conserva los errores de validación del formulario.

from .error_views import error_page


class FriendlyErrorsMiddleware:
    """Presenta errores amigables también en el entorno local con DEBUG."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Un formulario inválido ya tiene una respuesta útil con sus errores.
        context = getattr(response, 'context_data', None) or {}
        form = context.get('form')
        if response.status_code == 400 and form is not None and form.is_bound and form.errors:
            return response
        if response.status_code in (400, 403, 404, 405, 500):
            friendly = error_page(request, response.status_code)
            if response.has_header('Allow'):
                friendly['Allow'] = response['Allow']
            return friendly
        return response
