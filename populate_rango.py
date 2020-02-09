
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango.settings')

import django
django.setup()

from rango.models import Category, Page
import random

random.seed(a=100)

def populate():
	python_pages = [ {"title": "Official Python Tutorial","url":"http://docs.python.org/2/tutorial/"},
					{"title":"How to Think like a Computer Scientist", "url":"http://www.greenteapress.com/thinkpython/"},
					{"title":"Learn Python in 10 Minutes", "url":"http://www.korokithakis.net/tutorials/python/"} ]

	django_pages = [{"title":"Official Django Tutorial", "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
					{"title":"Django Rocks", "url":"http://www.djangorocks.com/"}, 
					{"title":"How to Tango with Django","url":"http://www.tangowithdjango.com/"} ]


	other_pages = [{"title":"Bottle", "url":"http://bottlepy.org/docs/dev/"}, 
					{"title":"Flask", "url":"http://flask.pocoo.org"} ]

	cats = {"Python": {"pages": python_pages},
			"Django": {"pages": django_pages},
			"Other Frameworks": {"pages": other_pages} }

	view_like = {"Python": {"views":128, "likes":64},
				"Django": {"views":64, "likes":32},
				"Other Frameworks": {"views":32, "likes":16}} 

	for key,value in cats.items():
		add_category(key, view_like[key]["views"], view_like[key]["likes"])
		
		for element in value["pages"]:
			add_page(key, element["title"], element["url"], random.randint(1,64))
		


def add_category(key, views, likes):
	c = Category(name = key, views=views, likes=likes)
	c.save()
	print(Category.objects.all())


def add_page(key, title, url, views):
	p = Page(category = Category.objects.filter(name=key)[0], title = title, url=url, views = views)
	p.save()
	print(Page.objects.all())


if __name__ == '__main__':
	print("starting...")
	populate()