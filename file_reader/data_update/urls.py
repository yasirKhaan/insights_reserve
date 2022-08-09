from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('existing-schema/', views.existing_schema, name='existing_schema'),
    path('new-schema/', views.migrate_to_new_schema, name='migrate-to-new-schema'),
    path('ins-del-upt/', views.insert_update_delete, name='ins_del_upt'),
    path('del-table-schema/', views.delete_table_or_schema, name='delete_table_schema'),

]
