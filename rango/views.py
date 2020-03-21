from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm,PageForm, UserForm, UserProfileForm
from rango.bing_search import run_query

from datetime import datetime

				
def index(request):
	# request.session.set_test_cookie()
	print(request.scheme)
	print(request.body)
	index_dict = {"index_page":"INDEX", "index_page_status":"active", 
				"category_ordered":Category.objects.order_by("-views")[:7],
				"page_ordered":Page.objects.order_by("-views")[:7]}
	visitor_cookie_handler(request)
	index_dict["visits"] = request.session["visits"]

	response = render(request, "rango/index.html", context=index_dict)

	return response

def about(request):
	# if request.session.test_cookie_worked():
	# 	print("TEST COOKIE WORKED")
	# 	request.session.delete_test_cookie()
	about_dict = {"about_page":"ABOUT", "about_page_status":"active"}
	
	return render(request,"rango/about.html", context=about_dict)

def main(request):
	main_dict = {"main_page_status":"active"}


	return render(request, "rango/main.html", context = main_dict)


def show_category(request, cat_name_slug):
	context_dict = {}
	print(request.method)
	print(request.GET)
	try:
		category_name = Category.objects.get(slug=cat_name_slug)
		category_name.views += 1
		category_name.save()
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
		page.views += 1
		page.save()
		context_dict["page"] = page

	except Page.DoesNotExist:
		context_dict["page"] = None

	return render(request, "rango/page_detail.html", context_dict)


def add_category(request):
	form = CategoryForm()

	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			cat_saved = form.save(commit=True)
			#print(f"Category Name: {cat_saved}, Slug: {cat_saved.slug}")
			return index(request)
		else:
			print(form.errors)
	return render(request, "rango/add_category.html", {"form": form})


def add_page(request, category_name_slug):

	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	form = PageForm()
	if request.method == "POST":
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.save()
				return show_category(request, category_name_slug)
		else:
			
			print(form.errors)
	return render(request, "rango/add_page.html", {"form": form, "category":category})


def register(request):
	registered = False

	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES["picture"]
			profile.save()

			registered=True
		else:
			print(user_form.errors, profile_form.errors )
			
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'rango/register.html', {'user_form':user_form, 
						'profile_form':profile_form, 'registered':registered})



def user_login(request):
	if request.method == "POST":
		
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('rango:index_page'))
			else:
				return HttpResponse("Your Rango account is DISABLED.")
		else:
			print(f"invalid login details {username}, {password}")
			return HttpResponse("INVALID login details supplied.")
	else:
		return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text")


def user_logout(request):
	logout(request)

	return HttpResponseRedirect(reverse("rango:index_page"))


def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val


def visitor_cookie_handler(request):
	
	visits = int(get_server_side_cookie(request, "visits", "1"))

	last_visit_cookie = get_server_side_cookie(request, "last_visit", str(datetime.now()))
	last_visit_time	= datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")

	if (datetime.now()-last_visit_time).seconds > 0:
		visits += 1
		request.session["last_visit"] = str(datetime.now())
	else:
		visits = 1
		request.session["last_visit"] = last_visit_cookie
	request.session["visits"] = visits



def search(request):
	content_dict = {"search_page_status":"active"}

	result_list = []
	if request.method == "POST":
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
			result_list = result_list["webPages"]["value"]
			content_dict['result_list'] = result_list
			content_dict['query'] = query
			
	return render(request, 'rango/search.html', context=content_dict)

@login_required
def like_category(request):
	cat_id = None
	if request.method == "GET":
		cat_id = request.GET["category_id"]
	
	likes = 0
	if cat_id:
		cat = Category.objects.get(id=int(cat_id))
		if cat:
			likes = cat.likes + 1 
			cat.likes = likes
			cat.save()
	return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
	cat_list = []
	if starts_with:
		cat_list = Category.objects.filter(name__istartswith=starts_with)

	if max_results>0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]
	return cat_list


def suggest_category(request):
	cat_list = []
	starts_with	= ""

	if request.method == "GET":
		starts_with = request.GET["suggestion"]
	cat_list = get_category_list(8, starts_with)

	return render(request, 'rango/cats.html', {'cats': cat_list})