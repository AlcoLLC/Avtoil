from django.urls import path
from .views import home_view, submit_review, submit_review_ajax

app_name = "home"

urlpatterns = [
    path("", home_view, name="home"),
    path("submit-review/", submit_review, name="submit_review"),
    path("submit-review-ajax/", submit_review_ajax, name="submit_review_ajax"),
]