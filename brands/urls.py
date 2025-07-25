from django.urls import path
from . import views

app_name = 'brands'

urlpatterns = [
    path('brands/', views.brand_portal_list, name='brand_portal_list'),
    path('brands/pdf/<int:content_id>/', views.view_brand_content_pdf, name='view_brand_content_pdf')
]

