from django.db import models


class Editorial(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Socio(models.Model):
    nombre = models.CharField(max_length=150)
    correo = models.EmailField(unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    """Libro almacenado de forma persistente en la base de datos."""

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="libros",
    )
    socios = models.ManyToManyField(
        Socio,
        through="Prestamo",
        related_name="libros",
        blank=True,
    )

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


class FichaLibro(models.Model):
    """Información adicional única para cada libro."""

    libro = models.OneToOneField(
        Libro,
        on_delete=models.CASCADE,
        related_name="ficha",
    )
    resumen = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Ficha de {self.libro.titulo}"


class Prestamo(models.Model):
    """Modelo intermedio entre libros y socios."""

    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name="prestamos",
    )
    socio = models.ForeignKey(
        Socio,
        on_delete=models.CASCADE,
        related_name="prestamos",
    )
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=30, default="Activo")

    class Meta:
        ordering = ["-fecha_prestamo", "libro__titulo"]

    def __str__(self):
        return f"{self.libro.titulo} - {self.socio.nombre}"
