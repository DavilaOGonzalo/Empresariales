from django.test import TestCase
from django.urls import reverse

from .models import Libro


class LibroViewsTests(TestCase):
    def test_listado_muestra_libros_guardados_en_orm(self):
        Libro.objects.create(
            titulo="Django para empresas",
            autor="Ana Perez",
            categoria="Tecnologia",
            disponible=True,
        )

        response = self.client.get(reverse("lista_libros"))

        self.assertContains(response, "Django para empresas")

    def test_crear_libro_persiste_y_redirige_al_listado(self):
        response = self.client.post(reverse("crear_libro"), {
            "titulo": "Persistencia con SQLite",
            "autor": "Luis Gomez",
            "categoria": "Tecnologia",
            "disponible": "on",
        })

        self.assertRedirects(response, reverse("lista_libros"))
        self.assertTrue(Libro.objects.filter(titulo="Persistencia con SQLite").exists())
