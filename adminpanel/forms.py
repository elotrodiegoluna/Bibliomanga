from django import forms
from store.models import Producto
from mangas.models import MangaDigital

class ProductoForm(forms.ModelForm):
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
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'class': 'product-form'})
                field.required = True

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
        self.fields['archivo'].required = True