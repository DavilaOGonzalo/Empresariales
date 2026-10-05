from django.contrib import admin

from .models import Editorial, FichaLibro, Libro, Prestamo, Socio


class FichaLibroInline(admin.StackedInline):
    model = FichaLibro
    extra = 0
    max_num = 1


class PrestamoInline(admin.TabularInline):
    model = Prestamo
    fields = ("socio", "fecha_prestamo", "fecha_devolucion", "estado", "cantidad", "monto")
    extra = 0


@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "correo")


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "categoria", "existencias", "disponible", "editorial")
    list_filter = ("disponible", "categoria", "editorial")
    search_fields = ("titulo", "autor", "categoria")
    readonly_fields = ("disponible",)
    inlines = [FichaLibroInline, PrestamoInline]


@admin.register(FichaLibro)
class FichaLibroAdmin(admin.ModelAdmin):
    list_display = ("libro", "ubicacion")
    search_fields = ("libro__titulo", "ubicacion")


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ("libro", "socio", "fecha_prestamo", "fecha_devolucion", "estado", "cantidad", "monto")
    search_fields = ("libro__titulo", "socio__nombre")
    list_filter = ("estado", "fecha_prestamo")
