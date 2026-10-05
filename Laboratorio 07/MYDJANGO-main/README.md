# Sistema de Biblioteca - Django

## Descripción

Este proyecto es una aplicación web desarrollada con Django que permite administrar
una biblioteca de libros. El sistema guarda la información en una base de datos y
ofrece dos formas de trabajar con ella:

- Una **aplicación web propia**, con páginas diseñadas para el uso diario:
  listado, detalle, formularios de alta y edición, y confirmación de eliminación.
- El **panel de administración de Django (Django Admin)**, que Django genera
  automáticamente a partir de los modelos.

El problema que resuelve es organizar la información de una biblioteca en un lugar
único: qué libros existen, de qué editorial vienen, qué socio tiene prestado cada
libro, en qué sala está cada ejemplar y cuál es la ficha descriptiva de cada obra.

El proyecto reúne los trabajos de dos laboratorios:

| Laboratorio | Tema | Aportación al proyecto |
|---|---|---|
| **Laboratorio 05** | Django Admin | Definición de los modelos y configuración del panel administrativo |
| **Laboratorio 06** | Refactorización y seguridad de Templates | Organización, reutilización y verificación de las plantillas HTML |
| **Laboratorio 07** | ORM avanzado | Inventario transaccional, reportes agregados, QuerySet personalizado y optimización N+1 |

---

## Objetivos

### Objetivos generales

- Modelar el dominio de una biblioteca usando clases de Django.
- Persistir la información de forma reliable mediante el ORM de Django.
- Ofrecer una interfaz web propia para las operaciones CRUD.
- Configurar el panel administrativo de Django para la gestión interna.

### Objetivos del Laboratorio 05

- Definir modelos con sus atributos y métodos.
- Establecer relaciones entre modelos: `ForeignKey`, `OneToOneField` y
  `ManyToManyField` con modelo intermedio.
- Aplicar `ModelAdmin` para personalizar el panel administrativo.
- Configurar `list_display`, `search_fields` y `list_filter`.
- Gestionar datos relacionados con `StackedInline` y `TabularInline`.

### Objetivos del Laboratorio 06

- Aplicar herencia de plantillas con `{% extends %}` y `{% block %}`.
- Reutilizar fragmentos mediante `{% include %}`.
- Usar filtros y comentarios de plantilla.
- Comprobar el escapado automático de contenido (auto-escape).
- Verificar que las pantallas sigan funcionando tras los cambios.

---

## Tecnologías utilizadas

| Tecnología | Versión / detalle |
|---|---|
| Python | 3.10 o superior |
| Django | 5.2.17 |
| SQLite | Base de datos, configurada en `src/config/settings.py` |
| HTML / CSS | Plantillas y estilos estáticos |
| JavaScript | `core/static/core/js/app.js` (búsqueda en el andamiaje) |
| Git y GitHub | Control de versiones |

> Los archivos `requirements.txt` de la raíz y de `src/` fijan Django 5.2.17.

---

## Estructura del proyecto

```text
MYDJANGO-main/
├── README.md
├── requirements.txt
├── mydjango.md                  # Enunciado del laboratorio
├── MIGRACION_SEMANA_2.md
├── EVIDENCIA_EJERCICIO_1.md
├── EVIDENCIA_EJERCICIO_6.md
├── evidencias/                 # Guía de capturas requeridas
├── image.png
└── src/
    ├── manage.py
    ├── requirements.txt
    ├── db.sqlite3
    ├── config/                  # Configuración global de Django
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── core/                    # Aplicación base (andamiaje)
    │   ├── admin.py
    │   ├── models.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── migrations/
    │   ├── static/core/
    │   │   ├── css/style.css
    │   │   └── js/app.js
    │   └── templates/
    │       ├── base.html        # Plantilla padre
    │       └── core/item_list.html
    └── library/                 # Aplicación de la biblioteca
        ├── admin.py
        ├── models.py
        ├── forms.py
        ├── urls.py
        ├── views.py
        ├── tests.py
        ├── migrations/          # 0001 a 0006
        ├── static/library/css/style.css
        └── templates/library/
            ├── lista.html
            ├── detalle.html
            ├── crear.html
            ├── editar.html
            ├── eliminar.html
            ├── actualizar_disponibilidad.html
            ├── ficha_form.html
            ├── relaciones.html
            ├── relaciones_lista.html
            ├── prestamo_form.html
            ├── prestamo_eliminar.html
            ├── reporte.html
            ├── consultas.html
            ├── item_list.html   # (en core)
            ├── _form_libro.html
            ├── _relaciones_encabezado.html
            ├── _relaciones_select.html
            └── _relaciones_prefetch.html
```

### Configuración relevante

| Clave | Valor | Para qué sirve |
|---|---|---|
| `LANGUAGE_CODE` | `es-es` | Idioma de la interfaz |
| `STATIC_URL` | `static/` | Ruta base de los archivos estáticos |
| `TEMPLATES > DIRS` | `src/templates` | Carpeta raíz de plantillas |
| `TEMPLATES > APP_DIRS` | `True` | Busca `templates/` dentro de cada app |
| `DATABASES` | `db.sqlite3` | Base de datos SQLite |

