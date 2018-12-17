from bestadmin import permission_hook

perm_dic= {

    #'crm_table_index': ['table_index', 'GET', [], {'source':'qq'}, ],  # 可以查看CRM APP里所有数据库表
    'crm_model_detail': ['model_detail', 'GET', [], {} ],  # 可以查看每张表里所有的数据
    'crm_model_change_view': ['model_change', 'GET', [], {}],  # 可以访问表里每条数据的修改页
    'crm_model_change': ['model_change', 'POST', [], {}],  # 可以对表里的每条数据进行修改
    'crm_model_add_view': ['model_add', 'GET', [], {}],  # 可以访问数据增加页
    'crm_model_add': ['model_add', 'POST', [], {}],  # 可以添加每张表里的数据

}



