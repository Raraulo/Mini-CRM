"""Los permisos del CRM son los mismos permisos del modelo usados por Admin."""
from functools import wraps

from django.template.response import TemplateResponse


def client_permission_required(permission):
    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not request.user.has_perm(permission):
                from .views import dashboard_context
                context = dashboard_context(request)
                context['permission_denied'] = True
                return TemplateResponse(request, 'clients/dashboard.html', context, status=403)
            return view(request, *args, **kwargs)
        return wrapped
    return decorator
