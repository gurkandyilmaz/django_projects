from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm

content_dict = {"boldmessage_index":"This is the index page...",
                "boldmessage_about": "This is the about page...",
                "index_page":"INDEX",
                "about_page":"ABOUT",
                "category_ordered":Category.objects.order_by("-likes")[:3],
                "page_ordered":Page.objects.order_by("-views")[:3]}

                
def index(request):
    #return HttpResponse("Index Page.. \<br/><br/> <a href='/rango/about/'>About Page Link</a>")
    return render(request, "rango/index.html", context=content_dict)


def about(request):
    return render(request,"rango/about.html", context=content_dict)


def main(request):
    return render(request, "rango/main.html")


def show_category(request, cat_name_slug):
	context_dict = {}
	try:
		category_name = Category.objects.get(slug=cat_name_slug)
		pages = Page.objects.filter(category=category_name)
		context_dict['pages'] = pages
		context_dict['category'] = category_name
	except Category.DoesNotExist:
		context_dict['pages'] = None
		context_dict['category'] = None

	return render(request, "rango/category.html", context_dict)


def show_page(request, page_name_slug):
	context_dict = {}
	try:
		page = Page.objects.get(slug=page_name_slug)
		context_dict["page"] = page

	except Page.DoesNotExist:
		context_dict["page"] = None

	return render(request, "rango/page.html", context_dict)


def add_category(request):
	form = CategoryForm()

	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			cat_saved = form.save(commit=True)
			print(f"Category Name: {cat_saved}, Slug: {cat_saved.slug}")
			return index(request)
		else:
			print(form.errors)
	return render(request, "rango/add_category.html", {"form": form})