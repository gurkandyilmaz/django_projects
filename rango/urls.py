from django.urls import path,re_path
from rango import views

urlpatterns = [

        path('index/', views.index, name='index'),
        path('about/', views.about, name='about'),
        re_path('category/(?P<cat_name_slug>[\w\-]+)/$', views.show_category, name='show-category'),
        re_path('page/(?P<cat_name_slug>[\w\-]+)/$', views.show_page, name='show-page'),
        re_path('^add_category/$', views.add_category, name='add_category'),
        
        
    ]
