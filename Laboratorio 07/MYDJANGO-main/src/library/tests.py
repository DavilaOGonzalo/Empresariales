from django.db import connection, reset_queries
from django.test import TestCase, override_settings
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
        libro = Libro.objects.get(titulo="Persistencia con SQLite")
        self.assertEqual(libro.existencias, 5)
        self.assertTrue(libro.disponible)


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
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.existencias, 4)
        self.assertEqual(self.client.get(reverse("editar_prestamo", args=[prestamo.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("eliminar_prestamo", args=[prestamo.id])).status_code, 200)

    def test_falta_de_existencias_revierte_toda_la_operacion(self):
        self.libro.existencias = 0
        self.libro.disponible = False
        self.libro.save(update_fields=["existencias", "disponible"])
        prestamos_antes = Prestamo.objects.count()
        libros_antes = Libro.objects.count()

        response = self.client.post(reverse("crear_prestamo"), {
            "libro": self.libro.id,
            "socio": self.socio.id,
            "fecha_prestamo": "2026-10-04",
            "fecha_devolucion": "",
            "estado": "Activo",
            "cantidad": "1",
            "monto": "3.50",
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay existencias suficientes")
        self.assertEqual(Prestamo.objects.count(), prestamos_antes)
        self.assertEqual(Libro.objects.count(), libros_antes)
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.existencias, 0)
        self.assertFalse(self.libro.disponible)

    def test_editar_y_eliminar_prestamo_reponen_existencias(self):
        self.libro.existencias = 1
        self.libro.save(update_fields=["existencias"])
        prestamo = Prestamo.objects.create(
            libro=self.libro,
            socio=self.socio,
            fecha_prestamo="2026-10-04",
            cantidad=2,
            monto="1.50",
        )
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.existencias, 1)

        response = self.client.post(reverse("editar_prestamo", args=[prestamo.id]), {
            "libro": self.libro.id,
            "socio": self.socio.id,
            "fecha_prestamo": "2026-10-04",
            "fecha_devolucion": "",
            "estado": "Activo",
            "cantidad": "1",
            "monto": "1.50",
        })

        self.assertRedirects(response, reverse("lista_prestamos"))
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.existencias, 2)
        self.client.post(reverse("eliminar_prestamo", args=[prestamo.id]))
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.existencias, 3)

    def test_edicion_sin_existencias_revierte_reposicion_y_cambios(self):
        self.libro.existencias = 1
        self.libro.save(update_fields=["existencias"])
        destino = Libro.objects.create(
            titulo="Libro sin copias",
            autor="Autora de prueba",
            categoria="Tecnologia",
            existencias=0,
        )
        prestamo = Prestamo.objects.create(
            libro=self.libro,
            socio=self.socio,
            fecha_prestamo="2026-10-04",
            cantidad=1,
        )
        prestamos_antes = Prestamo.objects.count()

        response = self.client.post(reverse("editar_prestamo", args=[prestamo.id]), {
            "libro": destino.id,
            "socio": self.socio.id,
            "fecha_prestamo": "2026-10-04",
            "fecha_devolucion": "",
            "estado": "Activo",
            "cantidad": "1",
            "monto": "1.50",
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay existencias suficientes")
        self.assertEqual(Prestamo.objects.count(), prestamos_antes)
        prestamo.refresh_from_db()
        self.assertEqual(prestamo.libro_id, self.libro.id)
        self.libro.refresh_from_db()
        destino.refresh_from_db()
        self.assertEqual(self.libro.existencias, 1)
        self.assertEqual(destino.existencias, 0)

    def test_reportes_solo_muestran_informacion_de_negocio(self):
        reporte = self.client.get(reverse("reportes"))
        self.assertEqual(reporte.status_code, 200)
        self.assertContains(reporte, "S/. 12,50")
        self.assertContains(reporte, "Actividad por estado")
        self.assertContains(reporte, "Actividad por libro")
        self.assertNotContains(reporte, "Ejercicios")
        self.assertNotContains(reporte, "aggregate()")
        self.assertNotContains(reporte, "annotate()")
        self.assertContains(self.client.get(reverse("lista_prestamos")), "S/.")

    @override_settings(DEBUG=True)
    def test_select_related_reduce_consultas_sin_exponerlas_al_cliente(self):
        def contar_consultas(queryset):
            reset_queries()
            for libro in queryset:
                if libro.editorial_id:
                    _ = libro.editorial.nombre
                try:
                    _ = libro.ficha.ubicacion
                except FichaLibro.DoesNotExist:
                    pass
            return len(connection.queries)

        consultas_sin_optimizar = contar_consultas(Libro.objects.all())
        consultas_optimizadas = contar_consultas(
            Libro.objects.select_related("editorial", "ficha")
        )

        self.assertGreater(consultas_sin_optimizar, consultas_optimizadas)
        listado = self.client.get(reverse("lista_libros"))
        self.assertNotContains(listado, "Consultas ORM")
        self.assertNotContains(listado, "SQL")

    def test_queryset_personalizado_permite_encadenar_filtros(self):
        self.assertIn(self.libro, Libro.objects.con_existencias().por_categoria("Tecnologia"))
        self.assertNotIn(self.libro, Libro.objects.por_categoria("Literatura"))


class DatosDemostracionTests(TestCase):
    def test_migracion_carga_datos_suficientes_para_los_reportes(self):
        self.assertGreaterEqual(Libro.objects.count(), 5)
        self.assertGreaterEqual(Editorial.objects.count(), 3)
        self.assertGreaterEqual(Prestamo.objects.count(), 8)
