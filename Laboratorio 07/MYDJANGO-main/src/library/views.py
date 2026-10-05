from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import connection, reset_queries, transaction
from django.db.models import (
    BooleanField,
    Case,
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    Sum,
    Value,
    When,
)
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LibroForm, PrestamoForm
from .models import FichaLibro, Libro, Prestamo


def lista_libros(request):
    """Muestra los libros persistidos y permite filtrarlos mediante ORM."""
    buscar_titulo = request.GET.get("titulo", "").strip()
    buscar_autor = request.GET.get("autor", "").strip()
    filtro_categoria = request.GET.get("categoria", "").strip()
    libros = Libro.objects.por_categoria(filtro_categoria)

    if buscar_titulo:
        libros = libros.filter(titulo__icontains=buscar_titulo)
    if buscar_autor:
        libros = libros.filter(autor__icontains=buscar_autor)

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
        libro.existencias = 0 if libro.disponible else 1
        libro.save(update_fields=["existencias", "disponible"])
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
            prestamo = form.save(commit=False)
            try:
                with transaction.atomic():
                    prestamo.save()
                    if prestamo.estado == "Activo":
                        descontar_existencias(prestamo.libro_id, prestamo.cantidad)
            except ValidationError as error:
                form.add_error(None, error)
            else:
                return redirect("lista_prestamos")
    else:
        form = PrestamoForm()
    return render(request, "library/prestamo_form.html", {"form": form, "titulo": "Registrar préstamo"})


def editar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, pk=prestamo_id)
    if request.method == "POST":
        libro_anterior_id = prestamo.libro_id
        cantidad_anterior = prestamo.cantidad
        estado_anterior = prestamo.estado
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            prestamo_actualizado = form.save(commit=False)
            try:
                with transaction.atomic():
                    if estado_anterior == "Activo":
                        aumentar_existencias(libro_anterior_id, cantidad_anterior)
                    if prestamo_actualizado.estado == "Activo":
                        descontar_existencias(
                            prestamo_actualizado.libro_id,
                            prestamo_actualizado.cantidad,
                        )
                    prestamo_actualizado.save()
            except ValidationError as error:
                form.add_error(None, error)
            else:
                return redirect("lista_prestamos")
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, "library/prestamo_form.html", {"form": form, "titulo": "Editar préstamo"})


def eliminar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, pk=prestamo_id)
    if request.method == "POST":
        with transaction.atomic():
            libro_id = prestamo.libro_id
            if prestamo.estado == "Activo":
                aumentar_existencias(libro_id, prestamo.cantidad)
            prestamo.delete()
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


def descontar_existencias(libro_id, cantidad):
    """Descuenta existencias solo si la actualización condicional puede cumplirse."""
    actualizados = Libro.objects.filter(
        pk=libro_id,
        existencias__gte=cantidad,
    ).update(
        existencias=F("existencias") - cantidad,
        disponible=Case(
            When(existencias__gt=cantidad, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
    )
    if not actualizados:
        raise ValidationError("No hay existencias suficientes para registrar este préstamo.")


def aumentar_existencias(libro_id, cantidad):
    Libro.objects.filter(pk=libro_id).update(
        existencias=F("existencias") + cantidad,
        disponible=True,
    )


def reportes(request):
    importe = ExpressionWrapper(
        F("cantidad") * F("monto"),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )
    total_general = Prestamo.objects.aggregate(
        total=Sum(importe, default=Decimal("0.00")),
        ejemplares=Sum("cantidad", default=0),
    )
    libros_reportados = (
        Libro.objects.annotate(
            cantidad_prestamos=Count("prestamos"),
            ejemplares_prestados=Sum("prestamos__cantidad"),
            monto_total=Sum(
                ExpressionWrapper(
                    F("prestamos__cantidad") * F("prestamos__monto"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            ),
        )
        .order_by("-cantidad_prestamos", "titulo")
    )
    estados = (
        Prestamo.objects.values("estado")
        .annotate(
            cantidad_prestamos=Count("id"),
            ejemplares=Sum("cantidad"),
            monto_total=Sum(importe),
        )
        .order_by("-cantidad_prestamos", "estado")
    )
    return render(
        request,
        "library/reporte.html",
        {
            "total_general": total_general,
            "libros_reportados": libros_reportados,
            "estados": estados,
            "libros_disponibles": Libro.objects.con_existencias().count(),
        },
    )


def medir_consultas_relaciones(request):
    def medir(queryset):
        reset_queries()
        for libro in queryset:
            if libro.editorial_id:
                _ = libro.editorial.nombre
            try:
                _ = libro.ficha.ubicacion
            except FichaLibro.DoesNotExist:
                pass
        return len(connection.queries)

    consultas_sin_optimizar = medir(Libro.objects.all())
    consultas_optimizadas = medir(
        Libro.objects.select_related("editorial", "ficha")
    )
    return render(
        request,
        "library/consultas.html",
        {
            "consultas_sin_optimizar": consultas_sin_optimizar,
            "consultas_optimizadas": consultas_optimizadas,
            "libros": Libro.objects.con_existencias().count(),
        },
    )
