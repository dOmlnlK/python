from django.template import Library
import datetime

register = Library()


@register.simple_tag
def build_tb_row(obj, admin_class):
    """生产一条记录的html"""

    tr_ele = ""
    for index,column_name in enumerate(admin_class.list_display):
        column_obj = admin_class.model._meta.get_field(column_name)  # 拿到字段对象
        if column_obj.choices:
            column_data = getattr(obj, "get_%s_display" % column_name)()
        else:
            column_data = getattr(obj, column_name)

        td_ele = "<td>%s</td>" % column_data

        if index == 0:
            td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id,column_data)

        tr_ele += td_ele

    return tr_ele


@register.simple_tag
def build_filter_ele(filter_column, admin_class):
    column_obj = admin_class.model._meta.get_field(filter_column)

    try:
        ele = "<select name=%s>" % filter_column
        for choice in column_obj.get_choices():  # (0,未报名)
            selected = ""
            if filter_column in admin_class.filter_condition:  # 判断过滤字段是否被选中

                if str(choice[0]) == admin_class.filter_condition.get(filter_column):  #
                    selected = "selected"
            opt_ele = "<option value=%s %s>%s</option>" % (choice[0], selected, choice[1])
            ele += opt_ele

    except AttributeError:
        ele = "<select name=%s__gte>" % filter_column
        if column_obj.get_internal_type() in ("DateField", "DateTimeField"):  # 获取字段对象类型
            time_obj = datetime.datetime.now()
            opt_list = [
                ["", "---------"],
                [time_obj, "今天"],
                [time_obj - datetime.timedelta(7), "七天内"],
                [time_obj.replace(day=1), "一个月内"],
                [time_obj - datetime.timedelta(90), "三个月内"],
                [time_obj.replace(month=1, day=1), "一年内"],

            ]
            for i in opt_list:
                selected = ""
                i[0] = "" if not i[0] else "%s-%s-%s" % (i[0].year, i[0].month, i[0].day)
                if "%s__gte" % filter_column in admin_class.filter_condition:  # 判断过滤字段是否被选中
                    if str(i[0]) == admin_class.filter_condition.get("%s__gte" % filter_column):  #
                        selected = "selected"

                opt_ele = "<option value=%s %s>%s</option>" % (i[0], selected, i[1])
                ele += opt_ele

    ele += "</select>"

    return ele


@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()


@register.simple_tag
def render_filter_args(admin_class):
    """生产过滤参数，用于拼接"""
    if admin_class.filter_condition:
        filter_args = ""
        for k, v in admin_class.filter_condition.items():
            filter_args += "&%s=%s" % (k, v)

        return filter_args
    else:
        return ""


@register.simple_tag
def render_paginator(obj_list,admin_class,current_orderby_column):
    ele = """
    <ul class="pagination">
    """
    filter_args = render_filter_args(admin_class)  #拼接分页和过滤

    orderby_args = ""
    if current_orderby_column:
        orderby_args = list(current_orderby_column.values())[0]

    if obj_list.number - 1 > 0:
        prev_ele = """<li><a href ="?_page=%s%s&_o=%s"> << </a><li>""" % (obj_list.number - 1,filter_args,orderby_args)
        ele += prev_ele

    for i in obj_list.paginator.page_range:
        active = ""

        if obj_list.number == i:
            active = "active"

        if abs(obj_list.number - i) < 2:
            p_ele = '<li class=%s><a href="?_page=%s%s&_o=%s">%s</a></li>' % (active, i, filter_args,orderby_args, i)


            ele += p_ele

    if (obj_list.paginator.num_pages - obj_list.number) > 0:
        next_ele = """<li><a href ="?_page=%s%s&_o=%s"> >> </a><li>""" % (obj_list.number + 1,filter_args,orderby_args)

        ele += next_ele

    ele += "</ul>"
    return ele


@register.simple_tag
def get_orderby_index(current_orderby_column, forloop, column_name):
    # current_orderby_column = {"id":1}
    if column_name in current_orderby_column:  # 判断该字段是否作为排序条件字段
        last_orderby_index = current_orderby_column[column_name]
        if last_orderby_index.startswith("-"):
            this_orderby_index = last_orderby_index.strip("-")
        else:
            this_orderby_index = "-" + last_orderby_index
        return this_orderby_index

    else:
        return forloop


@register.simple_tag
def render_orderby_arrow(current_orderby_column, column_name):
    ele = ""

    if column_name in current_orderby_column:
        if current_orderby_column[column_name].startswith("-"):
            arrow_direction = "alphabet-alt"

        else:
            arrow_direction = "alphabet"

        ele = '''<span class="glyphicon glyphicon-sort-by-%s" aria-hidden="true"></span>''' % arrow_direction


    return ele





@register.simple_tag
def get_current_orderby_index(current_orderby_column):

    val = list(current_orderby_column.values())

    return val[0] if current_orderby_column else ""


@register.simple_tag
def get_readonly_field_val(form_obj,field):
    val = getattr(form_obj.instance,field)

    return val


@register.simple_tag
def get_available_m2m_data(admin_class,field_name,form_obj):
    field_obj = admin_class.model._meta.get_field(field_name)

    field_data_objs = set(field_obj.related_model.objects.all())  #[<Course: python>, <Course: 土木工程>, <Course: java>]
    selected_data_objs = set(getattr(form_obj.instance, field_name).all())
    ele = ""
    for obj in (field_data_objs-selected_data_objs):
        ele += "<option value=%s ondblclick=MoveOption(this,'%s_selected')>%s</option>"%(obj.id,field_name,obj)
        #'%s_selected'  想返回id必须是字符串，不然返回的是一个标签


    return ele


@register.simple_tag
def get_selected_m2m_data(admin_class,field_name,form_obj):
    selected_data_objs = getattr(form_obj.instance,field_name).all()

    ele = ""
    for obj in selected_data_objs:
        ele += "<option value=%s ondblclick=MoveOption(this,'%s_unselected')>%s</option>" % (obj.id, field_name, obj)

    return ele


@register.simple_tag
def display_related_objs(obj):
    """
    obj._meta.fields   找到所有FK
    obj._meta.related_objects   找到所有被关联的FK
    obj._meta.mang_to_many   找到所有m2m

    """
    related_model_objs = obj._meta.related_objects  #(<ManyToOneRel: crm.customerinfos>, <ManyToOneRel: crm.customerfollowup>, <ManyToOneRel: crm.student>)

    ele = "<ul>"
    ele += "<li><a href='/bestadmin/%s/%s/%s/change/'>%s</a></li>"%(obj._meta.app_label,obj._meta.model_name,obj.id,obj)

    for related_model_obj in related_model_objs:
        lookup_related_model_key = "%s_set"%related_model_obj.name   #寻找被关联表的key   表面_set
        related_objs = getattr(obj,lookup_related_model_key).all()    #某一张被关联表下被关联的多条数据



        ele += "<li>%s<ul>"%related_model_obj.name

        if related_model_obj.field.get_internal_type() == "ManyToManyField": #多对多的对象不会删除，不必深入
            for related_obj in related_objs:
                ele += "<li><a href='/bestadmin/%s/%s/%s/change/'>%s</a> 记录里与【%s】相关的数据将被删除</li>" \
                       %(related_obj._meta.app_label,related_obj._meta.model_name,related_obj.id,related_obj,obj)

        else:
            for related_obj in related_objs:

                ele += display_related_objs(related_obj)
        ele += "</ul></li>"




    ele += "</ul>"


    return ele