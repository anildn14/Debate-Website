from django.contrib.auth.models import User
from .models import Category,Post,Comment
from django import forms
from django.contrib.auth import get_user_model
import datetime
from crispy_forms.helper import FormHelper
from django.forms.fields import DateField


User=get_user_model()

class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	class Meta: #info about your class is metaclass
		model=User
		fields=['username','email','first_name','last_name','password']

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields='__all__'


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		# fields='__all__'
		fields=['post_category','post_topic','post_content']#,'post_likes']


class CommentForm(forms.ModelForm):
	comment_text=forms.CharField(label="",max_length=1000,widget= forms.Textarea(attrs={'placeholder':'Add new comment','rows':1, 'cols':100}))

	class Meta:
		model=Comment
		fields=['comment_text']
