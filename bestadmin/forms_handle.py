from django.forms import ModelForm


def create_dynamic_model_form(admin_class,form_add=False):
    """生产动态model_form"""

    class Meta:
        model = admin_class.model
        fields = "__all__"

        if not form_add:
            exclude = admin_class.readonly_fields



    def __new__(cls,*args,**kwargs):  #重写父类__new__方法
        for field_name in cls.base_fields:   #cls.base_fields 表所有字段类型
            field_obj = cls.base_fields[field_name]  #cls.base_fields 表字段类型对象
            field_obj.widget.attrs.update({"class":"form-control"})
        return ModelForm.__new__(cls)

    DynamicModelForm = type("DynamicModelForm",(ModelForm,),{"Meta":Meta,"__new__":__new__})
    return DynamicModelForm