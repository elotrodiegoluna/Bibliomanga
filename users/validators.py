from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_file_size(value):
    filesize = value.size
    
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError(_("El tamaño máximo permitido es de 5MB."))

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # Obtiene la extensión del archivo
    valid_extensions = ['.jpg', '.jpeg', '.png']
    
    if not ext.lower() in valid_extensions:
        raise ValidationError(_("Formato de archivo no válido. Solo se permiten archivos JPG, JPEG y PNG."))
