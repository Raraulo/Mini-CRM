from django.contrib import admin
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .forms import ClientForm
from .models import Client


# Pruebas de campos, validaciones y persistencia.
class ClientTests(TestCase):
    def setUp(self):
        Client.objects.all().delete()

    def test_client_persists_with_required_fields(self):
        client = Client.objects.create(name=' Ana ', company='Aurora', phone='0991234567', email='ana@example.com')
        client.refresh_from_db()
        self.assertEqual(client.name, 'Ana')
        self.assertEqual(client.status, Client.Status.PROSPECT)
        self.assertEqual(client.phone, '0991234567')
        self.assertIsNotNone(client.created_at)
        self.assertIsNotNone(client.updated_at)

    def test_invalid_data_is_rejected_before_saving(self):
        for field, value in [('name', '   '), ('name', 'Ana123'), ('email', 'incorrecto'),
                             ('status', 'desconocido'), ('phone', 'abcdefghi')]:
            with self.subTest(field=field):
                values = {'name': 'Ana', 'email': 'ana@example.com', 'company': 'Aurora', 'phone': '0991234567', field: value}
                with self.assertRaises(ValidationError) as error:
                    Client.objects.create(**values)
                self.assertIn(field, error.exception.message_dict)
        self.assertEqual(Client.objects.count(), 0)

    def test_form_validates_and_saves_phone(self):
        form = ClientForm(data={
            'name': 'Ana', 'email': 'ana@example.com', 'company': 'Aurora',
            'phone': '+593 99 123-4567', 'status': 'customer',
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().status, Client.Status.CUSTOMER)

    def test_model_registered_in_admin(self):
        self.assertIn(Client, admin.site._registry)

    def test_company_and_phone_are_optional_in_model_and_form(self):
        form = ClientForm(data={'name': 'Juan Pérez', 'email': 'juan@example.com', 'status': 'prospect'})
        self.assertTrue(form.is_valid(), form.errors)
        client = form.save()
        client.refresh_from_db()
        self.assertEqual(client.company, '')
        self.assertEqual(client.phone, '')
        client = Client.objects.create(name='Ana', email='ana@example.com')
        self.assertEqual(client.company, '')
        self.assertEqual(client.phone, '')


# Pruebas de listado, filtros y operaciones CRUD con sesión.
class DashboardTests(TestCase):
    def setUp(self):
        Client.objects.all().delete()
        from django.contrib.auth import get_user_model
        self.user = get_user_model().objects.create_user(username='tester', password='Test-password-482!')
        self.client.force_login(self.user)
        self.client_record = Client.objects.create(
            name='Ana Pérez', company='Estudio Norte', email='ana@example.com', phone='0991234567',
        )

    def test_dashboard_renders_and_filters_with_metrics(self):
        Client.objects.create(name='Luis', company='Sur', phone='0991234567', email='luis@example.com', status='customer')
        response = self.client.get(reverse('clients:dashboard'), {'q': 'Norte', 'status': 'prospect'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana Pérez')
        self.assertEqual(list(response.context['clients']), [self.client_record])
        self.assertEqual(response.context['metrics']['total'], 2)
        self.assertEqual(response.context['metrics']['customers'], 1)

    def test_create_update_and_delete(self):
        data = {'name': 'María', 'email': 'maria@example.com', 'company': 'Aurora', 'phone': '0991234567', 'status': 'customer'}
        response = self.client.post(reverse('clients:create'), data)
        self.assertRedirects(response, reverse('clients:dashboard'))
        record = Client.objects.get(email='maria@example.com')
        data['name'] = 'María López'
        response = self.client.post(reverse('clients:update', args=[record.pk]), data)
        self.assertRedirects(response, reverse('clients:dashboard'))
        record.refresh_from_db()
        self.assertEqual(record.name, 'María López')
        response = self.client.post(reverse('clients:delete', args=[record.pk]))
        self.assertRedirects(response, reverse('clients:dashboard'))
        self.assertFalse(Client.objects.filter(pk=record.pk).exists())

    def test_invalid_form_shows_errors_without_writing(self):
        response = self.client.post(reverse('clients:create'), {
            'name': ' ', 'email': 'incorrecto', 'status': 'unknown',
        })
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.context['form'].errors)
        self.assertContains(response, 'data-reopen="true"', status_code=400)
        self.assertEqual(Client.objects.count(), 1)

    def test_mutations_reject_get_and_csrf_is_enforced(self):
        from django.test import Client as HttpClient
        for url in [reverse('clients:create'),
                    reverse('clients:update', args=[self.client_record.pk]),
                    reverse('clients:delete', args=[self.client_record.pk])]:
            self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(HttpClient(enforce_csrf_checks=True).post(reverse('clients:create'), {}).status_code, 403)

    def test_invalid_update_keeps_modal_and_does_not_modify_client(self):
        response = self.client.post(
            reverse('clients:update', args=[self.client_record.pk]),
            {'name': 'Ana123', 'company': 'Norte', 'email': 'incorrecto',
             'phone': 'abc', 'status': 'prospect'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'clients/dashboard.html')
        self.assertContains(response, 'data-reopen="true"', status_code=400)
        self.assertIn('name', response.context['form'].errors)
        self.client_record.refresh_from_db()
        self.assertEqual(self.client_record.name, 'Ana Pérez')

    def test_client_content_is_escaped(self):
        self.client_record.company = '<script>alert(1)</script>'
        self.client_record.save()
        response = self.client.get(reverse('clients:dashboard'))
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertContains(response, '&lt;script&gt;alert(1)&lt;/script&gt;')


# Comprueba cantidades y que la carga de ejemplo no sobrescriba contactos.
class DemoDataTests(TestCase):
    def test_seed_counts_and_preserves_existing_contact(self):
        from importlib import import_module
        from types import SimpleNamespace
        from django.apps import apps
        from django.db import connection

        Client.objects.all().delete()
        seed = import_module('clients.migrations.0002_contactos_prueba').cargar_contactos
        editor = SimpleNamespace(connection=connection)
        seed(apps, editor)
        self.assertEqual(Client.objects.count(), 10)
        self.assertEqual(Client.objects.filter(status='customer').count(), 5)
        self.assertEqual(Client.objects.filter(status='prospect').count(), 3)
        self.assertEqual(Client.objects.filter(status='inactive').count(), 2)
        record = Client.objects.get(email='ana.torres@example.com')
        record.name = 'Nombre editado'
        record.save()
        seed(apps, editor)
        self.assertEqual(Client.objects.count(), 10)
        record.refresh_from_db()
        self.assertEqual(record.name, 'Nombre editado')



# Pruebas de acceso, login, logout y páginas de error.
class AuthenticationTests(TestCase):
    def test_unknown_url_shows_friendly_404(self):
        response = self.client.get('/direccion-inexistente/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/error.html')
        self.assertContains(response, 'Página no encontrada', status_code=404)
        self.assertContains(response, 'lotties/mantenimiento.json', status_code=404)

    def test_csrf_failure_shows_friendly_error(self):
        from django.test import Client as HttpClient
        response = HttpClient(enforce_csrf_checks=True).post(reverse('login'), {})
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/error.html')
        self.assertContains(response, 'Acceso no permitido', status_code=403)

    def test_anonymous_cannot_read_or_mutate_clients(self):
        for url in [reverse('clients:dashboard'), reverse('clients:create'),
                    reverse('clients:update', args=[1]), reverse('clients:delete', args=[1])]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse('login') + '?next='))
                response = self.client.post(url, {'name': 'Intruso'})
                self.assertEqual(response.status_code, 302)

    def test_login_identity_and_logout(self):
        from django.contrib.auth import get_user_model
        user = get_user_model().objects.create_user(username='adminprueba', password='Test-password-482!')
        response = self.client.post(reverse('login'), {'username': user.username, 'password': 'incorrecta'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        response = self.client.post(reverse('login'), {'username': user.username, 'password': 'Test-password-482!'})
        self.assertRedirects(response, reverse('clients:dashboard'))
        self.assertContains(self.client.get(reverse('clients:dashboard')), 'adminprueba')
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        self.assertRedirects(self.client.post(reverse('logout')), reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_does_not_redirect_to_external_site(self):
        from django.contrib.auth import get_user_model
        get_user_model().objects.create_user(username='tester', password='Test-password-482!')
        response = self.client.post(reverse('login'), {
            'username': 'tester', 'password': 'Test-password-482!', 'next': 'https://example.com/',
        })
        self.assertRedirects(response, reverse('clients:dashboard'))
