# Laboratorio 05 - Django Admin

## Descripción

Este proyecto implementa un sistema de biblioteca con Django. El Laboratorio 05
aplica clases, atributos y métodos mediante los modelos del sistema, y configura
el panel Django Admin para administrar la información de la biblioteca de forma
centralizada.

La administración incluye el registro de los modelos, vistas de lista, búsqueda,
filtros e interfaces en línea para las relaciones `FichaLibro` y `Prestamo`.

## Objetivos

- Configurar Django Admin para administrar los datos de la biblioteca.
- Aplicar `ModelAdmin` para personalizar la interfaz administrativa.
- Mostrar, buscar y filtrar registros mediante `list_display`, `search_fields`
  y `list_filter`.
- Representar relaciones `ForeignKey`, `OneToOneField` y `ManyToManyField` en
  la administración.
- Gestionar datos relacionados con `StackedInline` y `TabularInline`.

## Tecnologías utilizadas

- Python.
- Django 5.2.
- SQLite, configurada como base de datos del proyecto.
- Git y GitHub.

## Estructura del proyecto

```text
MYDJANGO-main/
├── README.md
├── requirements.txt
├── evidencias/
├── src/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/             # Configuración global de Django
│   ├── core/               # Aplicación base del proyecto
│   └── library/            # Aplicación del sistema de biblioteca
│       ├── admin.py
│       ├── models.py
│       ├── forms.py
│       ├── urls.py
│       ├── views.py
│       ├── migrations/
│       ├── static/
│       └── templates/
└── image.png
```

La implementación del laboratorio se encuentra principalmente en la aplicación
`library`, especialmente en `models.py` y `admin.py`.

## Modelos y relaciones

El sistema de biblioteca contiene cinco modelos directamente relacionados con
la investigación:

- **Editorial:** representa la editorial asociada a los libros.
- **Socio:** representa a la persona que puede solicitar libros.
- **Libro:** almacena título, autor, categoría, disponibilidad y editorial.
- **FichaLibro:** contiene información adicional de un libro, como resumen y
  ubicación.
- **Prestamo:** representa el préstamo de un libro a un socio y registra sus
  datos propios.

No se documentan entidades adicionales: el proyecto contiene estos cinco
modelos para el sistema de biblioteca.

### Relaciones implementadas

- **ForeignKey:** `Libro` se relaciona con `Editorial`. Una editorial puede
  estar asociada a varios libros.
- **OneToOneField:** `FichaLibro` se relaciona de forma única con `Libro`.
- **ManyToManyField mediante modelo intermedio:** `Libro` se relaciona con
  `Socio` mediante `Prestamo`.

El modelo intermedio `Prestamo` incluye los atributos `fecha_prestamo`,
`fecha_devolucion` y `estado`, además de sus referencias a `libro` y `socio`.

## Configuración de Django Admin

Los modelos `Editorial`, `Socio`, `Libro`, `FichaLibro` y `Prestamo` están
registrados en el panel de administración.

Se configuraron clases `ModelAdmin` para adaptar la consulta de registros. La
configuración emplea:

- `list_display` para mostrar campos relevantes en las listas administrativas.
- `search_fields` para permitir búsquedas por nombre, correo, título, autor,
  categoría y datos relacionados según el modelo.
- `list_filter` para filtrar socios por estado activo, libros por disponibilidad
  y categoría, y préstamos por estado y fecha de préstamo.
- `StackedInline` para gestionar `FichaLibro` desde la edición de un `Libro`.
- `TabularInline` para gestionar `Prestamo` desde `Libro`, mostrando `socio`,
  `fecha_prestamo`, `fecha_devolucion` y `estado`.

## Operaciones CRUD

Desde Django Admin se pueden realizar las operaciones CRUD sobre los modelos
registrados:

- **Crear** registros.
- **Consultar** registros y sus relaciones.
- **Editar** registros existentes.
- **Eliminar** registros.

## Ejecución del proyecto

Desde la raíz del proyecto, ingrese a la carpeta `src` y ejecute:

```powershell
cd src
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

El panel administrativo está disponible en:

`/admin/`

En el entorno local predeterminado: <http://127.0.0.1:8000/admin/>.

Para acceder al panel se requiere un usuario administrador. Si aún no existe,
puede crearse con:

```powershell
python manage.py createsuperuser
```

## Evidencias

La carpeta `evidencias/` se utiliza para documentar las evidencias del
laboratorio. Las evidencias consideradas incluyen:

- Panel inicial de Django Admin.
- Modelos registrados.
- Configuración de `list_display`.
- Búsqueda mediante `search_fields`.
- Filtros mediante `list_filter`.
- `FichaLibro` mediante `StackedInline`.
- `Prestamo` mediante `TabularInline`.
- Operaciones CRUD.

## GitHub

[URL DEL REPOSITORIO]

## Conclusiones

1. Django Admin permite crear una interfaz administrativa funcional a partir de
   los modelos definidos en Django.
2. `ModelAdmin`, las búsquedas y los filtros facilitan la consulta y gestión de
   información en el panel administrativo.
3. Los inlines permiten administrar relaciones `OneToOneField` y modelos
   intermedios de una relación `ManyToManyField` desde un mismo formulario.
