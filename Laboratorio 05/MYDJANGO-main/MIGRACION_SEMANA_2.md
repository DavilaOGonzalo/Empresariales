# Migracion de Semana 2 a Django ORM y SQLite

## Ejercicio 1: aplicacion recuperada

La entidad principal es `Libro`. En la version inicial se almacenaba en la
lista global `libros` de diccionarios dentro de `library/models.py`.

- Views: listado, creacion, detalle, edicion, eliminacion y cambio de disponibilidad.
- URLs: `library/`, `library/crear/` y rutas con el identificador del libro.
- Formulario: `LibroForm`.
- Templates: `lista.html`, `crear.html`, `detalle.html`, `editar.html`,
  `eliminar.html` y `actualizar_disponibilidad.html`.

Al reiniciar el servidor, la lista en memoria se reconstruia con sus datos
iniciales y se perdian los libros registrados durante la ejecucion anterior.

## Ejercicios 2 a 5: cambios realizados

`Libro` ahora es un modelo Django con los campos `titulo`, `autor`,
`categoria` y `disponible`. Django crea la clave primaria `id` automaticamente.
El formulario se convirtio en `ModelForm` y usa `form.save()` para registrar o
editar libros.

En la Semana 4 se amplió el mismo modelo sin eliminar sus campos existentes:
se agregaron `Editorial`, `Socio`, `FichaLibro` y `Prestamo`. Las migraciones
`0003_editorial_socio_libro_editorial_fichalibro_prestamo_and_more` y
`0004_datos_relaciones_iniciales` incorporan las relaciones y datos de prueba.

La vista de listado usa `Libro.objects.all()` y filtros ORM. Las otras vistas
usan `get_object_or_404`, `save` y `delete`. Se generaron las migraciones
`0001_initial` (tabla `library_libro`) y `0002_cargar_libros_iniciales`
(catalogo de ejemplo). Los datos ahora se guardan en `src/db.sqlite3`.

## Ejercicio 6: flujo de consulta

`Request GET /library/` -> `library/urls.py` -> `lista_libros` -> modelo
`Libro` -> `Libro.objects.all().filter(...)` (Manager y QuerySet) -> Django ORM
-> SQLite -> View -> contexto `libros` -> `lista.html` -> `Response` HTML.

El ORM representa conceptualmente la consulta como:

```sql
SELECT id, titulo, autor, categoria, disponible
FROM library_libro
WHERE titulo LIKE '%valor%';
```

Los filtros por autor y categoria se convierten, respectivamente, en
condiciones `WHERE` adicionales.

## Ejercicio 6: flujo de creacion

`Request POST /library/crear/` -> `library/urls.py` -> `crear_libro` ->
`LibroForm` valida -> modelo `Libro` -> `form.save()` -> Django ORM -> SQLite
-> View -> redireccion al listado -> contexto `libros` -> `lista.html` ->
`Response` HTML.

La persistencia se representa conceptualmente como:

```sql
INSERT INTO library_libro (titulo, autor, categoria, disponible)
VALUES ('Nuevo libro', 'Autor', 'Categoria', 1);
```

Otras operaciones ORM equivalentes son `libro.save()` -> `UPDATE` y
`libro.delete()` -> `DELETE`.
