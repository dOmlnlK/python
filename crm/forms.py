from django.forms import ModelForm
from crm import models



class CustomerInfo(ModelForm):
    def __new__(cls, *args, **kwargs):  # 重写父类__new__方法
        for field_name in cls.base_fields:  # cls.base_fields 表所有字段类型
            field_obj = cls.base_fields[field_name]  # cls.base_fields 表字段类型对象
            field_obj.widget.attrs.update({"class": "form-control"})

        for field_name in cls.Meta.readonly_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({"disabled":"True"})

        return ModelForm.__new__(cls)

    def clean(self): #定制父类验证方法

        if self.instance.id is not None:
            for field in self.Meta.readonly_fields:
                old_field_val = getattr(self.instance,field)
                new_field_val = self.cleaned_data[field]

                if old_field_val != new_field_val:
                    """添加字段错误"""
                    self.add_error(field,"Readonly Field: this field should be %s ,not %s."%(old_field_val,new_field_val))

    class Meta:
        model = models.CustomerInfos
        fields = "__all__"
        exclude = ["consult_content","consult_courses","status"]
        readonly_fields = ["contact_type","contact","consultant","referral_from","source"]




class AuditForm(ModelForm):
    def __new__(cls, *args, **kwargs):  # 重写父类__new__方法
        for field_name in cls.base_fields:  # cls.base_fields 表所有字段类型
            field_obj = cls.base_fields[field_name]  # cls.base_fields 表字段类型对象
            field_obj.widget.attrs.update({"class": "form-control"})

        for field_name in cls.Meta.readonly_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({"disabled": "True"})

        return ModelForm.__new__(cls)

    def clean(self):  # 定制父类验证方法

        if self.instance.id is not None:
            for field in self.Meta.readonly_fields:
                old_field_val = getattr(self.instance, field)
                new_field_val = self.cleaned_data[field]

                if old_field_val != new_field_val:
                    """添加字段错误"""
                    self.add_error(field,
                                   "Readonly Field: this field should be %s ,not %s." % (old_field_val, new_field_val))

    class Meta:
        model = models.StudentEnrollment
        fields = "__all__"
        exclude = ["contract_approved_date"]
        readonly_fields = ["contract_argeed"]