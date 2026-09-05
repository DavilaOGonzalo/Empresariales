# Ejercicio 6 — Analizar el flujo de persistencia

La aplicación `library` persiste la información de los libros mediante el modelo `Libro`, el ORM de Django y la base de datos SQLite configurada en `src/config/settings.py`.

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

La tabla física correspondiente al modelo es `library_libro`. Su estructura se genera a partir de la migración `library/migrations/0001_initial.py`.

---

## 1. Operación de consulta: listar y filtrar libros

Ejemplo: el usuario abre `http://127.0.0.1:8000/library/?titulo=django`.

```text
Request (GET /library/?titulo=django)
        ↓
URL
        ↓
View: lista_libros
        ↓
Model: Libro
        ↓
Manager / QuerySet: Libro.objects.all().filter(...)
        ↓
Django ORM
        ↓
SQLite: db.sqlite3, tabla library_libro
        ↓
View
        ↓
Context
        ↓
Template: library/lista.html
        ↓
Response: HTML 200 OK
```

### Recorrido detallado

1. **Request:** El navegador envía una petición `GET` a `/library/`. Opcionalmente incluye los parámetros `titulo`, `autor` y/o `categoria`.

2. **URL:** En `src/config/urls.py`, la ruta `path("library/", include("library.urls"))` delega la petición a `src/library/urls.py`. Allí, `path("", views.lista_libros, name="lista_libros")` selecciona la vista `lista_libros`.

3. **View:** `lista_libros(request)` obtiene los criterios desde `request.GET` y empieza la consulta:

   ```python
   libros = Libro.objects.all()
   ```

4. **Model:** `Libro`, definido en `src/library/models.py`, describe los campos persistentes: `titulo`, `autor`, `categoria` y `disponible`. Su clase `Meta` ordena los resultados por título.

5. **Manager / QuerySet:** `objects` es el *manager* predeterminado de `Libro`. `all()` crea un `QuerySet`; luego, si existen criterios, la vista lo refina con `filter()`:

   ```python
   libros = libros.filter(titulo__icontains=buscar_titulo)
   libros = libros.filter(autor__icontains=buscar_autor)
   libros = libros.filter(categoria__iexact=filtro_categoria)
   ```

   También se consulta el conjunto de categorías con `Libro.objects.order_by("categoria").values_list("categoria", flat=True).distinct()`.

6. **Django ORM → SQLite:** El `QuerySet` se evalúa al ser utilizado por el template. Django ORM traduce la operación a sentencias SQL `SELECT` y las ejecuta contra `db.sqlite3`, sobre la tabla `library_libro`. Las filas obtenidas se convierten en instancias de `Libro`.

7. **View → Context:** La vista prepara el diccionario de contexto y ejecuta `render()`:

   ```python
   return render(request, "library/lista.html", {
       "libros": libros,
       "categorias": categorias,
       "buscar_titulo": buscar_titulo,
       "buscar_autor": buscar_autor,
       "filtro_categoria": filtro_categoria,
   })
   ```

8. **Template:** `src/library/templates/library/lista.html` recorre `{% for libro in libros %}` y muestra los atributos de cada objeto, además de las categorías y filtros activos.

9. **Response:** Django renderiza la plantilla como HTML y devuelve una respuesta `HTTP 200 OK` al navegador.

---

## 2. Operación de creación: registrar un libro

La creación incluye dos solicitudes: primero se carga el formulario y después se envía el formulario validado.

```text
Request (POST /library/crear/)
        ↓
URL
        ↓
View: crear_libro
        ↓
Model: Libro, mediante LibroForm
        ↓
Manager / QuerySet: instancia Libro y save()
        ↓
Django ORM
        ↓
SQLite: INSERT en library_libro
        ↓
View
        ↓
Response: redirect 302 a /library/
        ↓
Nueva consulta y renderizado de lista.html
```

### Recorrido detallado

1. **Request:** El usuario abre `/library/crear/` con `GET`. La vista crea un formulario vacío (`LibroForm()`) y renderiza `library/crear.html`. El usuario completa el formulario y pulsa **Registrar libro**, por lo que el navegador envía un `POST /library/crear/` con el token CSRF y los campos ingresados.

2. **URL:** En `src/library/urls.py`, la ruta `path("crear/", views.crear_libro, name="crear_libro")` dirige la petición a `crear_libro`.

3. **View:** La vista detecta el método `POST` y enlaza los datos recibidos al formulario:

   ```python
   form = LibroForm(request.POST)
   ```

4. **Model:** `LibroForm` es un `ModelForm` configurado con `model = Libro` y los campos `titulo`, `autor`, `categoria` y `disponible`. Al ejecutar `form.is_valid()`, Django valida los datos usando las reglas del formulario y del modelo, por ejemplo las longitudes máximas y los campos obligatorios.

5. **Manager / QuerySet:** Si los datos son válidos, la vista llama a:

   ```python
   form.save()
   ```

   Como el formulario no tiene una instancia previa, `ModelForm.save()` construye una nueva instancia de `Libro` y ejecuta su método `save()`. En una creación no se requiere un `QuerySet` de lectura: interviene el modelo, su manager/conexión configurada y la operación de guardado.

6. **Django ORM → SQLite:** El ORM transforma `save()` en una sentencia SQL `INSERT` para `library_libro`. SQLite guarda los valores y asigna la clave primaria `id` automáticamente. Con esto, el libro queda persistido incluso cuando se reinicia el servidor.

7. **View → Response:** Tras guardar correctamente, `crear_libro` ejecuta:

   ```python
   return redirect("lista_libros")
   ```

   Django devuelve una respuesta `HTTP 302 Found` con la URL del listado. En este punto no se renderiza un template de éxito directamente.

8. **Nueva Request, Context y Template:** El navegador sigue la redirección realizando `GET /library/`. Se repite el flujo de consulta anterior: el nuevo libro es leído desde SQLite, se coloca en el contexto como parte de `libros`, `library/lista.html` lo muestra y el navegador recibe finalmente un `HTTP 200 OK`.

### Cuando el formulario no es válido

Si `form.is_valid()` devuelve `False`, no se ejecuta `form.save()` ni se emite ningún `INSERT`. La misma vista construye el contexto `{"form": form}`, renderiza `library/crear.html` y devuelve `HTTP 200 OK` con los mensajes de error asociados a los campos.

---

## Resumen del patrón aplicado

```text
Consulta: GET → URL → View → Libro.objects / QuerySet → ORM → SQLite
          → View / Context → lista.html → Response 200

Creación: POST → URL → View → LibroForm / Libro.save() → ORM → SQLite (INSERT)
          → Redirect 302 → GET de consulta → Context → lista.html → Response 200
```

Este recorrido implementa el patrón MVT de Django: el modelo representa los datos persistentes, la vista coordina la lógica y el contexto, y el template presenta el resultado al usuario.
