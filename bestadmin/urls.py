from django.conf.urls import include, url
from bestadmin import views

urlpatterns = [
    url(r'^$', views.app_index),
    url(r'^(\w+)/(\w+)/$', views.model_detail,name="model_detail"),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.model_change,name="model_change"),
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.model_delete,name="model_delete"),
    url(r'^(\w+)/(\w+)/add/$', views.model_add,name="model_add"),
    url(r'^password_change/$', views.password_change,name="password_change"),


]
