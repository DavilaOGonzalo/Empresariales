from datetime import date

from django.db import migrations


def cargar_datos_relaciones(apps, schema_editor):
    Editorial = apps.get_model("library", "Editorial")
    FichaLibro = apps.get_model("library", "FichaLibro")
    Libro = apps.get_model("library", "Libro")
    Prestamo = apps.get_model("library", "Prestamo")
    Socio = apps.get_model("library", "Socio")

    editorial_1, _ = Editorial.objects.get_or_create(nombre="Editorial Andina")
    editorial_2, _ = Editorial.objects.get_or_create(nombre="Letras del Sur")
    socio_1, _ = Socio.objects.get_or_create(
        correo="ana@biblioteca.test",
        defaults={"nombre": "Ana Perez", "activo": True},
    )
    socio_2, _ = Socio.objects.get_or_create(
        correo="luis@biblioteca.test",
        defaults={"nombre": "Luis Gomez", "activo": True},
    )

    libros = list(Libro.objects.order_by("id")[:2])
    if libros:
        libros[0].editorial = editorial_1
        libros[0].save(update_fields=["editorial"])
        FichaLibro.objects.get_or_create(
            libro=libros[0],
            defaults={
                "resumen": "Obra principal de la colección de literatura.",
                "ubicacion": "Sala A - Estante 1",
            },
        )
        Prestamo.objects.get_or_create(
            libro=libros[0],
            socio=socio_1,
            defaults={
                "fecha_prestamo": date(2026, 9, 1),
                "estado": "Activo",
            },
        )
    if len(libros) > 1:
        libros[1].editorial = editorial_2
        libros[1].save(update_fields=["editorial"])
        FichaLibro.objects.get_or_create(
            libro=libros[1],
            defaults={
                "resumen": "Clásico disponible para consulta.",
                "ubicacion": "Sala B - Estante 2",
            },
        )
        Prestamo.objects.get_or_create(
            libro=libros[1],
            socio=socio_2,
            defaults={
                "fecha_prestamo": date(2026, 8, 20),
                "fecha_devolucion": date(2026, 9, 10),
                "estado": "Devuelto",
            },
        )


def eliminar_datos_relaciones(apps, schema_editor):
    Editorial = apps.get_model("library", "Editorial")
    FichaLibro = apps.get_model("library", "FichaLibro")
    Prestamo = apps.get_model("library", "Prestamo")
    Socio = apps.get_model("library", "Socio")

    Prestamo.objects.all().delete()
    FichaLibro.objects.all().delete()
    Editorial.objects.filter(nombre__in=["Editorial Andina", "Letras del Sur"]).delete()
    Socio.objects.filter(correo__in=["ana@biblioteca.test", "luis@biblioteca.test"]).delete()


class Migration(migrations.Migration):
    dependencies = [("library", "0003_editorial_socio_libro_editorial_fichalibro_prestamo_and_more")]

    operations = [migrations.RunPython(cargar_datos_relaciones, eliminar_datos_relaciones)]
