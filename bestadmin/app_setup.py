from django import conf


def bestadmin_auto_load():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            mod = __import__("%s.bestadmin" % (app_name))
        except ImportError:
            pass