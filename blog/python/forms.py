from django import forms
from blog.models import Comment

BASE_STYLE_CLASS = {'class': 'form-control', 'autocomplete': 'off'}


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs=BASE_STYLE_CLASS
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs=BASE_STYLE_CLASS
    ))
    to = forms.EmailField(widget=forms.EmailInput(
        attrs=BASE_STYLE_CLASS
    ))
    comments = forms.CharField(required=False, widget=forms.Textarea(
        attrs=BASE_STYLE_CLASS
    ))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs=BASE_STYLE_CLASS),
            'email': forms.TextInput(attrs=BASE_STYLE_CLASS),
            'body': forms.Textarea(attrs=BASE_STYLE_CLASS),
        }


class SearchForm(forms.Form):
    query = forms.CharField()
