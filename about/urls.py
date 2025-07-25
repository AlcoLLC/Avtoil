from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'about'

urlpatterns = [
    path('about/', views.about_page_view, name='about_page'),
]
