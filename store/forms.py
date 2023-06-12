from django import forms


class ShippingForm(forms.Form):
    COMUNAS_CHOICES = (
        ('', 'Seleccione una comuna'),
        ('la_florida', 'La Florida'),
        ('santiago', 'Santiago'),
        ('cerrillos', 'Cerrillos'),
        ('cerro_navia', 'Cerro Navia'),
        ('conchali', 'Conchalí'),
        ('el_bosque', 'El Bosque'),
        ('estacion_central', 'Estación Central'),
        ('huechuraba', 'Huechuraba'),
        ('independencia', 'Independencia'),
        ('la_cisterna', 'La Cisterna'),
        ('la_granja', 'La Granja'),
        ('la_pintana', 'La Pintana'),
        ('la_reina', 'La Reina'),
        ('las_condes', 'Las Condes'),
        ('lo_barnechea', 'Lo Barnechea'),
        ('lo_espejo', 'Lo Espejo'),
        ('lo_prado', 'Lo Prado'),
        ('macul', 'Macul'),
        ('maipu', 'Maipú'),
        ('nunoa', 'Ñuñoa'),
        ('pedro_aguirre_cerda', 'Pedro Aguirre Cerda'),
        ('penalolen', 'Peñalolén'),
        ('providencia', 'Providencia'),
        ('pudahuel', 'Pudahuel'),
        ('quilicura', 'Quilicura'),
        ('quinta_normal', 'Quinta Normal'),
        ('recoleta', 'Recoleta'),
        ('renca', 'Renca'),
        ('san_joaquin', 'San Joaquín'),
        ('san_miguel', 'San Miguel'),
        ('san_ramón', 'San Ramón'),
        ('vitacura', 'Vitacura'),
    )

    
    comuna = forms.ChoiceField(choices=COMUNAS_CHOICES, required=True)
    direccion = forms.CharField(max_length=100, required=True)
    nombre = forms.CharField(max_length=64, required=True)
    apellido = forms.CharField(max_length=64, required=True)
    telefono = forms.IntegerField(required=True)
    departamento = forms.CharField(max_length=10, required=False)