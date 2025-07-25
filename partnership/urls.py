from django.urls import path
from . import views

app_name = 'partnership'

urlpatterns = [
    path('partnership/', views.partnership_view, name='partnership'),
]