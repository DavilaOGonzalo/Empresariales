from django.urls import path

from . import views


urlpatterns = [
    path('relaciones/select/', views.relaciones_select, name='relaciones_select'),
    path('relaciones/prefetch/', views.relaciones_prefetch, name='relaciones_prefetch'),
    path('relaciones/', views.lista_prestamos, name='lista_prestamos'),
    path('relaciones/crear/', views.crear_prestamo, name='crear_prestamo'),
    path('relaciones/editar/<int:prestamo_id>/', views.editar_prestamo, name='editar_prestamo'),
    path('relaciones/eliminar/<int:prestamo_id>/', views.eliminar_prestamo, name='eliminar_prestamo'),
    path('<int:libro_id>/ficha/', views.crear_ficha_libro, name='crear_ficha_libro'),
    # Listado de libros
    path('', views.lista_libros, name='lista_libros'),
    
    # Crear libro
    path('crear/', views.crear_libro, name='crear_libro'),
    
    # Detalle de libro
    path('<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    
    # Editar libro
    path('<int:libro_id>/editar/', views.editar_libro, name='editar_libro'),
    
    # Eliminar libro
    path('<int:libro_id>/eliminar/', views.eliminar_libro, name='eliminar_libro'),
    
    # Cambiar disponibilidad
    path('<int:libro_id>/disponibilidad/', views.actualizar_disponibilidad, name='actualizar_disponibilidad'),
]
