# Evidencias de los Laboratorios Semanas 4 a 7

Toma las capturas con el servidor ejecutándose y colócalas junto a esta guía.

## Capturas requeridas

1. Estructura del proyecto y modelos reales en `src/library/models.py`.
2. Migraciones `0003` a `0006`, junto con `python manage.py showmigrations`.
3. `/library/relaciones/select/` mostrando `select_related()`.
4. `/library/relaciones/prefetch/` mostrando `prefetch_related()`.
5. `/library/relaciones/` y los formularios de crear, editar y eliminar préstamos.
6. `/admin/` mostrando los modelos registrados.

No se incluyen imágenes inventadas. Las evidencias deben mostrar la aplicación
real y los datos de demostración cargados por las migraciones `0004` y `0006`.

## Capturas adicionales del Laboratorio Semana 7

7. `/admin/` con al menos cinco libros, tres editoriales y ocho préstamos, y la
   migración `0005_libro_existencias_prestamo_cantidad_prestamo_monto.py`.
8. El formulario de préstamo y un caso correcto; después, intentar prestar más
   ejemplares de los disponibles y capturar el mensaje de error y los conteos
   de libros/préstamos antes y después.
9. `python manage.py shell` mostrando el diccionario de `aggregate()` y las
   consultas `annotate()`/`values().annotate()` con sus resultados.
10. `/library/reportes/` y `/library/consultas/`, incluyendo las cifras medidas
    antes y después de `select_related()`.
11. `library/models.py`, `library/views.py` y la prueba de CRUD después de los
    cambios, además de la URL del repositorio incluida en el documento Word.

Las capturas de la entrega se toman con la aplicación y la base de datos locales
en ejecución; el código no genera ni simula capturas.
