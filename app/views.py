from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from app.forms import TODOForm,CustomerRegistrationForm
from app.models import TODO,Admin,User,Employee
from .forms import AdminLoginForm
from django.contrib.auth.decorators import login_required
# from app.models import CustomUser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# @login_required(login_url='login')
# def home(request):
#     print(request.GET)
#     if request.user.is_authenticated:
#         user_id = request.user.id
#         emp_id = Employee.objects.filter(user_id=user_id).values('id')[0]

#         todos = TODO.objects.filter(assigned_to = emp_id['id']).order_by('priority')
#         return render(request , 'index.html' , context={'todos' : todos})
    
@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        emp_qs = Employee.objects.filter(user_id=user_id).values('id')
        
        if emp_qs.exists():  # Check if the queryset has results
            emp_id = emp_qs[0]['id']  # Access the first element if available
            todos = TODO.objects.filter(assigned_to=emp_id).order_by('priority')
            return render(request, 'index.html', context={'todos': todos})
    
    # Return an empty queryset or handle the case where emp_qs doesn't have results
    return render(request, 'index.html', context={'todos': []})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {"form": form}
        return render(request, 'login.html', context=context)
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and Employee.objects.filter(user_id = user).exists():
                loginUser(request, user)
                return redirect('home')
            else:
                # Handle case where user is not superuser

                form.add_error(None, 'Invalid login credentials for superuser')
        # If form is not valid, return with the form and errors
        context = {"form": form}
        return render(request, 'login.html', context=context)


def signup(request):

    if request.method == 'GET':
        form = CustomerRegistrationForm()
        context = {
            "form" : form
        }
        return render(request , 'signup.html' , context=context)
    else:
        print(request.POST)
        form = CustomerRegistrationForm(request.POST)
        context = {
            "form" : form
        }
        print(context)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            user = User.objects.create_user(username,email,password)
            form.instance.user = user
            form.save()

            if user is not None:
                return redirect('login')
        else:
            return render(request , 'signup.html' , context=context)



# @login_required(login_url='login')
# def add_todo(request):
#     if request.user.is_authenticated:
#         user = request.user
#         print(user)
#         form = TODOForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             todo = form.save(commit=False)
#             todo.user = user
#             todo.save()
#             print(todo)
#             return redirect("home")
#         else:
#             return render(request , 'index.html' , context={'form' : form})
        
# @login_required(login_url='login')
# def useradd_todo(request):
#     if request.user.is_authenticated:
#         user = request.user
#         print(user)
#         form = TODOForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             todo = form.save(commit=False)
#             todo.user = user
#             todo.save()
#             print(todo)
#             return redirect("home")
#         else:
#             return render(request , 'index.html' , context={'form' : form})

@login_required(login_url='login')
def useradd_todo(request):
    print("carrrr")
    if request.user.is_authenticated:
        user = request.user  # This represents the logged-in user
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user  # Associate the TODO with the logged-in CustomUser
            todo.save()
            return redirect("home")
        else:
            return render(request, 'index.html', context={'form': form})
# @login_required(login_url='login')
# def adminadd_todo(request):
#     print('jaguaar')
#     if request.user.is_authenticated:
#         user = request.user  # This represents the logged-in user
#         form = TODOForm(request.POST)
#         if form.is_valid():
#             todo = form.save(commit=False)
#             todo.user = user  # Associate the TODO with the logged-in CustomUser
#             todo.save()
#             return redirect("admin_home")
#         else:
#             return render(request, 'index.html', context={'form': form})




# def delete_todo_user(request , id ):
#     print(id)
#     todo= TODO.objects.get(pk = id).delete()

#     if todo.user == request.user:
#         todo.delete()

#     return redirect('home')





def change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')


def signout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def adminadd_todo(request):
    print('jaguaar')
    if request.user.is_authenticated:
        user = request.user  # This represents the logged-in user
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user  # Associate the TODO with the logged-in CustomUser
            todo.save()
            return redirect("admin_home")
        else:
            return render(request, 'index.html', context={'form': form})


def some_view(request):
    custom_users = CustomUser.objects.filter(is_superuser=True)
    return render(request, 'user_list.html', {'custom_users': custom_users})



def admin_login(request):
    if request.method == 'GET':
        print('book')
        form = AdminLoginForm() 
        context = {"form": form}
        return render(request, 'admin_login.html', context=context)
    else:
        form = AdminLoginForm(data=request.POST)
        print('flower')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data['password']
            usr = authenticate(username=username, password=password)
            if usr is not None and Admin.objects.filter(user = usr).exists():
                loginUser(request, usr)
                return redirect('admin_home')
        context = {"form": form}
        return render(request, 'admin_login.html', context=context)
    

from django.contrib.auth import login as loginUser, authenticate

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data['password']
            usr = authenticate(username=username, password=password)
            if usr is not None and Admin.objects.filter(user=usr).exists():
                # Create a session for the logged-in user
                loginUser(request, usr)
                request.session['admin_logged_in'] = True  # Example session key for admin login
                return redirect('admin_home')
        else:
            context = {"form": form}
            return render(request, 'admin_login.html', context=context)
    else:
        form = AdminLoginForm()
        context = {"form": form}
        return render(request, 'admin_login.html', context=context)
    
