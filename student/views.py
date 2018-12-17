from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student import models
from crm import models as crm_models
# Create your views here.


@login_required()
def my_courses(request,acc_id):

    stu_obj = models.Account.objects.get(id=acc_id).student
    class_list = crm_models.ClassList.objects.filter(student=stu_obj)



    return render(request,"student/my_courses.html",locals())
