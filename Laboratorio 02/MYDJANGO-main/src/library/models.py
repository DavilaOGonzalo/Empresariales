from django.db import models


class Libro(models.Model):
    """Libro almacenado de forma persistente en la base de datos."""

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.titulo} - {self.autor}"
