from django import forms


class ReviewForm(forms.Form):
    titulo = forms.CharField(max_length=64, required=True)
    comentario = forms.CharField(widget=forms.Textarea, required=True)
    rating = forms.IntegerField(required=True, min_value=1, max_value=5)