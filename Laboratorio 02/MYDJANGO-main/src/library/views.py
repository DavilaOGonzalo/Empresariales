from django.shortcuts import get_object_or_404, redirect, render

from .forms import LibroForm
from .models import Libro


def lista_libros(request):
    """Muestra los libros persistidos y permite filtrarlos mediante ORM."""
    libros = Libro.objects.all()
    buscar_titulo = request.GET.get("titulo", "").strip()
    buscar_autor = request.GET.get("autor", "").strip()
    filtro_categoria = request.GET.get("categoria", "").strip()

    if buscar_titulo:
        libros = libros.filter(titulo__icontains=buscar_titulo)
    if buscar_autor:
        libros = libros.filter(autor__icontains=buscar_autor)
    if filtro_categoria:
        libros = libros.filter(categoria__iexact=filtro_categoria)

    categorias = Libro.objects.order_by("categoria").values_list("categoria", flat=True).distinct()
    return render(request, "library/lista.html", {
        "libros": libros,
        "categorias": categorias,
        "buscar_titulo": buscar_titulo,
        "buscar_autor": buscar_autor,
        "filtro_categoria": filtro_categoria,
    })


def crear_libro(request):
    """Guarda un libro validado en SQLite mediante el ORM."""
    if request.method == "POST":
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_libros")
    else:
        form = LibroForm()
    return render(request, "library/crear.html", {"form": form})


def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    return render(request, "library/detalle.html", {"libro": libro})


def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    if request.method == "POST":
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect("detalle_libro", libro_id=libro.id)
    else:
        form = LibroForm(instance=libro)
    return render(request, "library/editar.html", {"form": form, "libro": libro})


def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    if request.method == "POST":
        libro.delete()
        return redirect("lista_libros")
    return render(request, "library/eliminar.html", {"libro": libro})


def actualizar_disponibilidad(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    if request.method == "POST":
        libro.disponible = not libro.disponible
        libro.save(update_fields=["disponible"])
        return redirect("detalle_libro", libro_id=libro.id)
    return render(request, "library/actualizar_disponibilidad.html", {"libro": libro})
