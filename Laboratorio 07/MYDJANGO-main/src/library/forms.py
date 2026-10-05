from django import forms

from .models import Libro, Prestamo


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


class PrestamoForm(forms.ModelForm):
    """Formulario para administrar la relación entre libros y socios."""

    class Meta:
        model = Prestamo
        fields = ["libro", "socio", "fecha_prestamo", "fecha_devolucion", "estado"]
        widgets = {
            "fecha_prestamo": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "fecha_devolucion": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "estado": forms.TextInput(attrs={"class": "form-input"}),
            "libro": forms.Select(attrs={"class": "form-input"}),
            "socio": forms.Select(attrs={"class": "form-input"}),
        }
