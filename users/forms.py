from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models import Post

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email','password1','password2']


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=30)
    class Meta:
        model = Post
        fields = ['title', 'content']

    def hack_control(self):
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')
        if ('hack' in content) or ('hack' in title):
            return None
        return content, title
