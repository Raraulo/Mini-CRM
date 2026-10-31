from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse
from datetime import timedelta
from django.db.models.functions import TruncDate
from django.utils import timezone

from .forms import ClientForm
from .models import Client


# Consultas del listado, filtros, métricas y datos para los gráficos.
def dashboard_context(request, form=None, editing=None):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    clients = Client.objects.all()
    if query:
        clients = clients.filter(Q(name__icontains=query) | Q(company__icontains=query))
    if status in Client.Status.values:
        clients = clients.filter(status=status)
    metrics = Client.objects.aggregate(
        total=Count('pk'), prospects=Count('pk', filter=Q(status='prospect')),
        customers=Count('pk', filter=Q(status='customer')),
        inactive=Count('pk', filter=Q(status='inactive')),
    )
    today = timezone.localdate()
    start = today - timedelta(days=29)
    registrations = dict(Client.objects.annotate(day=TruncDate('created_at')).filter(
        day__gte=start, day__lte=today,
    ).values('day').annotate(count=Count('pk')).values_list('day', 'count'))
    chart_data = {
        'statuses': [metrics['customers'], metrics['prospects'], metrics['inactive']],
        'days': [{'date': (start + timedelta(days=i)).isoformat(),
                  'count': registrations.get(start + timedelta(days=i), 0)} for i in range(30)],
    }
    return {'clients': clients, 'metrics': metrics, 'query': query,
            'selected_status': status, 'statuses': Client.Status.choices,
            'form': form if form is not None else ClientForm(), 'editing': editing,
            'open_form': form is not None, 'chart_data': chart_data}


@login_required
@never_cache
@require_GET
def dashboard(request):
    return render(request, 'clients/dashboard.html', dashboard_context(request))


@login_required
@require_POST
def create(request):
    # Valida y guarda un contacto; si falla, conserva el modal y sus errores.
    form = ClientForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente registrado correctamente.')
        return redirect('clients:dashboard')
    return TemplateResponse(request, 'clients/dashboard.html', dashboard_context(request, form), status=400)


@login_required
@require_POST
def update(request, pk):
    # Busca el contacto y aplica los mismos campos y validaciones del alta.
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST, instance=client)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cambios guardados correctamente.')
        return redirect('clients:dashboard')
    return TemplateResponse(request, 'clients/dashboard.html', dashboard_context(request, form, client), status=400)


@login_required
@require_POST
def delete(request, pk):
    # Solo se elimina mediante POST y con una sesión válida.
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    messages.success(request, 'Cliente eliminado correctamente.', extra_tags='deleted')
    return redirect('clients:dashboard')

