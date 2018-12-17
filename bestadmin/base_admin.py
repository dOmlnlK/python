from django.shortcuts import render
import json


class BaseAdmin(object):
    def __init__(self):
        self.actions = self.actions + self.default_actions

    list_display = []
    list_filter = []
    search_fields =[]
    readonly_fields = []
    filter_horizontal = []
    list_per_page = 20
    default_actions = ["delete_selected_objects"]
    actions = []

    def delete_selected_objects(self, request, querysets,selected_ids,app_name,model_name):

        return render(request,"bestadmin/model_delete.html",
                      {
                           "objs":querysets,
                           "selected_ids":json.dumps(selected_ids),
                           "app_name":app_name,
                           "model_name":model_name
                                                             }
                      )