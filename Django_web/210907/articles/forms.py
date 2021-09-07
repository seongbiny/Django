from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='Title: ',
        widget=forms.TextInput(
            attrs={
                'class': 'my-title',
                'maxlength': 10,
            }
        )
    )
    content = forms.CharField(
        label='Content: ',
        widget=forms.Textarea(
            attrs={
                'class': 'my-content',
                'rows': 5,
                'cols': 50,
            }
        )
    )

    class Meta:
        model = Article
        fields = '__all__'