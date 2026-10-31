from django import forms

from .models import Client


# Formulario compartido por crear y editar; hereda las reglas del modelo.
class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['aria-describedby'] = f'id_{name}_errors'
            if self.is_bound and name in self.errors:
                field.widget.attrs['aria-invalid'] = 'true'
        self.fields['name'].widget.attrs['autocomplete'] = 'name'
        self.fields['email'].widget.attrs['autocomplete'] = 'email'
        self.fields['company'].widget.attrs['autocomplete'] = 'organization'
        self.fields['phone'].widget.attrs.update({'autocomplete': 'tel', 'type': 'tel'})
        # Ejemplos visuales: orientan al usuario, nunca se guardan como valores.
        examples = {
            'name': 'Ej. Juan Pérez', 'company': 'Ej. Estudio Aurora',
            'email': 'Ej. juan@empresa.com', 'phone': 'Ej. 0991234567',
        }
        for name, example in examples.items():
            self.fields[name].widget.attrs['placeholder'] = example
        self.fields['phone'].widget.attrs['pattern'] = r'\+?[0-9][0-9 \(\)\-]{5,28}[0-9]'
        self.fields['phone'].widget.attrs['title'] = 'Sin letras. De 7 a 30 caracteres; puedes usar + al inicio, espacios, paréntesis y guiones.'

    # Lista explícita de campos editables; las fechas quedan fuera.
    class Meta:
        model = Client
        fields = ['name', 'company', 'email', 'phone', 'status']