---

## Modelos y entidades

La investigación propia se desarrolla sobre **cinco modelos**, definidos en
`src/library/models.py`:

### Editorial

Editorial que publica los libros.

| Atributo | Tipo | Notas |
|---|---|---|
| `nombre` | `CharField(max_length=150)` | Único |

### Socio

Persona que puede solicitar libros en préstamo.

| Atributo | Tipo | Notas |
|---|---|---|
| `nombre` | `CharField(max_length=150)` | |
| `correo` | `EmailField()` | Único |
| `activo` | `BooleanField(default=True)` | Permite filtrar socios activos |

### Libro

Entidad principal del sistema.

| Atributo | Tipo | Notas |
|---|---|---|
| `titulo` | `CharField(max_length=200)` | |
| `autor` | `CharField(max_length=150)` | |
| `categoria` | `CharField(max_length=100)` | |
| `disponible` | `BooleanField(default=True)` | Indicador sincronizado con las existencias |
| `existencias` | `PositiveIntegerField(default=5)` | Copias disponibles para prestar |
| `editorial` | `ForeignKey(Editorial)` | Editorial del libro |
| `socios` | `ManyToManyField(Socio)` | A través del modelo `Prestamo` |

### FichaLibro

Información adicional y única de cada libro (relación 1:1).

| Atributo | Tipo | Notas |
|---|---|---|
| `libro` | `OneToOneField(Libro)` | Un solo ficha por libro |
| `resumen` | `TextField(blank=True)` | |
| `ubicacion` | `CharField(max_length=100, blank=True)` | Por ejemplo, sala y estante |

### Prestamo

Modelo intermedio entre `Libro` y `Socio`. Además de relacionar ambas entidades,
guarda datos propios del préstamo.

| Atributo | Tipo | Notas |
|---|---|---|
| `libro` | `ForeignKey(Libro)` | Libro prestado |
| `socio` | `ForeignKey(Socio)` | Socio que lo recibe |
| `fecha_prestamo` | `DateField()` | Obligatoria |
| `fecha_devolucion` | `DateField(null=True, blank=True)` | Vacío si sigue prestado |
| `estado` | `CharField(max_length=30, default="Activo")` | |
| `cantidad` | `PositiveIntegerField(default=1)` | Ejemplares incluidos en el préstamo |
| `monto` | `DecimalField(max_digits=10, decimal_places=2)` | Importe por ejemplar para los reportes |

### Modelo auxiliar: `Item` (aplicación `core`)

La aplicación `core` contiene un modelo `Item` con los campos `name`,
`description` y `created_at`. **No forma parte de los cinco modelos de la
investigación**: es el andamiaje que Django crea al iniciar el proyecto.

---

## Relaciones entre modelos

El sistema implementa los tres tipos de relación que pide el enunciado.

### 1. `ForeignKey` — muchos a uno (1:N)

`Libro` pertenece a una `Editorial`. Una editorial puede tener muchos libros.

```python
class Libro(models.Model):
    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="libros",
    )
```

- `on_delete=models.SET_NULL`: si se borra una editorial, los libros se conservan
  y quedan sin editorial.
- `related_name="libros"`: permite consultar `editorial.libros.all()`.

### 2. `OneToOneField` — uno a uno (1:1)

`FichaLibro` es la extensión de `Libro`. Cada libro tiene como máximo una ficha.

```python
class FichaLibro(models.Model):
    libro = models.OneToOneField(
        Libro,
        on_delete=models.CASCADE,
        related_name="ficha",
    )
```

- `on_delete=models.CASCADE`: si se borra el libro, su ficha se borra también.
- `related_name="ficha"`: permite acceder con `libro.ficha`.

### 3. `ManyToManyField` con modelo intermedio — muchos a muchos (N:M)

`Libro` y `Socio` se relacionan mediante `Prestamo`, que guarda datos propios.

```python
class Libro(models.Model):
    socios = models.ManyToManyField(
        Socio,
        through="Prestamo",
        related_name="libros",
        blank=True,
    )
```

El modelo intermedio es necesario porque la relación **tiene información propia**:
cuándo se prestó, cuándo se devolvió y en qué estado está.

### Resumen

| Relación | Tipo | Campo | `on_delete` | `related_name` |
|---|---|---|---|---|
| `Libro.editorial` | `ForeignKey` | → `Editorial` | `SET_NULL` | `libros` |
| `FichaLibro.libro` | `OneToOneField` | → `Libro` | `CASCADE` | `ficha` |
| `Prestamo.libro` | `ForeignKey` | → `Libro` | `CASCADE` | `prestamos` |
| `Prestamo.socio` | `ForeignKey` | → `Socio` | `CASCADE` | `prestamos` |
| `Libro.socios` | `ManyToManyField` | ↔ `Socio` (vía `Prestamo`) | — | `libros` |

