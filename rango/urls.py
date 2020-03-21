from django.urls import path,re_path
from rango import views

app_name = "rango"
urlpatterns = [

        path('index/', views.index, name='index_page'),
        path('about/', views.about, name='about_page'),
        re_path('search/$', views.search, name='search_page'),
        re_path('category/(?P<cat_name_slug>[\w\-]+)/$', views.show_category, name='show-category'),
        re_path('page/(?P<page_name_slug>[\w\-]+)/$', views.show_page, name='show-page'),
        re_path('^add_category/$', views.add_category, name='add_category'),
        re_path('^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),

        re_path('^like_category/$', views.like_category, name="like_category"),
        re_path('^suggest/$', views.suggest_category, name="suggest_category"),

        re_path('^register/$', views.register, name='register_page'),
        re_path('^login/$', views.user_login, name='login_page'),
        re_path('^restricted/$', views.restricted, name="restricted_page"),
        re_path('^logout/$', views.user_logout, name="logout_page"),
        
        
    ]
