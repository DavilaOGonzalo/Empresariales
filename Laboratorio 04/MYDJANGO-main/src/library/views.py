from django.shortcuts import get_object_or_404, redirect, render

from .forms import LibroForm, PrestamoForm
from .models import FichaLibro, Libro, Prestamo


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


def relaciones_select(request):
    """Muestra relaciones directas optimizadas con INNER JOIN."""
    libros = Libro.objects.select_related("editorial", "ficha").all()
    return render(request, "library/relaciones.html", {
        "modo": "select",
        "libros": libros,
    })


def relaciones_prefetch(request):
    """Muestra la relación N:M y la relación reversa con prefetch."""
    libros = Libro.objects.prefetch_related("socios", "prestamos__socio").all()
    return render(request, "library/relaciones.html", {
        "modo": "prefetch",
        "libros": libros,
    })


def lista_prestamos(request):
    prestamos = Prestamo.objects.select_related("libro", "socio").all()
    return render(request, "library/relaciones_lista.html", {"prestamos": prestamos})


def crear_prestamo(request):
    if request.method == "POST":
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save()
            prestamo.libro.disponible = False
            prestamo.libro.save(update_fields=["disponible"])
            return redirect("lista_prestamos")
    else:
        form = PrestamoForm()
    return render(request, "library/prestamo_form.html", {"form": form, "titulo": "Registrar préstamo"})


def editar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, pk=prestamo_id)
    if request.method == "POST":
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect("lista_prestamos")
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, "library/prestamo_form.html", {"form": form, "titulo": "Editar préstamo"})


def eliminar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, pk=prestamo_id)
    if request.method == "POST":
        libro = prestamo.libro
        prestamo.delete()
        libro.disponible = True
        libro.save(update_fields=["disponible"])
        return redirect("lista_prestamos")
    return render(request, "library/prestamo_eliminar.html", {"prestamo": prestamo})


def crear_ficha_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    ficha, _ = FichaLibro.objects.get_or_create(libro=libro)
    if request.method == "POST":
        ficha.resumen = request.POST.get("resumen", "")
        ficha.ubicacion = request.POST.get("ubicacion", "")
        ficha.save()
        return redirect("detalle_libro", libro_id=libro.id)
    return render(request, "library/ficha_form.html", {"libro": libro, "ficha": ficha})
