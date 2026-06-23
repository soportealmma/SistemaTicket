from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from usuarios.models import Usuario_soporte




# Create your models here.

class Localidad(models.Model):
    # choices.py o models.py

    CIUDADES_CHILE_CHOICES = [
        ('Región de Arica y Parinacota', (
            ('ARICA', 'Arica'),
        )),
        ('Región de Tarapacá', (
            ('IQUIQUE', 'Iquique'),
            ('ALTO_HOSPICIO', 'Alto Hospicio'),
            ('POZO_ALMONTE', 'Pozo Almonte'),
        )),
        ('Región de Antofagasta', (
            ('ANTOFAGASTA', 'Antofagasta'),
            ('CALAMA', 'Calama'),
            ('TOCOPILLA', 'Tocopilla'),
            ('MEJILLONES', 'Mejillones'),
            ('TALTAL', 'Taltal'),
        )),
        ('Región de Atacama', (
            ('COPIAPO', 'Copiapó'),
            ('VALLENAR', 'Vallenar'),
            ('CHANARAL', 'Chañaral'),
            ('CALDERA', 'Caldera'),
        )),
        ('Región de Coquimbo', (
            ('LA_SERENA', 'La Serena'),
            ('COQUIMBO', 'Coquimbo'),
            ('OVALLE', 'Ovalle'),
            ('ILLAPEL', 'Illapel'),
            ('VICUNA', 'Vicuña'),
            ('SALAMANCA', 'Salamanca'),
        )),
        ('Región de Valparaíso', (
            ('VALPARAISO', 'Valparaíso'),
            ('VINA_DEL_MAR', 'Viña del Mar'),
            ('QUILPUE', 'Quilpué'),
            ('VILLA_ALEMANA', 'Villa Alemana'),
            ('SAN_ANTONIO', 'San Antonio'),
            ('QUILLOTA', 'Quillota'),
            ('SAN_FELIPE', 'San Felipe'),
            ('LOS_ANDES', 'Los Andes'),
            ('LA_CALERA', 'La Calera'),
            ('LIMACHE', 'Limache'),
        )),
        ('Región Metropolitana de Santiago', (
            ('SANTIAGO', 'Santiago'),
            ('PUENTE_ALTO', 'Puente Alto'),
            ('SAN_BERNARDO', 'San Bernardo'),
            ('MELIPILLA', 'Melipilla'),
            ('TALAGANTE', 'Talagante'),
            ('BUIN', 'Buin'),
            ('PENAFLOR', 'Peñaflor'),
            ('COLINA', 'Colina'),
            ('CURACAVI', 'Curacaví'),
        )),
        ("Región del Libertador General Bernardo O'Higgins", (
            ('RANCAGUA', 'Rancagua'),
            ('SAN_FERNANDO', 'San Fernando'),
            ('RENGO', 'Rengo'),
            ('PICHILEMU', 'Pichilemu'),
            ('SAN_VICENTE', 'San Vicente de Tagua Tagua'),
        )),
        ('Región del Maule', (
            ('TALCA', 'Talca'),
            ('CURICO', 'Curicó'),
            ('LINARES', 'Linares'),
            ('CAUQUENES', 'Cauquenes'),
            ('CONSTITUCION', 'Constitución'),
            ('PARRAL', 'Parral'),
            ('SAN_JAVIER', 'San Javier'),
        )),
        ('Región de Ñuble', (
            ('CHILLAN', 'Chillán'),
            ('SAN_CARLOS', 'San Carlos'),
            ('BULNES', 'Bulnes'),
            ('COELEMU', 'Coelemu'),
        )),
        ('Región del Biobío', (
            ('CONCEPCION', 'Concepción'),
            ('TALCAHUANO', 'Talcahuano'),
            ('SAN_PEDRO_DE_LA_PAZ', 'San Pedro de la Paz'),
            ('CHIGUAYANTE', 'Chiguayante'),
            ('CORONEL', 'Coronel'),
            ('LOTA', 'Lota'),
            ('LOS_ANGELES', 'Los Ángeles'),
            ('PENCO', 'Penco'),
            ('TOME', 'Tomé'),
            ('CURANILAHUE', 'Curanilahue'),
        )),
        ('Región de La Araucanía', (
            ('TEMUCO', 'Temuco'),
            ('ANGOL', 'Angol'),
            ('VILLARRICA', 'Villarrica'),
            ('PUCON', 'Pucón'),
            ('LAUTARO', 'Lautaro'),
            ('NUEVA_IMPERIAL', 'Nueva Imperial'),
            ('VICTORIA', 'Victoria'),
        )),
        ('Región de Los Ríos', (
            ('VALDIVIA', 'Valdivia'),
            ('LA_UNION', 'La Unión'),
            ('RIO_BUENO', 'Río Bueno'),
            ('PANGUIPULLI', 'Panguipulli'),
        )),
        ('Región de Los Lagos', (
            ('PUERTO_MONTT', 'Puerto Montt'),
            ('OSORNO', 'Osorno'),
            ('PUERTO_VARAS', 'Puerto Varas'),
            ('CASTRO', 'Castro'),
            ('ANCUD', 'Ancud'),
            ('QUELLON', 'Quellón'),
            ('CALBUCO', 'Calbuco'),
        )),
        ('Región de Aysén del General Carlos Ibáñez del Campo', (
            ('COYHAIQUE', 'Coyhaique'),
            ('PUERTO_AYSEN', 'Puerto Aysén'),
            ('CHILE_CHICO', 'Chile Chico'),
        )),
        ('Región de Magallanes y de la Antártica Chilena', (
            ('PUNTA_ARENAS', 'Punta Arenas'),
            ('PUERTO_NATALES', 'Puerto Natales'),
            ('PORVENIR', 'Porvenir'),
        )),
    ]

    país = models.CharField(max_length=100, default="Chile")
    región = models.CharField(max_length=100)
    ciudad = models.CharField(choices=CIUDADES_CHILE_CHOICES, default="SANTIAGO", max_length=100)
    comuna = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ciudad}, {self.región}, {self.país}"



class cliente(models.Model):
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=20, unique=True)
    contacto = models.CharField(max_length=200)
    correo = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.ForeignKey('Localidad', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre}"
    
    

class Fabricante(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
