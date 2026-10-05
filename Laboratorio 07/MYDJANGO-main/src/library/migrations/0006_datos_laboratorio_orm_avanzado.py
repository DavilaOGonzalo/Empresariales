from datetime import date
from decimal import Decimal

from django.db import migrations


def cargar_datos_demostracion(apps, schema_editor):
    alias = schema_editor.connection.alias
    Editorial = apps.get_model("library", "Editorial")
    FichaLibro = apps.get_model("library", "FichaLibro")
    Libro = apps.get_model("library", "Libro")
    Prestamo = apps.get_model("library", "Prestamo")
    Socio = apps.get_model("library", "Socio")

    editoriales = [
        Editorial.objects.using(alias).get_or_create(nombre=nombre)[0]
        for nombre in ("Editorial Andina", "Letras del Sur", "Lectura Abierta")
    ]
    socios = {
        correo: Socio.objects.using(alias).get_or_create(
            correo=correo,
            defaults={"nombre": nombre, "activo": True},
        )[0]
        for correo, nombre in (
            ("ana@biblioteca.test", "Ana Perez"),
            ("luis@biblioteca.test", "Luis Gomez"),
            ("maria@biblioteca.test", "Maria Torres"),
            ("carlos@biblioteca.test", "Carlos Ruiz"),
            ("sofia@biblioteca.test", "Sofia Vega"),
        )
    }

    libros = list(Libro.objects.using(alias).order_by("id"))
    for indice, libro in enumerate(libros):
        libro.editorial = editoriales[indice % len(editoriales)]
        libro.existencias = 5
        libro.disponible = True
        libro.save(update_fields=["editorial", "existencias", "disponible"])
        FichaLibro.objects.using(alias).get_or_create(
            libro_id=libro.pk,
            defaults={
                "resumen": f"Ficha de consulta para {libro.titulo}.",
                "ubicacion": f"Sala {chr(65 + indice)} - Estante {indice + 1}",
            },
        )

    prestamos = [
        ("El principito", "ana@biblioteca.test", "Activo", 1, "1.50"),
        ("1984", "luis@biblioteca.test", "Activo", 2, "2.50"),
        ("Orgullo y prejuicio", "ana@biblioteca.test", "Activo", 1, "1.25"),
        ("Cien anos de soledad", "luis@biblioteca.test", "Devuelto", 1, "0.75"),
        ("Don Quijote de la Mancha", "ana@biblioteca.test", "Devuelto", 1, "0.00"),
        ("El principito", "luis@biblioteca.test", "Devuelto", 2, "2.00"),
    ]
    for titulo, correo, estado, cantidad, monto in prestamos:
        libro = Libro.objects.using(alias).get(titulo=titulo)
        Prestamo.objects.using(alias).get_or_create(
            libro_id=libro.pk,
            socio_id=socios[correo].pk,
            defaults={
                "fecha_prestamo": date(2026, 9, 15),
                "fecha_devolucion": date(2026, 9, 30) if estado == "Devuelto" else None,
                "estado": estado,
                "cantidad": cantidad,
                "monto": Decimal(monto),
            },
        )

    for libro in Libro.objects.using(alias).all():
        prestados = sum(
            Prestamo.objects.using(alias)
            .filter(libro_id=libro.pk, estado="Activo")
            .values_list("cantidad", flat=True)
        )
        libro.existencias = max(0, 5 - prestados)
        libro.disponible = libro.existencias > 0
        libro.save(update_fields=["existencias", "disponible"])


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0005_libro_existencias_prestamo_cantidad_prestamo_monto"),
    ]

    operations = [
        migrations.RunPython(cargar_datos_demostracion, migrations.RunPython.noop),
    ]
