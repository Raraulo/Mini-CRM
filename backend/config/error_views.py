# Respuestas de error con mensajes y plantilla compartidos.

from django.shortcuts import render
from django.utils.cache import patch_cache_control


def error_page(request, status=404):
    titles = {
        400: ('Solicitud no válida', 'No pudimos procesar esta solicitud. Vuelve al inicio e inténtalo de nuevo.'),
        403: ('Acceso no permitido', 'La sesión o el permiso de esta solicitud no es válido. Vuelve a iniciar sesión para continuar.'),
        404: ('Página no encontrada', 'Esta dirección no existe o el recurso ya no está disponible.'),
        405: ('Acción no permitida', 'Abre el CRM y utiliza sus botones para realizar esta acción.'),
        500: ('Algo salió mal', 'No pudimos completar la operación. Inténtalo de nuevo en unos momentos.'),
    }
    title, description = titles.get(status, titles[500])
    response = render(request, 'errors/error.html', {
        'error_code': status, 'error_title': title, 'error_description': description,
    }, status=status)
    patch_cache_control(response, no_store=True, private=True)
    return response


def bad_request(request, exception):
    return error_page(request, 400)


def permission_denied(request, exception):
    return error_page(request, 403)


def not_found(request, exception):
    return error_page(request, 404)


def server_error(request):
    return error_page(request, 500)


def csrf_failure(request, reason=''):
    return error_page(request, 403)
