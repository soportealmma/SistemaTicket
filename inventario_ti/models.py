from django.db import models
from django.contrib.auth.models import User


# ============================
# EQUIPOS TI
# ============================
class EquipoTI(models.Model):

    TIPOS = [
        ("notebook", "Notebook"),
        ("macbook", "MacBook"),
        ("workstation", "Estación de trabajo"),
        ("tablet", "Tablet"),
        ("lector_codigo", "Lector de código"),
        ("monitor", "Monitor"),
        ("proyector", "Proyector"),
    ]


    tipo_equipo = models.CharField(max_length=50, choices=TIPOS)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100, unique=True)

    cpu = models.CharField(max_length=100)
    ram_gb = models.IntegerField()
    tipo_disco = models.CharField(max_length=20, choices=[("HDD","HDD"),("SSD","SSD"),("M2","M.2")])
    capacidad_disco_gb = models.IntegerField()

    sistema_operativo = models.CharField(max_length=100)
    licencia_windows_key = models.CharField(max_length=200, blank=True, null=True)

    accesorios = models.CharField(max_length=250)

    estado_equipo = models.CharField(max_length=50, default="operativo")

    responsable_actual = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="equipos_asignados"
    )

    def __str__(self):
        return f"{self.tipo_equipo} - {self.marca} {self.modelo} ({self.numero_serie})"


# ============================
# CELULARES
# ============================
class CelularTI(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=75, blank=True, null=True)
    imei1 = models.CharField(max_length=50)
    imei2 = models.CharField(max_length=50, blank=True, null=True)
    numero_sim1 = models.CharField(max_length=20, blank=True, null=True)
    numero_sim2 = models.CharField(max_length=20, blank=True, null=True)
    version_os = models.CharField(max_length=50)
    clave_bloqueo = models.CharField(max_length=20, blank=True, null=True)

    estado = models.CharField(max_length=50, default="operativo")

    responsable_actual = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="celulares_asignados"
    )

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.imei1})"


# ============================
# LICENCIAS
# ============================
class LicenciaTI(models.Model):
    tipo_licencia = models.CharField(max_length=50)
    producto = models.CharField(max_length=100)
    clave = models.CharField(max_length=200)
    correo_asociado = models.EmailField(blank=True, null=True)
    fecha_compra = models.DateField(blank=True, null=True)
    fecha_expiracion = models.DateField(blank=True, null=True)

    responsable_actual = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="licencias_asignadas"
    )

    def __str__(self):
        return f"{self.tipo_licencia} - {self.producto}"


# ============================
# HISTORIAL DE ASIGNACIONES
# ============================
class HistorialAsignacion(models.Model):
    persona = models.ForeignKey(User, on_delete=models.CASCADE)

    equipo = models.ForeignKey(EquipoTI, on_delete=models.CASCADE, null=True, blank=True)
    celular = models.ForeignKey(CelularTI, on_delete=models.CASCADE, null=True, blank=True)
    licencia = models.ForeignKey(LicenciaTI, on_delete=models.CASCADE, null=True, blank=True)

    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(blank=True, null=True)

    motivo_termino = models.CharField(
        max_length=50,
        choices=[
            ("despido", "Despido"),
            ("renuncia", "Renuncia"),
            ("falla", "Falla"),
            ("renovacion", "Renovación"),
            ("otro", "Otro"),
        ],
        blank=True,
        null=True
    )

    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Asignación {self.persona} - {self.fecha_inicio}"


# ============================
# DOCUMENTO DE ENTREGA (PDF)
# ============================
class DocumentoEntrega(models.Model):
    persona = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    archivo_pdf = models.FileField(upload_to="documentos_entrega/")

    equipos = models.ManyToManyField(EquipoTI, blank=True)
    celulares = models.ManyToManyField(CelularTI, blank=True)
    licencias = models.ManyToManyField(LicenciaTI, blank=True)

    def __str__(self):
        return f"Documento entrega {self.persona} - {self.fecha}"
