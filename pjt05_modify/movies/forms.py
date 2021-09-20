from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class': 'my-title',
                'placeholder': '제목을 입력하세요',
                'maxlength': 100,
            }
        )
    )
    overview = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class': 'my-content',
                'placeholder': '내용을 입력하세요',
                'rows': 5,
                'cols': 50,
            }
        )
    )
    poster_path = forms.CharField(
        label='포스터',
        widget=forms.TextInput(
            attrs={
                'class': 'my-poster',
                'placeholder': '포스터를 입력하세요',
                'maxlength': 500,
            }
        )
    )
    class Meta:
        model = Movie
        fields = '__all__'