---

## Operaciones CRUD

El sistema permite crear, consultar, editar y eliminar información de libros y
préstamos desde la aplicación web.

| Operación | Formas disponibles | Vista |
|---|---|---|
| **Crear** | Formulario de libro y de préstamo | `crear_libro`, `crear_prestamo` |
| **Consultar** | Listado, búsqueda por filtros y detalle | `lista_libros`, `detalle_libro` |
| **Editar** | Formulario de libro y de préstamo | `editar_libro`, `editar_prestamo` |
| **Eliminar** | Confirmación y borrado | `eliminar_libro`, `eliminar_prestamo` |

### Rutas de la aplicación `library`

Todas las rutas cuelgan del prefijo `/library/`.

| Ruta | Vista | Nombre |
|---|---|---|
| `/library/` | `lista_libros` | `lista_libros` |
| `/library/crear/` | `crear_libro` | `crear_libro` |
| `/library/<id>/` | `detalle_libro` | `detalle_libro` |
| `/library/<id>/editar/` | `editar_libro` | `editar_libro` |
| `/library/<id>/eliminar/` | `eliminar_libro` | `eliminar_libro` |
| `/library/<id>/disponibilidad/` | `actualizar_disponibilidad` | `actualizar_disponibilidad` |
| `/library/<id>/ficha/` | `crear_ficha_libro` | `crear_ficha_libro` |
| `/library/relaciones/` | `lista_prestamos` | `lista_prestamos` |
| `/library/relaciones/crear/` | `crear_prestamo` | `crear_prestamo` |
| `/library/relaciones/editar/<id>/` | `editar_prestamo` | `editar_prestamo` |
| `/library/relaciones/eliminar/<id>/` | `eliminar_prestamo` | `eliminar_prestamo` |
| `/library/relaciones/select/` | `relaciones_select` | `relaciones_select` |
| `/library/relaciones/prefetch/` | `relaciones_prefetch` | `relaciones_prefetch` |

### Rutas de la aplicación `core`

| Ruta | Vista | Nombre |
|---|---|---|
| `/` | `item_list` | `item_list` |
| `/api/items/` | `item_api` | `item_api` |

### Formularios

`src/library/forms.py` define dos formularios basados en modelos
(`ModelForm`), que son los que generan los campos HTML automáticamente:

| Formulario | Modelo | Campos |
|---|---|---|
| `LibroForm` | `Libro` | `titulo`, `autor`, `categoria`, `existencias` |
| `PrestamoForm` | `Prestamo` | `libro`, `socio`, `fecha_prestamo`, `fecha_devolucion`, `estado`, `cantidad`, `monto` |

---

## Laboratorio 05 - Django Admin

### Qué es Django Admin

Django Admin es un panel de administración que Django genera automáticamente a
partir de los modelos. No hace falta escribir las vistas: el panel interpreta las
clases de los modelos y construye las pantallas de alta, consulta, edición y
eliminación.

### Modelos registrados

Los cinco modelos de `library` y el modelo `Item` de `core` están registrados:

| Modelo | Clase de administración |
|---|---|
| `Editorial` | `EditorialAdmin` |
| `Socio` | `SocioAdmin` |
| `Libro` | `LibroAdmin` |
| `FichaLibro` | `FichaLibroAdmin` |
| `Prestamo` | `PrestamoAdmin` |
| `Item` (core) | `ItemAdmin` |

### Uso de `ModelAdmin`

`ModelAdmin` es la clase que permite personalizar el comportamiento de un modelo
en el panel. Se usa con el decorador `@admin.register`, que registra el modelo y
asocia la clase de administración.

```python
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "categoria", "existencias", "disponible", "editorial")
    list_filter = ("disponible", "categoria", "editorial")
    search_fields = ("titulo", "autor", "categoria")
    inlines = [FichaLibroInline, PrestamoInline]
```

### `list_display`

Define qué columnas se muestran en la tabla de registros:

| Modelo | Columnas |
|---|---|
| `Editorial` | `nombre` |
| `Socio` | `nombre`, `correo`, `activo` |
| `Libro` | `titulo`, `autor`, `categoria`, `existencias`, `disponible`, `editorial` |
| `FichaLibro` | `libro`, `ubicacion` |
| `Prestamo` | `libro`, `socio`, `fecha_prestamo`, `fecha_devolucion`, `estado`, `cantidad`, `monto` |
| `Item` | `name`, `created_at` |

### `search_fields`

Define en qué campos se puede buscar. El texto con doble guion bajo (`__`) permite
buscar a través de una relación:

| Modelo | Campos de búsqueda |
|---|---|
| `Editorial` | `nombre` |
| `Socio` | `nombre`, `correo` |
| `Libro` | `titulo`, `autor`, `categoria` |
| `FichaLibro` | `libro__titulo`, `ubicacion` |
| `Prestamo` | `libro__titulo`, `socio__nombre` |
| `Item` | `name`, `description` |

