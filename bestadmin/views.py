from django.shortcuts import render,redirect
from django import conf
from bestadmin import app_setup
from bestadmin.sites import site
# from student import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from bestadmin import forms_handle
from django.db.models import Q
from bestadmin import permissions

import json

# Create your views here.
app_setup.bestadmin_auto_load()


@login_required()
def app_index(request):
    return render(request, "bestadmin/app-index.html", {"site": site})


def get_filter_condition(filter_dic):
    filter_condition = {}

    for k, v in filter_dic.items():
        if k in ["_page", "_o", "_q"]:
            continue
        if v:
            filter_condition[k] = v

    return filter_condition


def get_orderby_result(request, admin_class, obj_list):
    current_orderby_column = {}
    orderby_index = request.GET.get("_o")
    if orderby_index:
        orderby_key = admin_class.list_display[abs(int(orderby_index))]
        current_orderby_column[orderby_key] = orderby_index  # 让前端知道当前排序的字段

        if orderby_index.startswith("-"):
            orderby_key = "-" + orderby_key

        obj_list = obj_list.order_by(orderby_key)

    return obj_list, current_orderby_column


def get_search_result(request, admin_class, obj_list):
    search_val = request.GET.get("_q")
    if search_val:
        q = Q()
        q.connector = "OR"

        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains" % search_field, search_val))
        obj_list = obj_list.filter(q)

        return obj_list
    else:
        return obj_list

@permissions.check_permission
@login_required()
def model_detail(request, app_name, model_name):
    admin_class = site.enabled_admins[app_name][model_name]

    if request.method == "POST":

        selected_ids = json.loads(request.POST.get("selected_ids"))
        print("post>.", request.POST)
        select_action = request.POST.get("action")

        if not select_action:         #如果post中没有"action"，则为确认删除的post
            if selected_ids:

                admin_class.model.objects.filter(id__in=selected_ids).delete()



        else:

            querysets = admin_class.model.objects.filter(id__in=selected_ids)

            action_func = getattr(admin_class,select_action)
            return action_func(request,querysets,selected_ids,app_name,model_name)


    filter_dic = request.GET
    filter_condition = get_filter_condition(filter_dic)
    admin_class.filter_condition = filter_condition
    obj_list = admin_class.model.objects.filter(**filter_condition).order_by("-id")

    # 搜索后的obj_list
    obj_list = get_search_result(request, admin_class, obj_list)
    search_val = request.GET.get("_q", "")

    # 排序后的obj_list
    obj_list, current_orderby_column = get_orderby_result(request, admin_class, obj_list)

    paginator = Paginator(obj_list, admin_class.list_per_page)  # Show 25 contacts per page

    page = request.GET.get('_page')

    try:
        obj_list = paginator.page(page)

    except PageNotAnInteger:
        obj_list = paginator.page(1)

    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)

    return render(request, "bestadmin/model_detail.html", locals())

@permissions.check_permission
@login_required()
def model_change(request, app_name, model_name, obj_id):
    admin_class = site.enabled_admins[app_name][model_name]

    model_form = forms_handle.create_dynamic_model_form(admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "GET":
        form_obj = model_form(instance=obj)
    else:
        form_obj = model_form(instance=obj,data=request.POST)# instance为当前model的一个对象，即数据库一行数据，所以可以保存

        if form_obj.is_valid():
            form_obj.save()

            return redirect("/bestadmin/%s/%s/"%(app_name,model_name))


    return render(request, "bestadmin/model_change.html",locals())

@permissions.check_permission
@login_required()
def model_add(request,app_name,model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = forms_handle.create_dynamic_model_form(admin_class,form_add=True)

    if request.method == "GET":
        form_obj = model_form()
    else:
        form_obj = model_form(data=request.POST)

        if form_obj.is_valid():
            form_obj.save()

            return redirect("/bestadmin/%s/%s/" % (app_name, model_name))

    return render(request,"bestadmin/model_add.html",locals())



@login_required()
def model_delete(request,app_name,model_name,obj_id):
    admin_class = site.enabled_admins[app_name][model_name]
    objs = admin_class.model.objects.filter(id=obj_id)
    objs_len = len(objs)

    if request.method == "POST":
        objs.delete()
        return redirect("/bestadmin/{app_name}/{model_name}/".format(app_name=app_name,model_name=model_name))

    return render(request,"bestadmin/model_delete.html",locals())



@login_required()
def password_change(request):
    app_name = request.user._meta.app_label
    model_name  = request.user._meta.model_name


    if request.method == "GET":
        change_form = site.enabled_admins[app_name][model_name].add_form(instance=request.user)
    else:

        change_form = site.enabled_admins[app_name][model_name].add_form(request.POST, instance=request.user)
        if change_form.is_valid():

            change_form.save()

            return redirect("/bestadmin/")

    return render(request, 'bestadmin/password_change.html',locals())