from django.contrib.auth import logout

def admin_logout(request):
    if 'admin_logged_in' in request.session:
        del request.session['admin_logged_in']
    logout(request)
    return redirect('admin_login')





# @login_required(login_url='login')
# def admin_home(request):
#     form = TODOForm()
#     context ={
#         'form':form
#     }
#     return render(request, 'admin_home.html',context)

# @login_required(login_url='login')
# def admin_home(request):
#     form = TODOForm()
#     users = User.objects.all()  # Fetch all users
#     context ={
#         'form': form,
#         'users': users  # Pass the users to the context
#     }
#     return render(request, 'admin_home.html', context)

@login_required(login_url='login')
def admin_home(request):
    form = TODOForm()
    users = User.objects.all()  # Fetch all users
    context = {
        'form': form,
        'users': users  # Pass the users to the context
    }
    return render(request, 'admin_home.html', context)


@login_required(login_url='login')
def admin_home(request):
    form = TODOForm()
    todos = TODO.objects.all().order_by('id')
    context ={
        'form':form,
        'todos':todos
    }
    return render(request, 'admin_home.html',context)






# @staff_member_required
# def update_task_assignment(request, task_id):
#     task = get_object_or_404(TODO, pk=task_id)
    
#     if request.method == 'POST':
#         form = TODOForm(request.POST, instance=task)
#         if form.is_valid():
#             new_assigned_employee_name = form.cleaned_data.get('assigned_to')  # Assuming 'assigned_to' is the field name
#             new_assigned_employee = Employee.objects.get(full_name=new_assigned_employee_name)
            
#             # Update the task assignment to employee2
#             task.assigned_to = new_assigned_employee
#             task.save()
            
#             # Delete the task assigned to employee1
#             task.delete(task.assigned_to)
            
#             return redirect("admin-home")  # Redirect to whatever page you want after updating the task
#     else:
#         form = TODOForm(instance=task)
    
    # return render(request, 'update_task.html', {'form': form, 'task_id': task_id})

from django.contrib import messages

@login_required(login_url='login')              #for admin
def update_task_assignment(request, task_id):   
    task = get_object_or_404(TODO, pk=task_id)
    
    if request.method == 'POST':
        form = TODOForm(request.POST, instance=task)
        if form.is_valid():
            new_assigned_employee_name = form.cleaned_data.get('assigned_to')  # Assuming 'assigned_to' is the field name
            new_assigned_employee = Employee.objects.get(full_name=new_assigned_employee_name)
            
            # Update the task assignment to new employee
            task.assigned_to = new_assigned_employee
            task.save()
            
            # Optionally, if you want to delete the task assigned to the original employee
            original_assigned_employee = task.assigned_to
            if original_assigned_employee != new_assigned_employee:
                # Remove the task from the original employee
                task.assigned_to = None
                task.save()
            
            messages.success(request, 'Task assignment updated successfully.')
            return redirect('admin_home')  # Redirect after updating the task
    else:
        form = TODOForm(instance=task)
    
    return render(request, 'update_task.html', {'form': form, 'task_id': task_id})




@login_required(login_url='login')              #for user
def update_task_assignment(request, task_id):   
    task = get_object_or_404(TODO, pk=task_id)
    
    if request.method == 'POST':
        form = TODOForm(request.POST, instance=task)
        if form.is_valid():
            new_assigned_employee_name = form.cleaned_data.get('assigned_to')  # Assuming 'assigned_to' is the field name
            new_assigned_employee = Employee.objects.get(full_name=new_assigned_employee_name)
            
            # Update the task assignment to new employee
            task.assigned_to = new_assigned_employee
            task.save()
            
            # Optionally, if you want to delete the task assigned to the original employee
            original_assigned_employee = task.assigned_to
            if original_assigned_employee != new_assigned_employee:
                # Remove the task from the original employee
                task.assigned_to = None
                task.save()
            
            messages.success(request, 'Task assignment updated successfully.')
            return redirect('home')  # Redirect after updating the task
    else:
        form = TODOForm(instance=task)
    
    return render(request, 'update_task.html', {'form': form, 'task_id': task_id})


# @login_required(login_url='login')
# def delete_todo_admin(request, todo_id):
#     todo = TODO.objects.get(pk=todo_id)
#     todo.delete()
#     return redirect('admin_home')

@login_required(login_url='login')
def delete_todo_admin(request, todo_id):
    todo = TODO.objects.get(pk=todo_id)
    
    # Check if the task was assigned by an admin
    if todo.user == request.user:
        todo.delete()
    
    return redirect('admin_home')

# @login_required(login_url='login')
# def delete_todo_user(request, todo_id):
#     print('bikeee')
#     todoo = TODO.objects.get(pk=todo_id)
    
