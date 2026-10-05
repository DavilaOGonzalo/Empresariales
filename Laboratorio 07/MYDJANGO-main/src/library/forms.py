from django import forms

from .models import Libro, Prestamo


class LibroForm(forms.ModelForm):
    """Formulario de creacion y edicion conectado al modelo Libro."""

    existencias = forms.IntegerField(
        min_value=0,
        required=False,
        label="Ejemplares disponibles",
    )

    class Meta:
        model = Libro
        fields = ["titulo", "autor", "categoria", "existencias"]
        labels = {"titulo": "Titulo", "categoria": "Categoria"}
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-input", "placeholder": "Ingrese el titulo del libro"}),
            "autor": forms.TextInput(attrs={"class": "form-input", "placeholder": "Ingrese el nombre del autor"}),
            "categoria": forms.TextInput(attrs={"class": "form-input", "placeholder": "Ingrese la categoria"}),
            "existencias": forms.NumberInput(attrs={"class": "form-input", "min": 0}),
        }

    def clean_existencias(self):
        valor = self.cleaned_data.get("existencias")
        if valor is not None:
            return valor
        if self.instance.pk:
            return self.instance.existencias
        return 5

    def clean(self):
        cleaned_data = super().clean()
        if "existencias" in cleaned_data:
            self.instance.disponible = cleaned_data["existencias"] > 0
        return cleaned_data


class PrestamoForm(forms.ModelForm):
    """Formulario para administrar la relación entre libros y socios."""

    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        required=False,
        label="Cantidad de ejemplares",
    )
    monto = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        initial=0,
        required=False,
        label="Monto",
    )

    class Meta:
        model = Prestamo
        fields = [
            "libro",
            "socio",
            "fecha_prestamo",
            "fecha_devolucion",
            "estado",
            "cantidad",
            "monto",
        ]
        widgets = {
            "fecha_prestamo": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "fecha_devolucion": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "estado": forms.TextInput(attrs={"class": "form-input"}),
            "libro": forms.Select(attrs={"class": "form-input"}),
            "socio": forms.Select(attrs={"class": "form-input"}),
        }

    def clean_cantidad(self):
        return self.cleaned_data.get("cantidad") or 1

    def clean_monto(self):
        return self.cleaned_data.get("monto") or 0
