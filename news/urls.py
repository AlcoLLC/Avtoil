from django.urls import path
from . import views   

app_name = 'news'

urlpatterns = [
    path('news/', views.news_list, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
]

