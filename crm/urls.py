from django.conf.urls import include, url
from crm import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^stu_enrollment/$', views.stu_enrollment,name="stu_enrollment"),
    url(r'^enrollment/(\d+)/$', views.enrollment,name="enrollment"),
    url(r'^enrollment/(\d+)/upload/$', views.enrollment_upload,name="enrollment_upload"),
    url(r'^stu_enrollment/(\d+)/contract_audit/$', views.contract_audit,name="contract_audit"),
]
