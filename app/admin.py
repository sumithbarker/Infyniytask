from django.contrib import admin
from app.models import TODO,Employee,Admin
# Register your models here.
@admin.register(TODO)
class TODOAdmin(admin.ModelAdmin):
    list_display=['id','title','status','priority','assigned_to','assigned_by','user']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['user','full_name','address']


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display=['user','full_name','mobile']