### `list_filter`

Define los filtros laterales que se muestran a la derecha de la tabla:

| Modelo | Filtros |
|---|---|
| `Socio` | `activo` |
| `Libro` | `disponible`, `categoria`, `editorial` |
| `Prestamo` | `estado`, `fecha_prestamo` |

`Editorial`, `FichaLibro` e `Item` no definen `list_filter`.

### `StackedInline` — ficha del libro

`FichaLibroInline` es una relación 1:1. Se muestra dentro de la página del libro,
con los campos apilados verticalmente.

```python
class FichaLibroInline(admin.StackedInline):
    model = FichaLibro
    extra = 0
    max_num = 1
```

- `extra = 0`: no se muestran filas vacías para rellenar.
- `max_num = 1`: limita a un solo formulario, coherente con la relación 1:1.

### `TabularInline` — préstamos del libro

`PrestamoInline` muestra los préstamos en formato de tabla compacta.

```python
class PrestamoInline(admin.TabularInline):
    model = Prestamo
    fields = ("socio", "fecha_prestamo", "fecha_devolucion", "estado")
    extra = 0
```

Ambas clases se declaran en la lista `inlines` de `LibroAdmin`, por lo que la
página de un libro permite administrar su ficha y sus préstamos sin salir de ella.

---

## Laboratorio 06 - Refactorización y seguridad de Templates

Una plantilla (template) es el archivo HTML que Django usa para construir la
respuesta de una página. En este laboratorio se organizaron las plantillas para
evitar código repetido y se comprobó cómo Django protege al usuario frente a
contenido malicioso.

### Herencia de Templates

#### Qué es la herencia

La herencia permite que varias plantillas compartan una misma estructura. Se
definen una **plantilla padre**, que contiene el esqueleto común, y una o más
**plantillas hijas**, que solo rellenan los huecos que les interesan.

La etiqueta `{% extends "base.html" %}` indica que la plantilla actual no es un
documento HTML completo, sino una pieza que se insertará dentro de `base.html`.

#### El papel de `base.html`

`src/core/templates/base.html` es la **plantilla padre**. Contiene todo lo que es
común a todas las páginas:

| Elemento de `base.html` | Descripción |
|---|---|
| `{% load static %}` | Habilita el uso de `{% static %}` |
| `<head>`, metadatos, `lang="es"` | Estructura base del documento |
| `{% block title %}` | Hueco para el título de cada página |
| `<link>` a `core/css/style.css` | Estilo general del proyecto |
| `<header>` con título y menú | Barra superior con enlaces a Libros, Relaciones y Admin |
| `<main class="container">` | Contenedor donde se inserta cada página |
| `{% block content %}` | Hueco principal para el contenido |
| `<script>` a `core/js/app.js` | Comportamiento común |

La plantilla padre **no se visita como página**: no es una pantalla, es el molde
compartido.

#### Cómo la reutilizan las plantillas hijas

Cada plantilla hija "hereda" la estructura y llena los bloques. Por ejemplo,
`lista.html` se ve así en su parte superior:

```html
{% extends "base.html" %}
{% load static %}

{% block content %}
    <h1>Biblioteca</h1>
    ...
{% endblock %}
```

Al abrir `/library/`, el usuario recibe el esqueleto de `base.html` (la barra
superior, los estilos, el menú) y, en el lugar del `{% block content %}`, el
contenido de `lista.html`.

**Estado actual:** de los 16 archivos de plantilla del proyecto, **13 usan
`{% extends "base.html" %}`**. Los que no lo usan son `base.html` (que es la
plantilla padre) y los cuatro archivos parciales, que se insertan con
`{% include %}` en lugar de heredar.

| Archivo | Hereda de `base.html` | Bloques que define |
|---|---|---|
| `core/item_list.html` | Sí | `title`, `content` |
| `lista.html` | Sí | `content` |
| `detalle.html` | Sí | `content` |
| `crear.html` | Sí | `content` |
| `editar.html` | Sí | `content` |
| `eliminar.html` | Sí | `content` |
| `actualizar_disponibilidad.html` | Sí | `content` |
| `ficha_form.html` | Sí | `title`, `content` |
| `relaciones.html` | Sí | `title`, `content` |
| `relaciones_lista.html` | Sí | `title`, `content` |
| `prestamo_form.html` | Sí | `title`, `content` |
| `prestamo_eliminar.html` | Sí | `title`, `content` |

> **Detalle a tener en cuenta:** los bloques `content` que una plantilla hija
> define **reemplazan** por completo el bloque del mismo nombre en el padre. Por
> eso el contenido se coloca siempre dentro de `{% block content %}`.

### Filtros

Un filtro transforma un valor antes de mostrarlo. Se escriben con el símbolo
vertical `|` después de la variable. Los que realmente usa el proyecto son:

