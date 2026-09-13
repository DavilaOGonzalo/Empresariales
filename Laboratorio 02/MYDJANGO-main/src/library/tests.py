from django.test import TestCase
from django.urls import reverse

from .models import Editorial, FichaLibro, Libro, Prestamo, Socio


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


class RelacionesViewsTests(TestCase):
    def setUp(self):
        self.editorial = Editorial.objects.create(nombre="Editorial de prueba")
        self.socio = Socio.objects.create(nombre="Socio de prueba", correo="socio@test.local")
        self.libro = Libro.objects.create(
            titulo="Relaciones con Django",
            autor="Autor de prueba",
            categoria="Tecnologia",
            editorial=self.editorial,
        )
        FichaLibro.objects.create(libro=self.libro, ubicacion="Sala C")

    def test_relaciones_optimizadas_muestran_datos(self):
        self.assertEqual(self.client.get(reverse("relaciones_select")).status_code, 200)
        self.assertEqual(self.client.get(reverse("relaciones_prefetch")).status_code, 200)

    def test_crud_del_modelo_intermedio(self):
        response = self.client.post(reverse("crear_prestamo"), {
            "libro": self.libro.id,
            "socio": self.socio.id,
            "fecha_prestamo": "2026-09-13",
            "fecha_devolucion": "",
            "estado": "Activo",
        })

        self.assertRedirects(response, reverse("lista_prestamos"))
        prestamo = Prestamo.objects.get(libro=self.libro, socio=self.socio)
        self.assertEqual(self.client.get(reverse("editar_prestamo", args=[prestamo.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("eliminar_prestamo", args=[prestamo.id])).status_code, 200)
