from django.conf.urls import include, url
from student import views

urlpatterns = [
    url(r'^(\d+)/my_courses/', views.my_courses, name="my_courses"),
]
