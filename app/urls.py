
from django.contrib import admin
from django.urls import path
from app.views import home , login , signup , adminadd_todo , signout , delete_todo_user, change_todo, admin_home, admin_login, useradd_todo, update_task_assignment, delete_todo_admin, admin_change_todo


urlpatterns = [
   path('' , home , name='home' ),
   path('login/' ,login  , name='login'),
   path('signup/' , signup ),
   path('adminadd-todo/' , adminadd_todo ),
   path('useradd-todo/' , useradd_todo ,), 
   # path('assign-task/<int:user_id>/<int:task_id>/', assign_task, name='assign_task'),
   path('delete-todo-user/<int:id>/', delete_todo_user, name='delete_todo_user' ),
   path('change-status/<int:id>/<str:status>/' , change_todo ),
   path('logout/' , signout ),
   path('admin-login/',admin_login, name='admin_login'),
   path('admin-home/',admin_home, name='admin_home'),
   path('update-task/<int:task_id>/', update_task_assignment, name= 'update_task_assignment'),
   path('delete-todo-admin/<int:todo_id>/',delete_todo_admin, name='delete_todo_admin'),
   path('admin-change-todo/<int:id>/<str:status>/' , admin_change_todo ),
  
   #path('user_profile/',user_profile, name='user_profile'),

]