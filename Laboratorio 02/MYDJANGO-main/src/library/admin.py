from django.contrib import admin

from .models import Editorial, FichaLibro, Libro, Prestamo, Socio


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
	list_display = ("titulo", "autor", "categoria", "editorial", "disponible")
	list_filter = ("disponible", "editorial")
	search_fields = ("titulo", "autor")


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
	list_display = ("libro", "socio", "fecha_prestamo", "fecha_devolucion", "estado")
	list_filter = ("estado", "fecha_prestamo")


admin.site.register([Editorial, Socio, FichaLibro])
