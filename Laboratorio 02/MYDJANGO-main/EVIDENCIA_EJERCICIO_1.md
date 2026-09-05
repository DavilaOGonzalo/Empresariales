# Ejercicio 1 - models.py antes de la migracion

Este era el contenido de `library/models.py` en la aplicacion de la Semana 2:

```python
"""
Datos estaticos de la biblioteca.

Los libros se almacenan en una lista de diccionarios en memoria.
No se utiliza una base de datos.
Los datos se pierden al reiniciar el servidor.
"""

libros = [
    {
        "id": 1,
        "titulo": "Cien anos de soledad",
        "autor": "Gabriel Garcia Marquez",
        "categoria": "Novela",
        "disponible": True,
    },
    {
        "id": 2,
        "titulo": "Don Quijote de la Mancha",
        "autor": "Miguel de Cervantes",
        "categoria": "Clasico",
        "disponible": False,
    },
    {
        "id": 3,
        "titulo": "El principito",
        "autor": "Antoine de Saint-Exupery",
        "categoria": "Literatura",
        "disponible": True,
    },
    {
        "id": 4,
        "titulo": "1984",
        "autor": "George Orwell",
        "categoria": "Ciencia ficcion",
        "disponible": True,
    },
    {
        "id": 5,
        "titulo": "Orgullo y prejuicio",
        "autor": "Jane Austen",
        "categoria": "Romance",
        "disponible": False,
    },
]
```

Los registros agregados durante la ejecucion se perdian al reiniciar el
servidor porque la lista no se guardaba en una base de datos.
