from django import forms
from django.db.models import fields
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('user', 'like_users',)

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        exclude = ('review', 'user',)