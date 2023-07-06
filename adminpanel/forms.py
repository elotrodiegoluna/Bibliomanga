from django import forms
from store.models import Producto, Categoria
from mangas.models import MangaDigital

class ProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())

    class Meta:
        model = Producto
        fields = [
            'nombre',
            'desc',
            'imagen',
            'precio',
            'stock'
        ]
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')  # obtener instancia del producto
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'class': 'product-form'})
                field.required = True
                # si le doy instancia, me pone los datos
                if instance:
                    field.initial = getattr(instance, field_name)

class MangaForm(forms.ModelForm):
    archivo = forms.FileField(label='Archivo', required=True, widget=forms.ClearableFileInput(attrs={'accept': '.cbr,.cbz'}))

    class Meta:
        model = MangaDigital
        fields = ['nombre', 'tomo', 'desc', 'portada', 'premium', 'archivo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'class': 'product-form'})
        self.fields['nombre'].required = True
        self.fields['tomo'].required = True
        self.fields['desc'].required = True
        self.fields['portada'].required = True
        self.fields['archivo'].required = False