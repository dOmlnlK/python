from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from crm import  models
from crm.forms import CustomerInfo,AuditForm
from  django.views.decorators.csrf import csrf_exempt
import os
from django import conf
import json
from django.db.utils import IntegrityError
from django.utils.timezone import datetime


# Create your views here.



@login_required()
def dashboard(request):
    return render(request,"crm/dashboard.html")

@login_required()
def stu_enrollment(request):
    customer_list = models.CustomerInfos.objects.all()
    class_list = models.ClassList.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        class_grade_id = request.POST.get("class_grade_id")

        try:
            stu_enrollment_obj = models.StudentEnrollment.objects.create(
                customer_id = customer_id,
                class_grade_id = class_grade_id,
                consultant_id = request.user.userinfos.id

            )

        except IntegrityError as e:
            stu_enrollment_obj = models.StudentEnrollment.objects.get(customer_id=customer_id,class_grade_id = class_grade_id)
            if stu_enrollment_obj.contract_argeed:
                return redirect("/crm/stu_enrollment/%s/contract_audit/"%stu_enrollment_obj.id)

        stu_enrollment_link = "http://localhost:8000/crm/enrollment/%s/"%stu_enrollment_obj.id


    return render(request,"crm/stu_enrollment.html",locals())


def enrollment(request,stu_enrollment_id):
    stu_enrollment_obj = models.StudentEnrollment.objects.get(id=stu_enrollment_id)
    customer_obj = stu_enrollment_obj.customer

    price = stu_enrollment_obj.class_grade.course.price
    form = CustomerInfo(instance=customer_obj)

    if stu_enrollment_obj.contract_argeed:
        return HttpResponse("报名信息正在审核中，请耐心等待......")

    if request.method == "POST":
        form = CustomerInfo(instance=customer_obj,data=request.POST)

        if form.is_valid():
            form.save()
            stu_enrollment_obj.contract_argeed = True
            stu_enrollment_obj.save()

            stu_enrollment_obj.contract_argeed_date = datetime.now()
            stu_enrollment_obj.save()

            return HttpResponse("你已成功提交报名信息，请等待审核......")

        else:
            print("err:",form.errors)


    #列出已经上传的文件

    upload_files = []
    enrollment_upload_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR, stu_enrollment_id)

    if os.path.isdir(enrollment_upload_dir):  # 判断文件夹存不存在

        upload_files = os.listdir(enrollment_upload_dir)



    return render(request,"crm/enrollment.html",locals())



@csrf_exempt
def enrollment_upload(request,enrollment_id):
    print(request.FILES)

    enrollment_upload_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR,enrollment_id)  #保存上传文件的文件夹路径


    if not os.path.isdir(enrollment_upload_dir):  #判断文件夹存不存在

        os.mkdir(enrollment_upload_dir)


    file_obj = request.FILES.get("file")


    if len(os.listdir(enrollment_upload_dir)) <= 2:
        file_path = os.path.join(enrollment_upload_dir, file_obj.name)
        f = open(file_path, "wb")
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

    else:
        return HttpResponse(json.dumps({"status":False,"err_msg":"最多可上传两个文件!"}))


    return HttpResponse(json.dumps({"status":True}))



def contract_audit(request,stu_enrollment_id):

    stu_enrollment_obj = models.StudentEnrollment.objects.get(id=stu_enrollment_id)
    enrollment_form = CustomerInfo(instance=stu_enrollment_obj.customer)
    audit_form = AuditForm(instance=stu_enrollment_obj)

    if request.method == "POST":
        audit_form = AuditForm(instance=stu_enrollment_obj,data=request.POST)
        if audit_form.is_valid():
            audit_form.save()
            stu_enrollment_obj.contract_approved_date = datetime.now()
            stu_enrollment_obj.save()

            stu_obj = models.Student.objects.get_or_create(customer=stu_enrollment_obj.customer)[0]  #这是一个元组
            stu_obj.class_grades.add(stu_enrollment_obj.class_grade_id)
            stu_obj.save()

            stu_enrollment_obj.customer.status = 1
            stu_enrollment_obj.customer.save()


            return redirect("/bestadmin/crm/customerinfos/%s/change/"%stu_enrollment_obj.customer.id)

    return render(request,"crm/contract_audit.html",locals())