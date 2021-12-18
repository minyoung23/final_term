from django import forms
from .models import Post

#forms 위한 클래스 작성
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields=('title', 'text') #타이틀과 텍스트를 입력받을 수 있도록 필드에 추가시켜줌
