from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, 
		help_text="Please enter the CATEGORY NAME.")
	views = forms.IntegerField(initial=0, help_text="Views")
	likes = forms.IntegerField(initial=0, help_text="likes")
	slug = forms.CharField(required=False, help_text="slug")

	class Meta:
		model = Category
		fields = ("name", )

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, 
		help_text="Enter the TITLE of the PAGE")
	url = forms.URLField(max_length=200,
		help_text="enter the URL of the PAGE")
	views = forms.IntegerField(initial=0, help_text="Views")

	class Meta:
		model = Page
		exclude = ("category", )

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get("url")

		if url and not url.startswith("http://"):
			url = "http://"+ url
			cleaned_data["url"] = url

			return cleaned_data

