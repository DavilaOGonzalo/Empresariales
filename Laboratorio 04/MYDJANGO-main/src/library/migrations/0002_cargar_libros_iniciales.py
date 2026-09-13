from django.db import migrations


LIBROS_INICIALES = [
    ("Cien anos de soledad", "Gabriel Garcia Marquez", "Novela", True),
    ("Don Quijote de la Mancha", "Miguel de Cervantes", "Clasico", False),
    ("El principito", "Antoine de Saint-Exupery", "Literatura", True),
    ("1984", "George Orwell", "Ciencia ficcion", True),
    ("Orgullo y prejuicio", "Jane Austen", "Romance", False),
]


def cargar_libros_iniciales(apps, schema_editor):
    Libro = apps.get_model("library", "Libro")
    for titulo, autor, categoria, disponible in LIBROS_INICIALES:
        Libro.objects.get_or_create(
            titulo=titulo,
            autor=autor,
            defaults={"categoria": categoria, "disponible": disponible},
        )


def eliminar_libros_iniciales(apps, schema_editor):
    Libro = apps.get_model("library", "Libro")
    Libro.objects.filter(titulo__in=[libro[0] for libro in LIBROS_INICIALES]).delete()


class Migration(migrations.Migration):
    dependencies = [("library", "0001_initial")]

    operations = [migrations.RunPython(cargar_libros_iniciales, eliminar_libros_iniciales)]
