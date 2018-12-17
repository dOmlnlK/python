from crm import models
from bestadmin.sites import site
from bestadmin.base_admin import BaseAdmin
from  django import forms

class CustomerInfosAdmin(BaseAdmin):
    list_display = ["id","name","source","contact_type","contact","consultant","consult_content","status","date"]
    list_filter = ["consultant","source","status","date"]  #设置过滤
    search_fields = ["id","name","source"]     #设置搜索
    readonly_fields = ['status',"contact"]     #设置字段为只读
    filter_horizontal = ["consult_courses",]   #将字段设置成两个select框  方便多数据时选择
    list_per_page = 3
    actions = ["change_status"]

    def change_status(self,request,querysets):
        querysets.update(status=1)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


    class Meta:
        model = models.UserInfos
        fields = ('email','name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if len(password1) < 6:
            raise forms.ValidationError("Passwords takes at least 6 letters")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user




class UserInfosAdmin(BaseAdmin):
    add_form = UserCreationForm
    model =  models.UserInfos
    list_display = ('id','email','is_staff')
    readonly_fields = ['password',]
    change_page_onclick_fields = {
        'password':['password','重置密码']
    }
    filter_horizontal = ('user_permissions','roles')
    list_editable = ['is_superuser']

site.register(models.UserInfos,UserInfosAdmin)
site.register(models.Student)
site.register(models.CustomerInfos,CustomerInfosAdmin)
site.register(models.Course)
site.register(models.ClassList)