| Filtro | Qué hace | Dónde se usa |
|---|---|---|
| `default` | Muestra un texto alternativo si el valor está vacío | `detalle.html`, `relaciones_lista.html`, `_relaciones_select.html` |
| `upper` | Convierte el texto a mayúsculas | `lista.html` |
| `lower` | Convierte el texto a minúsculas | `core/item_list.html` |

Ejemplos reales del proyecto:

```html
{# Muestra "Sin editorial" cuando el libro no tiene editorial #}
{{ libro.editorial|default:"Sin editorial" }}

{# Presenta el título en mayúsculas en el listado #}
{{ libro.titulo|upper }}

{# Presenta el título en minúsculas en los atributos data-* #}
{{ item.name|lower }}
```

El filtro `default` se apoya en que Django considera "vacío" a `None`, a la
cadena vacía, a cero y a las listas vacías, de modo que cubre todos los casos en
los que un campo opcional no fue llenado.

### Comentarios de Templates

Un comentario de plantilla sirve para explicar el código **sin que aparezca en la
página**. Su sintaxis es `{# ... #}`.

`lista.html` lo utiliza para documentar el filtro por categoría:

```html
{# Permite filtrar los libros según la categoría seleccionada por el usuario #}
```

Esta línea no se ve en el navegador, pero ayuda a quien mantenga el archivo a
entender para qué sirve ese bloque de código.

Además, `lista.html` incluye comentarios de HTML (`<!-- ... -->`) como
`<!-- Formulario de búsqueda y filtrado -->`. La diferencia es que los comentarios
de HTML **sí** se pueden ver si se inspecciona el código fuente de la página,
mientras que los comentarios `{# #}` se eliminan antes de enviar la respuesta.

### Reutilización con `include`

`{% include %}` inserta el contenido de otra plantilla dentro de la actual. A
diferencia de la herencia, que aporta la estructura de la página, el `include`
reutiliza un **fragmento concreto**. Se usa, sobre todo, para evitar repetir un
mismo bloque de HTML en varias páginas.

La plantilla incluida recibe automáticamente el contexto de la plantilla que la
incluye, por lo que puede usar las mismas variables sin que se le pasen una por
una.

En el proyecto se usa en cinco lugares:

| Plantilla | Include |
|---|---|
| `crear.html` | `library/_form_libro.html` |
| `editar.html` | `library/_form_libro.html` |
| `relaciones.html` | `library/_relaciones_encabezado.html` |
| `relaciones.html` | `library/_relaciones_select.html` |
| `relaciones.html` | `library/_relaciones_prefetch.html` |

### Refactorización del formulario de libros

#### El problema

`crear.html` y `editar.html` mostraban el mismo formulario: cuatro campos
(`titulo`, `autor`, `categoria`, `disponible`), y para cada uno una etiqueta, el
campo y la lista de errores. Ese formulario estaba **copiado** en las dos
plantillas, unas 56 líneas duplicadas. Si había que cambiar el estilo de un campo,
había que cambiarlo dos veces, y era fácil olvidar una.

#### La solución

Se creó el archivo parcial `_form_libro.html`, que contiene el formulario una sola
vez. Ahora `crear.html` y `editar.html` lo insertan:

```html
{% extends "base.html" %}
{% load static %}

{% block content %}
    <h1>Registrar nuevo libro</h1>

    {% include "library/_form_libro.html" with boton_texto="Registrar libro" %}

    <a href="{% url 'lista_libros' %}" class="btn btn-secondary">Volver al listado</a>
{% endblock %}
```

```html
{% extends "base.html" %}
{% load static %}

{% block content %}
    <h1>Editar libro: {{ libro.titulo }}</h1>

    {% include "library/_form_libro.html" with boton_texto="Guardar cambios" %}

    <a href="{% url 'detalle_libro' libro.id %}" class="btn btn-secondary">Cancelar</a>
{% endblock %}
```

#### Cómo se personaliza el texto del botón

El parcial no puede saber si se está creando o editando, así que el texto del
botón se le entrega desde afuera con `with`:

```html
{% include "library/_form_libro.html" with boton_texto="Registrar libro" %}
```

Dentro del parcial, ese valor se usa así:

```html
<button type="submit" class="btn btn-success">
    {{ boton_texto }}
</button>
```

El resultado es el mismo formulario en las dos pantallas, con una única copia del
código y con el texto del botón adecuado en cada caso.

#### Por qué `_form_libro.html` no usa `extends`

Un archivo parcial **no es una página independiente**: nunca se visita por URL ni
aparece por sí solo en el navegador. Solo existe para ser insertado en otra
plantilla. Por eso no lleva `{% extends "base.html" %}` ni `{% block %}`: si los tuviera, se
convertiría en una pantalla más, con su propio encabezado y su
propio contenido, en lugar de un fragmento reutilizable.

### Refactorización de la pantalla de relaciones

#### Qué hace `relaciones.html`

`relaciones.html` es la pantalla que muestra **cómo se relacionan los modelos
entre sí**. La usan dos vistas distintas según la técnica de consulta que se quiera
enseñar:

| Vista | Ruta | Técnica de consulta | Qué muestra |
|---|---|---|---|
| `relaciones_select` | `/library/relaciones/select/` | `select_related()` | Editorial (1:N) y ficha del libro (1:1) |
| `relaciones_prefetch` | `/library/relaciones/prefetch/` | `prefetch_related()` | Socios relacionados mediante préstamos (N:M) |

La plantilla recibe una variable `modo` desde la vista y, con ella, decide qué
información mostrar. Las dos rutas existen realmente en `library/urls.py`:
`select/` y `prefetch/`.

#### La duplicación que se eliminó

Antes del refactor, la plantilla repetía la misma decisión en tres lugares: el
título, la descripción y, dentro del bucle de libros, el bloque de datos. Eso
significaba que cambiar el texto de la cabecera obligaba a editar varios puntos
del mismo archivo.

Se extrajeron tres archivos parciales:

| Parcial | Contenido extraído |
|---|---|
| `_relaciones_encabezado.html` | El `<h2>` con el título según `modo` y el `<p class="muted">` con la descripción |
| `_relaciones_select.html` | La rama `select`: editorial, ficha 1:1 y ubicación |
| `_relaciones_prefetch.html` | La rama `else`: lista de socios con sus préstamos |

La plantilla principal quedó así:

```html
<div class="panel">
    {% include "library/_relaciones_encabezado.html" %}

    {% for libro in libros %}
        <article class="book-info">
            <h3>{{ libro.titulo }}</h3>
            <p><strong>Autor:</strong> {{ libro.autor }}</p>
            {% if modo == "select" %}
                {% include "library/_relaciones_select.html" %}
            {% else %}
                {% include "library/_relaciones_prefetch.html" %}
            {% endif %}
        </article>
    {% empty %}
        <p>No existen libros registrados.</p>
    {% endfor %}
</div>
```

El archivo pasó de 52 a 34 líneas, y la decisión sobre `modo` se tomó en un solo
punto.

#### Un detalle sobre el `{% empty %}`

El `{% empty %}` se mantiene **dentro de `relaciones.html`**, y no en un parcial.
La razón es que pertenece al bucle `{% for %}`: Django solo lo evalúa cuando la
lista no tiene ningún elemento. Si se moviera a un archivo parcial, se ejecutaría
una vez por cada libro y no cumpliría su función.

#### Las variables que recibe cada parcial

Los parciales heredan el contexto de la plantilla que los incluye, por lo que
reciben lo que necesitan sin que haya que enumerarlo:

| Parcial | Variables que utiliza |
|---|---|
| `_relaciones_encabezado.html` | `modo`, que viene de la vista |
| `_relaciones_select.html` | `libro`, que viene del bucle `{% for %}` que lo rodea |
| `_relaciones_prefetch.html` | `libro`, que viene del bucle `{% for %}` que lo rodea |

#### `select_related()` y `prefetch_related()`

Ambas técnicas de Django sirven para evitar que la aplicación haga una consulta
separada por cada registro, pero funcionan de manera distinta.

`select_related()` construye **un solo comando SQL** que incluye las columnas de
la tabla relacionada. Solo funciona con relaciones que están en la misma fila
(`ForeignKey` y `OneToOneField`).

`prefetch_related()` realiza **una consulta inicial y otra secundaria** que
recupera todos los registros relacionados de una vez. Se usa con relaciones de
muchos a muchos y con relaciones inversas, donde la información vive en otra
tabla.

En `src/library/views.py` se usan de esta forma:

```python
# Editorial (1:N) y ficha (1:1): una sola consulta
def relaciones_select(request):
    libros = Libro.objects.select_related("editorial", "ficha").all()

# Socios mediante préstamos (N:M): consulta inicial + consulta de socios
def relaciones_prefetch(request):
    libros = Libro.objects.prefetch_related("socios", "prestamos__socio").all()
```

Además, el listado de préstamos también optimiza su consulta:

```python
def lista_prestamos(request):
    prestamos = Prestamo.objects.select_related("libro", "socio").all()
```

En los tres casos, el resultado es el mismo que con las consultas simples, pero
con menos viajes a la base de datos.

### Auto-escape y seguridad

#### Qué es el auto-escape

El auto-escape es la protección que Django aplica por defecto a los datos que
insertan las plantillas. Consiste en convertir los caracteres especiales del HTML
en su equivalente de texto, de modo que un valor guardado en la base de datos se
muestra como texto y no se interpreta como código de la página.

Por ejemplo, el texto `<script>alert("XSS")</script>` se convierte en
`&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;`.

#### La prueba realizada

Se guardaron en la base de datos dos libros cuyo título es
`<script>alert("XSS")</script>`. Después se revisaron las páginas que
muestran ese dato, y el resultado fue:

| Página | Etiqueta `<script>` real | Texto escapado |
|---|---|---|
| `/library/` (`lista.html`) | No aparece | `&lt;SCRIPT&gt;ALERT(&quot;XSS&quot;)&lt;/SCRIPT&gt;` |
| `/library/8/` (`detalle.html`) | No aparece | `&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;` |

En `lista.html` el texto sale en mayúsculas porque ese template aplica el filtro
`upper` al título. El filtro transforma el valor, y el escapado se aplica
después, de modo que el orden no altera el resultado.

**Conclusión de la prueba:** el navegador no ejecutó el código. El contenido se
mostró como texto literal, tal como se escriben los libros, y no como una orden
de JavaScript. La protección se debe al auto-escape de Django, que está activo de
forma predeterminada.

Esta protección se mantiene en todo el proyecto: **no se usa el filtro `|safe`**
en ningún template, ni `mark_safe` en Python, ni la etiqueta
`{% autoescape off %}`. Como regla general, un dato guardado por un usuario nunca
debe marcarse como seguro sin revisar antes qué contiene.

### Verificación del funcionamiento

Tras aplicar el refactor se comprobó que las pantallas siguieran funcionando.

| Verificación | Resultado |
|---|---|
| Peticiones a `/library/relaciones/select/` y `/library/relaciones/prefetch/` | Responden con estado 200, igual que antes |
| HTML generado por ambas vistas, antes y después del cambio | Idéntico, salvo el espaciado de sangrado |
| Pruebas automáticas de relaciones | Correctas |

La comparación del HTML se hizo de forma automática: se generaron las páginas
antes y después del cambio con datos que cubrían todos los casos (un libro con
ficha, uno sin ficha, un libro con dos socios y otro sin socios, para confirmar
que la lista vacía se sigue mostrando). El resultado coincidía una vez ignorados
los espacios, lo que confirma que el cambio **no alteró lo que ve el usuario**.

También se ejecutó la suite de pruebas automática del proyecto
(`src/library/tests.py`), con estos resultados:

| Prueba | Resultado |
|---|---|
| `test_relaciones_optimizadas_muestran_datos` | Correcta |
| `test_crud_del_modelo_intermedio` | Correcta |
| `test_crear_libro_persiste_y_redirige_al_listado` | Correcta |
| `test_listado_muestra_libros_guardados_en_orm` | Con error |

El error de la última prueba **no está relacionado con el refactor de las
plantillas**: esa prueba pide que el listado muestre el título «Django para
empresas» con mayúsculas y minúsculas tal como se guardó, pero `lista.html`
aplica el filtro `upper`, que lo convierte a mayúsculas. La causa es el filtro,
no la reorganización de las plantillas, y su corrección requiere modificar la
prueba o el filtro, lo que queda fuera del alcance de este laboratorio.

### Templates refactorizados en el Laboratorio 06

| Template | Cambio aplicado |
|---|---|
| `crear.html` | Reemplaza el formulario inline por `{% include %}` de `_form_libro.html` |
| `editar.html` | Reemplaza el formulario inline por `{% include %}` de `_form_libro.html` |
| `relaciones.html` | Encabezado y ramas de datos extraídos a tres parciales |
| `lista.html` | Se documenta el filtro de categoría con `{# ... #}` y se aplica `upper` al título |

---

## Aplicación web y Django Admin

El proyecto ofrece dos interfaces distintas para trabajar con los mismos datos.

| Característica | Aplicación web propia | Django Admin |
|---|---|---|
| Propósito | Uso diario por parte de los lectores y socios | Gestión interna de la biblioteca |
| Diseño | Personalizado, con los estilos del proyecto | Generado por Django, aspecto uniforme |
| Rutas | Las de la aplicación, por ejemplo `/library/` | Una sola ruta: `/admin/` |
| Acceso | Público | Requiere usuario con permisos |
| Formularios | Definidos a mano en los templates y en `forms.py` | Generados a partir del modelo |
| Validación | Mediante `forms.py` | Integrada en el modelo y los formularios del panel |

No se trata de que una sea mejor que la otra. Son herramientas con propósitos
distintos: la aplicación web presenta la información al usuario final con un
diseño pensado para él, mientras que Django Admin ofrece una vista práctica para
quien administra los datos y necesita trabajar con todas las entidades del modelo,
incluidas las relaciones, desde un mismo lugar.

En la práctica se complementar: en `detalle.html` hay un enlace al panel, y
`base.html` lo incluye en el menú superior.

---

## Ejecución del proyecto

### Requisitos

- Python 3.10 o superior instalado.
- Acceso a una terminal en la carpeta del proyecto.

### Instalación

Desde la carpeta `src`:

```powershell
cd src
pip install -r requirements.txt
```

### Preparar la base de datos

```powershell
python manage.py migrate
```

Las migraciones de la aplicación `library` cargan además datos de demostración:
cinco libros en `0002`, las relaciones base en `0004` y existencias, fichas,
editoriales, socios y ocho préstamos para los reportes en `0005` y `0006`.

Para comprobar el estado de las migraciones:

```powershell
python manage.py showmigrations
```

### Crear un usuario administrador

Django Admin exige un usuario con permiso de entrada:

```powershell
python manage.py createsuperuser
```

El comando ir pidiendo de forma interactiva el nombre de usuario, el correo
electrónico y la contraseña.

### Ejecutar el servidor

```powershell
python manage.py runserver
```

### Direcciones útiles

| Dirección | Contenido |
|---|---|
| `http://127.0.0.1:8000/` | Andamiaje de la aplicación `core` |
| `http://127.0.0.1:8000/library/` | Listado de libros (aplicación web) |
| `http://127.0.0.1:8000/library/reportes/` | Resumen de préstamos, actividad por libro y estado |
| `http://127.0.0.1:8000/library/relaciones/select/` | Relaciones 1:1 y 1:N |
| `http://127.0.0.1:8000/library/relaciones/prefetch/` | Relaciones N:M |
| `http://127.0.0.1:8000/admin/` | Panel de administración de Django |

---

## Evidencias

La carpeta `evidencias/` contiene la guía `README.md` con las capturas que deben
tomarse con el servidor en ejecución. Las capturas requeridas son:

1. Estructura del proyecto y modelos reales en `src/library/models.py`.
2. Migraciones `0003` y `0004`, junto con `python manage.py showmigrations`.
3. `/library/relaciones/select/` mostrando `select_related()`.
4. `/library/relaciones/prefetch/` mostrando `prefetch_related()`.
5. `/library/relaciones/` y los formularios de crear, editar y eliminar préstamos.
6. `/admin/` mostrando los modelos registrados.

Las evidencias deben mostrar la aplicación real y los datos de demostración
cargados por las migraciones `0004` y `0006`. Las capturas se toman con el servidor
funcionando y se colocan junto a esa guía.

En la raíz del proyecto se incluye además `image.png` y los documentos
`EVIDENCIA_EJERCICIO_1.md` y `EVIDENCIA_EJERCICIO_6.md`, que explican el flujo de
persistencia de los ejercicios 1 y 6.

---

## Repositorio

El proyecto forma parte del repositorio general de la asignatura:

```text
https://github.com/DavilaOGonzalo/Empresariales.git
```

Dentro de ese repositorio, este proyecto se encuentra en la carpeta
`Laboratorio 07/MYDJANGO-main/`, junto a los demás laboratorios.

---

## Conclusiones

### Del Laboratorio 05

1. Django Admin construye un panel administrativo funcional a partir de las
   clases de modelo, sin necesidad de escribir las vistas de administración.
2. `ModelAdmin` permite adaptar la presentación de los registros mediante
   `list_display`, `search_fields` y `list_filter`, de modo que el panel muestra
   exactamente la información que el biblioteca necesita.
3. Las relaciones entre modelos no son solo una forma de organizar el código:
   se reflejan en el panel. Las clases `StackedInline` y `TabularInline` permiten
   administrar la ficha 1:1 y los préstamos desde la misma página del libro.
4. Elegir un modelo intermedio para la relación N:M fue necesario porque el
   préstamo guarda datos propios; una relación directa no habría sido suficiente.

### Del Laboratorio 06

1. La herencia de plantillas (`{% extends %}` y `{% block %}`) permite mantener
   una sola definición de la estructura común y evita repetir el esqueleto de la
   página en cada pantalla.
2. `{% include %}` resuelve el problema distinto del código repetido dentro de una
   misma página. El formulario de libros se extrajo a `_form_libro.html` y las
   ramas de la pantalla de relaciones a tres parciales, reduciendo `relaciones.html`
   de 52 a 34 líneas sin cambiar lo que ve el usuario.
3. Los filtros y los comentarios de plantilla son herramientas pequeñas pero
   útiles: transforman la presentación sin tocar los datos y documentan el código
   sin ensuciar la página.
4. El auto-escape de Django protege al usuario frente a contenido malicioso sin
   trabajo adicional. La prueba con `<script>alert("XSS")</script>` confirmó que
   el texto se muestra escapado y no se ejecuta como JavaScript. El punto
   importante es no desactivar esa protección con `|safe` sin revisar el
   contenido.
5. Un refactor se hace bien cuando se puede demostrar que el resultado es el
   mismo. Comparar la respuesta de las páginas antes y después del cambio, y
   ejecutar las pruebas automáticas, permitió confirmar que la reorganización no
   alteró el funcionamiento de la aplicación.

### Funcionalidad añadida

- El catálogo registra existencias disponibles por libro.
- Los préstamos activos descuentan ejemplares de forma segura; al devolverlos o
  cancelarlos, el inventario se actualiza automáticamente.
- La pantalla de reportes presenta importes, ejemplares prestados y actividad
  agrupada por libro y estado.
- Las búsquedas del catálogo reutilizan filtros de negocio para mostrar libros
  por disponibilidad y categoría.
- La carga de relaciones del catálogo está optimizada. La reducción de consultas
  se verifica en las pruebas automatizadas y no se expone como una pantalla para
  los clientes.
- Para verificar la aplicación desde `src`, ejecutar `python manage.py check` y
  `python manage.py test library`.
