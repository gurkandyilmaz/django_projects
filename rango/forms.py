from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, 
		help_text="Please enter the CATEGORY NAME.")
	views = forms.IntegerField(initial=0,
		help_text="Category Views")
	likes = forms.IntegerField(initial=0, 
		help_text="Category Likes")
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Category
		fields = ("name","views","likes",)

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, 
		help_text="Enter the TITLE of the page")
	url = forms.URLField(max_length=250,
		help_text="enter the URL of the page")
	views = forms.IntegerField(initial=0, help_text="Page Views")


	class Meta:
		model = Page
		#exclude = ("category",)
		fields = ("title", "url","views",)

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get("url")

		if url and not url.startswith("http://"):
			url = "http://"+ url
			cleaned_data["url"] = url
			return cleaned_data

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ("username", "email", "password")


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ("website", "picture")