#     # Check if the task was assigned by the logged-in user (employee)
#     if todoo.user == request.user:
#         todoo.delete()
    
#     return redirect('home')

# def delete_todo_user(request , id ):
#     print(id)
#     TODO.objects.get(pk = id).delete()
#     return redirect('home')

@login_required(login_url='login')
def delete_todo_user(request, id):
    print("yayy")
    todo = get_object_or_404(TODO, pk=id)

    # Assuming there's a field in the TODO model named 'assigned_to' referencing the Employee
    # Replace 'assigned_to' with the actual field that references the Employee model
    if todo.user == request.user:  # Assuming request.user contains the logged-in user
        todo.delete()
    
    

    return redirect('home')

@login_required(login_url='login')
def admin_change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('admin_home')


@login_required(login_url='login')
def admin_home(request):
    form = TODOForm()
    todos = TODO.objects.all().order_by('id')

    # Set the number of items to display per page
    items_per_page = 8
    paginator = Paginator(todos, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')
  

    try:
        # Get the requested page
          paginated_todos = paginator.page(page)

    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
          paginated_todos = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page
          paginated_todos = paginator.page(paginator.num_pages)

    context ={
        'form': form,
        'paginated_todos': paginated_todos
    }

    return render(request, 'admin_home.html', context)


def user_todo_view(request):
    user = request.user  # Assuming user authentication is set up

    # Fetch todos based on user's role or relationship to tasks
    if user.is_admin:
        todos = TODO.objects.all()  # Fetch all tasks for admin
    else:
        # For non-admin users, filter tasks based on assignment
        todos = TODO.objects.filter(assigned_to=user.employee)

    context = {
        'todos': todos,
        'user': user,
    }
    return render(request, 'index.html', context)

def display_tasks(request):
    # Fetch all TODO tasks
    todos = TODO.objects.all()

    context = {
        'todos': todos,
        # Add other context variables if needed
    }

    return render(request, 'admin_home.html', context)









from django.contrib.auth import authenticate, login, logout

def login(request):
    if request.method == 'POST':
        # Validate user credentials
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log in the user using Django's login function
            # Redirect to the appropriate page after login
            return redirect('home')  # Replace 'home' with your desired URL name
        else:
            # Handle invalid login credentials
            # Render login page with error message, etc.
            pass  # Placeholder for error handling logic

    # Handle GET request (render login form)
    # Render your login template
    return render(request, 'login.html')

@login_required(login_url='login')  # Use this decorator to protect views that require authentication
def signout(request):
    logout(request)  # Log out the user using Django's logout function
    return redirect('login')  # Redirect to the login page after logout



def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {"form": form}
        return render(request, 'login.html', context=context)
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and Employee.objects.filter(user_id=user).exists():
                loginUser(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid login credentials for superuser')

        context = {"form": form}
        return render(request, 'login.html', context=context)

# @login_required(login_url='login')
# def admin_home(request):
#     form = TODOForm()
#     todos = TODO.objects.all().order_by('id')
#     context ={
#         'form':form,
#         'todos':todos
#     }
#     return render(request, 'admin_home.html',context)

# from django.shortcuts import redirect
# from app.models import TODO, Employee

# @login_required(login_url='login')
# def assign_task(request, user_id, task_id):
#     if request.user.is_authenticated:
#         # Assuming 'user_id' represents the Employee ID to whom the task is being assigned
#         employee = Employee.objects.get(pk=user_id)  # Fetch the Employee instance

#         # Assuming 'task_id' represents the ID of the task being assigned
#         task = TODO.objects.get(pk=task_id)  # Fetch the TODO task instance

#         if employee and task:
#             task.assigned_to = employee  # Assign the task to the Employee
#             task.save()
#             # Perform any additional logic related to task assignment if needed
#             return redirect('admin_home')  # Redirect to the admin home page after task assignment
#         else:
#             # Handle cases where Employee or TODO task doesn't exist
#             # Redirect or render an error page as needed
#             pass  # Placeholder for error handling logic
#     else:
#         # Handle cases where the user is not authenticated
#         # Redirect to the login page or render an error page as needed
#         pass  # Placeholder for authentication failure handling logic






# def admin_login(request):
#     if request.method == 'GET':
#         if request.user.is_authenticated and request.user.is_superuser:
#             form = AdminLoginForm()  # Use the AdminLoginForm for admin login
#         else:
#             form = AuthenticationForm()  # Use the regular AuthenticationForm for non-admin users
#         context = {"form": form}
#         return render(request, 'admin_login.html', context=context)
#     elif request.method == 'POST':
#         if request.user.is_authenticated and request.user.is_superuser:
#             form = AdminLoginForm(data=request.POST)  # Validate AdminLoginForm for admin users
#         else:
#             form = AuthenticationForm(data=request.POST)  # Validate AuthenticationForm for non-admin users
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None and user.is_superuser:
#                 loginUser(request, user)
#                 return redirect('admin_home')
#             # Add additional logic or error handling for regular users
#         context = {"form": form}
#         return render(request, 'admin_login.html', context=context)