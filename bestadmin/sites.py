from bestadmin import base_admin


class AdminSite(object):
    def __init__(self):
        """{app_name:{model_name:admin_class,model_name:admin_class}}"""
        self.enabled_admins = {}

    def register(self, model_class, admin_class=None):
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name

        if not admin_class:
            admin_class = base_admin.BaseAdmin()   #先创建实例对象，防止多个model使用同一个BaseAdmin对象
        else:
            admin_class = admin_class()

        admin_class.model = model_class

        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class


site = AdminSite()
