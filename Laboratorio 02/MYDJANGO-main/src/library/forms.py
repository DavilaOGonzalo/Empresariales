from django import forms

from .models import Libro


class LibroForm(forms.ModelForm):
    """Formulario de creacion y edicion conectado al modelo Libro."""

    class Meta:
        model = Libro
        fields = ["titulo", "autor", "categoria", "disponible"]
        labels = {"titulo": "Titulo", "categoria": "Categoria"}
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-input", "placeholder": "Ingrese el titulo del libro"}),
            "autor": forms.TextInput(attrs={"class": "form-input", "placeholder": "Ingrese el nombre del autor"}),
            "categoria": forms.TextInput(attrs={"class": "form-input", "placeholder": "Ingrese la categoria"}),
            "disponible": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }
