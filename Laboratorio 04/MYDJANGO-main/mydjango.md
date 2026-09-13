# Laboratorio Semana 4 — Relaciones entre Modelos en Django

## 1. Datos del proyecto

**Curso:** Desarrollo de Aplicaciones Empresariales
**Tecnología:** Django 5
**Lenguaje:** Python
**Base de datos:** SQLite
**Aplicación principal:** `library`

---

# 2. Objetivo del laboratorio

En este laboratorio se continúa el desarrollo de la aplicación realizada durante la Semana 3.

El objetivo principal es incorporar relaciones entre modelos utilizando Django ORM.

Se trabajarán las siguientes relaciones:

* Relación 1:1 utilizando `OneToOneField`.
* Relación 1:N utilizando `ForeignKey`.
* Relación N:M utilizando `ManyToManyField`.
* Modelo intermedio para la relación N:M.
* Uso de `select_related()`.
* Uso de `prefetch_related()`.
* Migraciones de Django.
* Acceso a relaciones desde las vistas y templates.
* CRUD del modelo intermedio.

---

# 3. Estructura final del proyecto

La estructura que se busca tener al finalizar el laboratorio es:

```text
MYDJANGO-main/
│
├── src/
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── library/
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   │
│   │   ├── static/
│   │   │   └── library/
│   │   │       └── css/
│   │   │           └── style.css
│   │   │
│   │   ├── templates/
│   │   │   └── library/
│   │   │       ├── lista.html
│   │   │       ├── detalle.html
│   │   │       ├── crear.html
│   │   │       ├── editar.html
│   │   │       ├── eliminar.html
│   │   │       └── relaciones.html
│   │   │
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   └── manage.py
│
├── evidencias/
│   ├── EVIDENCIA_EJERCICIO_1.md
│   ├── EVIDENCIA_EJERCICIO_6.md
│   └── MIGRACION_SEMANA_2.md
│
├── .gitignore
├── README.md
├── mydjango.md
└── requirements.txt
```

---

# 4. Limpieza del proyecto

Durante la revisión de la aplicación se encontraron dos aplicaciones:

```text
src/core/
src/library/
```

La aplicación utilizada para continuar el proyecto será:

```text
library
```

Por lo tanto, `core` corresponde a código anterior que debe revisarse antes de eliminarse.

## 4.1. Antes de eliminar `core`

Primero se debe verificar que `core` no esté siendo utilizado en:

```text
src/config/settings.py
src/config/urls.py
src/library/
```

También se debe revisar si existe:

```python
'core',
```

dentro de `INSTALLED_APPS`.

Si `core` ya no se utiliza, puede eliminarse.

> No se recomienda eliminar la carpeta `core` sin verificar primero sus referencias.

---

# 5. Aplicación principal

La aplicación utilizada para el laboratorio es:

```text
library
```

Se encuentra ubicada en:

```text
src/library/
```

Sus archivos principales son:

```text
models.py
views.py
urls.py
forms.py
admin.py
```

El archivo más importante para este laboratorio será:

```text
models.py
```

porque allí se definirán las relaciones entre las entidades.

---

# 6. Recuperación de la aplicación de la Semana 3

La aplicación desarrollada durante la Semana 3 se utiliza como punto de partida.

Se debe identificar:

* Modelo principal.
* Modelos existentes.
* Views.
* Templates.
* Formularios.
* URLs.
* Migraciones existentes.

La aplicación actualmente contiene operaciones CRUD como:

```text
Crear
Listar
Ver detalle
Editar
Eliminar
```

Estas funcionalidades serán conservadas.

---

# 7. Entidades de la Semana 3

Las cinco entidades originales de la aplicación deben mantenerse.

## Entidad 1

**Nombre:** ______________________________

**Descripción:**

---

## Entidad 2

**Nombre:** ______________________________

**Descripción:**

---

## Entidad 3

**Nombre:** ______________________________

**Descripción:**

---

## Entidad 4

**Nombre:** ______________________________

**Descripción:**

---

## Entidad 5

**Nombre:** ______________________________

**Descripción:**

---

Estas cinco entidades representan el problema desarrollado durante la Semana 3.

---

# 8. Relación 1:1

La primera relación que se implementará será una relación uno a uno.

En Django se utiliza:

```python
OneToOneField
```

La nueva entidad funcionará como una extensión o perfil de una entidad existente.

Ejemplo:

```python
class Perfil(models.Model):
    entidad = models.OneToOneField(
        EntidadPrincipal,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    descripcion = models.TextField(blank=True)
```

## Justificación

La relación 1:1 se utiliza cuando un registro de una entidad solamente puede tener un registro relacionado en la otra entidad.

Por ejemplo, una entidad principal puede tener un único perfil o información adicional.

## `related_name`

Se utiliza:

```python
related_name="perfil"
```

Esto permite acceder al perfil desde la entidad principal:

```python
objeto.perfil
```

## `on_delete`

Se utiliza:

```python
on_delete=models.CASCADE
```

porque el perfil depende de la existencia de la entidad principal.

Si se elimina la entidad principal, también se elimina su información adicional.

---

# 9. Relación 1:N

La segunda relación será uno a muchos.

En Django se utiliza:

```python
ForeignKey
```

Ejemplo:

```python
class EntidadRelacionada(models.Model):
    entidad_principal = models.ForeignKey(
        EntidadPrincipal,
        on_delete=models.CASCADE,
        related_name="entidades_relacionadas"
    )
```

Esto significa:

```text
EntidadPrincipal
       │
       ├── EntidadRelacionada
       ├── EntidadRelacionada
       └── EntidadRelacionada
```

Una entidad principal puede tener muchos registros relacionados.

## Justificación

La relación 1:N permite representar una situación donde un registro principal puede estar asociado con varios registros secundarios.

## `related_name`

Se utiliza:

```python
related_name="entidades_relacionadas"
```

Por ejemplo:

```python
objeto.entidades_relacionadas.all()
```

Esto permite obtener todos los registros relacionados.

---

# 10. Relación N:M

La tercera relación será muchos a muchos.

Django permite representar esta relación mediante:

```python
ManyToManyField
```

En este laboratorio se utilizará un modelo intermedio.

Ejemplo:

```python
class EntidadPrincipal(models.Model):
    entidades = models.ManyToManyField(
        EntidadSecundaria,
        through="RelacionIntermedia",
        related_name="entidades_principales"
    )
```

---

# 11. Modelo intermedio

El modelo intermedio será:

```python
class RelacionIntermedia(models.Model):
    entidad_principal = models.ForeignKey(
        EntidadPrincipal,
        on_delete=models.CASCADE,
        related_name="relaciones_intermedias"
    )

    entidad_secundaria = models.ForeignKey(
        EntidadSecundaria,
        on_delete=models.CASCADE,
        related_name="relaciones_intermedias"
    )

    fecha = models.DateField()

    estado = models.CharField(
        max_length=30
    )
```

El modelo intermedio tendrá por lo menos dos atributos propios de la relación:

```text
fecha
estado
```

Esto permite almacenar información adicional sobre la relación.

---

# 12. ¿Por qué utilizar un modelo intermedio?

Un modelo intermedio es necesario cuando la relación N:M necesita almacenar información adicional.

Por ejemplo:

```text
Entidad A
   │
   │
   ▼
Relación Intermedia
   │
   ├── fecha
   ├── estado
   │
   ▼
Entidad B
```

De esta manera la relación deja de ser solamente una asociación entre dos entidades y puede almacenar información propia.

---

# 13. Modelo final

El modelo final debe tener como mínimo:

```text
5 entidades originales
+
1 entidad para la relación 1:1
+
1 modelo intermedio para N:M
```

Por lo tanto:

```text
Mínimo: 7 entidades/modelos
```

Además, una de las entidades originales debe mantener la relación `ForeignKey` de la Semana 3.

---

# 14. Ejemplo de estructura de `models.py`

La estructura conceptual será:

```python
from django.db import models


class Entidad1(models.Model):
    # Campos originales
    pass


class Entidad2(models.Model):
    # Campos originales
    pass


class Entidad3(models.Model):
    # Campos originales
    pass


class Entidad4(models.Model):
    # Campos originales
    entidad1 = models.ForeignKey(
        Entidad1,
        on_delete=models.CASCADE,
        related_name="entidades4"
    )


class Entidad5(models.Model):
    # Campos originales
    pass


class Perfil(models.Model):
    entidad1 = models.OneToOneField(
        Entidad1,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    descripcion = models.TextField(blank=True)


class RelacionIntermedia(models.Model):
    entidad1 = models.ForeignKey(
        Entidad1,
        on_delete=models.CASCADE,
        related_name="relaciones"
    )

    entidad2 = models.ForeignKey(
        Entidad2,
        on_delete=models.CASCADE,
        related_name="relaciones"
    )

    fecha = models.DateField()

    estado = models.CharField(
        max_length=30
    )
```

La relación N:M se puede declarar en una de las entidades:

```python
class Entidad1(models.Model):

    entidades2 = models.ManyToManyField(
        Entidad2,
        through="RelacionIntermedia",
        related_name="entidades1"
    )
```

---

# 15. Migraciones

Después de modificar los modelos se debe ejecutar:

```powershell
cd src
```

Activar el entorno virtual si todavía no está activo:

```powershell
..\.venv\Scripts\Activate.ps1
```

Luego:

```powershell
python manage.py makemigrations
```

Después:

```powershell
python manage.py migrate
```

Finalmente:

```powershell
python manage.py showmigrations
```

Las migraciones aplicadas aparecerán con:

```text
[X]
```

---

# 16. Verificar las migraciones

Ejemplo:

```text
library
 [X] 0001_initial
 [X] 0002_...
 [X] 0003_...
```

La `X` significa que la migración fue aplicada correctamente.

---

# 17. `select_related()`

`select_related()` se utiliza principalmente con relaciones:

```text
ForeignKey
OneToOneField
```

Ejemplo:

```python
objetos = Entidad2.objects.select_related(
    "entidad1"
).all()
```

Esto permite obtener información relacionada mediante una consulta optimizada.

---

# 18. `prefetch_related()`

`prefetch_related()` se utiliza principalmente para relaciones:

```text
ManyToManyField
```

y relaciones reversas.

Ejemplo:

```python
objetos = Entidad1.objects.prefetch_related(
    "entidades2"
).all()
```

Esto permite obtener los objetos relacionados de manera eficiente.

---

# 19. Vista con `select_related()`

En `views.py` se puede implementar:

```python
from django.shortcuts import render
from .models import Entidad2


def lista_select_related(request):

    objetos = Entidad2.objects.select_related(
        "entidad1"
    ).all()

    return render(
        request,
        "library/relaciones.html",
        {
            "objetos": objetos
        }
    )
```

---

# 20. Vista con `prefetch_related()`

También se implementará una vista utilizando:

```python
prefetch_related()
```

Ejemplo:

```python
from django.shortcuts import render
from .models import Entidad1


def lista_prefetch_related(request):

    objetos = Entidad1.objects.prefetch_related(
        "entidades2"
    ).all()

    return render(
        request,
        "library/relaciones.html",
        {
            "objetos": objetos
        }
    )
```

---

# 21. URLs

En:

```text
src/library/urls.py
```

se agregarán las rutas correspondientes.

Ejemplo:

```python
from django.urls import path
from . import views


urlpatterns = [

    path(
        "relaciones/select/",
        views.lista_select_related,
        name="lista_select"
    ),

    path(
        "relaciones/prefetch/",
        views.lista_prefetch_related,
        name="lista_prefetch"
    ),

]
```

---

# 22. Template para mostrar relaciones

Archivo:

```text
templates/library/relaciones.html
```

Ejemplo:

```html
{% extends "base.html" %}

{% block content %}

<h1>Relaciones entre entidades</h1>

{% for objeto in objetos %}

    <div>
        <h2>{{ objeto }}</h2>

        {% if objeto.entidad1 %}
            <p>
                Relación directa:
                {{ objeto.entidad1 }}
            </p>
        {% endif %}

    </div>

{% empty %}

    <p>No existen registros.</p>

{% endfor %}

{% endblock %}
```

---

# 23. Acceso mediante `related_name`

Si tenemos:

```python
related_name="perfil"
```

podemos acceder:

```django
{{ objeto.perfil }}
```

Si tenemos:

```python
related_name="entidades_relacionadas"
```

podemos utilizar:

```django
{% for item in objeto.entidades_relacionadas.all %}
    {{ item }}
{% endfor %}
```

---

# 24. Acceso al modelo intermedio

El modelo intermedio también puede consultarse directamente.

Ejemplo:

```python
relaciones = RelacionIntermedia.objects.select_related(
    "entidad1",
    "entidad2"
).all()
```

En el template:

```html
{% for relacion in relaciones %}

    <p>
        {{ relacion.entidad1 }}
        -
        {{ relacion.entidad2 }}
    </p>

    <p>
        Fecha: {{ relacion.fecha }}
    </p>

    <p>
        Estado: {{ relacion.estado }}
    </p>

{% endfor %}
```

---

# 25. CRUD del modelo intermedio

El modelo intermedio debe tener operaciones CRUD.

Las operaciones serán:

```text
Crear relación
Listar relaciones
Editar relación
Eliminar relación
```

Por ejemplo:

```text
/relaciones/
```

para listar.

```text
/relaciones/crear/
```

para crear.

```text
/relaciones/editar/1/
```

para editar.

```text
/relaciones/eliminar/1/
```

para eliminar.

---

# 26. Formulario del modelo intermedio

En:

```text
src/library/forms.py
```

se puede crear:

```python
from django import forms
from .models import RelacionIntermedia


class RelacionIntermediaForm(forms.ModelForm):

    class Meta:
        model = RelacionIntermedia

        fields = [
            "entidad1",
            "entidad2",
            "fecha",
            "estado"
        ]
```

---

# 27. Vista para crear

Ejemplo:

```python
from django.shortcuts import render, redirect
from .forms import RelacionIntermediaForm


def crear_relacion(request):

    if request.method == "POST":

        form = RelacionIntermediaForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("lista_relaciones")

    else:

        form = RelacionIntermediaForm()

    return render(
        request,
        "library/crear_relacion.html",
        {
            "form": form
        }
    )
```

---

# 28. Vista para editar

```python
def editar_relacion(request, id):

    relacion = RelacionIntermedia.objects.get(id=id)

    if request.method == "POST":

        form = RelacionIntermediaForm(
            request.POST,
            instance=relacion
        )

        if form.is_valid():

            form.save()

            return redirect("lista_relaciones")

    else:

        form = RelacionIntermediaForm(
            instance=relacion
        )

    return render(
        request,
        "library/editar_relacion.html",
        {
            "form": form
        }
    )
```

---

# 29. Vista para eliminar

```python
def eliminar_relacion(request, id):

    relacion = RelacionIntermedia.objects.get(id=id)

    if request.method == "POST":

        relacion.delete()

        return redirect("lista_relaciones")

    return render(
        request,
        "library/eliminar_relacion.html",
        {
            "relacion": relacion
        }
    )
```

---

# 30. Flujo MVT

El funcionamiento de la aplicación sigue el patrón MVT de Django:

```text
USUARIO
   │
   ▼
REQUEST
   │
   ▼
URL
   │
   ▼
VIEW
   │
   ▼
MODEL / ORM
   │
   ▼
SQLite
   │
   ▼
MODEL / ORM
   │
   ▼
VIEW
   │
   ▼
CONTEXT
   │
   ▼
TEMPLATE
   │
   ▼
RESPONSE
   │
   ▼
USUARIO
```

---

# 31. Explicación del flujo

## Request

El usuario solicita una dirección desde el navegador.

Ejemplo:

```text
/relaciones/
```

## URL

Django busca la ruta correspondiente en:

```text
urls.py
```

## View

La URL llama a una función de:

```text
views.py
```

## Model / ORM

La vista consulta los modelos:

```python
RelacionIntermedia.objects.all()
```

o:

```python
Entidad.objects.select_related(...)
```

o:

```python
Entidad.objects.prefetch_related(...)
```

## SQLite

Django ORM transforma las consultas en instrucciones SQL para consultar la base de datos.

## Context

Los resultados se envían al template mediante un diccionario:

```python
{
    "objetos": objetos
}
```

## Template

El HTML utiliza los datos:

```django
{% for objeto in objetos %}
```

## Response

Finalmente Django devuelve la página HTML al navegador.

---

# 32. SQL conceptual

Aunque se utiliza Django ORM, internamente se generan consultas SQL.

Por ejemplo:

```python
Entidad.objects.all()
```

conceptualmente representa:

```sql
SELECT *
FROM entidad;
```

Una relación mediante `ForeignKey` puede utilizar:

```sql
SELECT *
FROM entidad2
INNER JOIN entidad1
ON entidad2.entidad1_id = entidad1.id;
```

Una relación N:M utiliza una tabla intermedia:

```text
entidad1
   │
   │
relacion_intermedia
   │
   │
entidad2
```

---

# 33. Panel administrativo

Para registrar los modelos en Django Admin se utiliza:

```python
from django.contrib import admin
from .models import (
    Entidad1,
    Entidad2,
    Entidad3,
    Entidad4,
    Entidad5,
    Perfil,
    RelacionIntermedia
)


admin.site.register(Entidad1)
admin.site.register(Entidad2)
admin.site.register(Entidad3)
admin.site.register(Entidad4)
admin.site.register(Entidad5)
admin.site.register(Perfil)
admin.site.register(RelacionIntermedia)
```

El servidor se inicia con:

```powershell
python manage.py runserver
```

Luego se ingresa a:

```text
http://127.0.0.1:8000/admin/
```

---

# 34. Crear superusuario

Si todavía no existe un usuario administrador:

```powershell
python manage.py createsuperuser
```

Se solicitará:

```text
Username
Email
Password
```

Después se puede ingresar a:

```text
http://127.0.0.1:8000/admin/
```

---

# 35. Verificación final

Antes de entregar el laboratorio se debe comprobar:

* [ ] La aplicación `library` funciona.
* [ ] El CRUD de la Semana 3 continúa funcionando.
* [ ] Se mantienen las cinco entidades originales.
* [ ] Existe una relación 1:1.
* [ ] Existe una relación 1:N.
* [ ] Existe una relación N:M.
* [ ] La relación N:M utiliza `through`.
* [ ] El modelo intermedio tiene mínimo dos atributos propios.
* [ ] Se utilizó `related_name`.
* [ ] Se justificó `on_delete`.
* [ ] Se ejecutó `makemigrations`.
* [ ] Se ejecutó `migrate`.
* [ ] Se verificó `showmigrations`.
* [ ] Se utilizó `select_related()`.
* [ ] Se utilizó `prefetch_related()`.
* [ ] Los templates muestran información relacionada.
* [ ] El modelo intermedio tiene CRUD.
* [ ] El panel administrativo funciona.
* [ ] `requirements.txt` está actualizado.
* [ ] `README.md` está actualizado.

---

# 36. Comandos utilizados

Ubicarse en:

```powershell
cd "C:\Users\Pedro\OneDrive\Documents\GitHub\Desarrollo-de-Aplicaciones-Empresariales\Laboratorio 02\Semana 03"
```

Entrar a `src`:

```powershell
cd src
```

Activar entorno virtual:

```powershell
..\.venv\Scripts\Activate.ps1
```

Crear migraciones:

```powershell
python manage.py makemigrations
```

Aplicar migraciones:

```powershell
python manage.py migrate
```

Ver migraciones:

```powershell
python manage.py showmigrations
```

Ejecutar servidor:

```powershell
python manage.py runserver
```

Crear superusuario:

```powershell
python manage.py createsuperuser
```

---

# 37. Requirements

El archivo:

```text
requirements.txt
```

debe contener las dependencias necesarias del proyecto.

Para verificar Django:

```powershell
python -m django --version
```

Ejemplo:

```text
5.x.x
```

---

# 38. Git

Antes de realizar el commit se recomienda comprobar:

```powershell
git status
```

Agregar los cambios:

```powershell
git add .
```

Crear el commit:

```powershell
git commit -m "Implementar relaciones de modelos Semana 4"
```

Actualizar desde GitHub antes de hacer push:

```powershell
git pull origin main
```

Si no existen conflictos:

```powershell
git push origin main
```

---

# 39. Repositorio

Repositorio utilizado:

```text
https://github.com/PedroJrSuarez/Desarrollo-de-Aplicaciones-Empresariales
```

La URL del repositorio debe incluirse en la entrega final.

---

# 40. Evidencias

Se deben tomar capturas de pantalla de los principales resultados.

### Evidencia 1

Estructura final del proyecto.

### Evidencia 2

Modelos con las relaciones.

### Evidencia 3

Migración creada:

```text
makemigrations
```

### Evidencia 4

Migraciones aplicadas:

```text
migrate
```

### Evidencia 5

Resultado de:

```text
showmigrations
```

### Evidencia 6

Vista utilizando:

```python
select_related()
```

### Evidencia 7

Vista utilizando:

```python
prefetch_related()
```

### Evidencia 8

Template mostrando información relacionada.

### Evidencia 9

CRUD del modelo intermedio.

### Evidencia 10

Panel administrativo.

### Evidencia 11

Aplicación funcionando en el navegador.

---

# 41. Conclusiones

## Conclusión 1

Durante este laboratorio se aprendió a trabajar con relaciones entre modelos en Django. Se implementaron relaciones uno a uno, uno a muchos y muchos a muchos, comprendiendo cómo estas relaciones permiten representar mejor la información de una aplicación empresarial.

## Conclusión 2

También se aprendió a utilizar `select_related()` y `prefetch_related()` para consultar información relacionada mediante Django ORM. Además, se trabajaron migraciones y un modelo intermedio con atributos propios, permitiendo implementar un CRUD completo para administrar las relaciones.

## Conclusión 3

Finalmente, se pudo continuar la aplicación desarrollada en la Semana 3 y ampliar su estructura sin perder las funcionalidades existentes. Esto permitió comprender mejor cómo Django organiza los modelos, las vistas, los templates, las URLs y la base de datos dentro del patrón MVT.
