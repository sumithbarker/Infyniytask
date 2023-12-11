from django.db import models
from django.contrib.auth.models import User


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Employee(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200,null=True,blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name



class TODO(models.Model):
    status_choices = [
    ('C', 'COMPLETED'),
    ('P', 'PENDING'),
    ]
    priority_choices = [
    ('1', '1️⃣'),
    ('2', '2️⃣'),
    ('3', '3️⃣'),
    ('4', '4️⃣'),
    ('5', '5️⃣'),
    ('6', '6️⃣'),
    ('7', '7️⃣'),
    ('8', '8️⃣'),
    ('9', '9️⃣'),
    ('10', '🔟'),
    ]
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=2, choices=status_choices)
    date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=2, choices=priority_choices)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assigned_tasks',null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_by_tasks', null=True)
    user  = models.ForeignKey(User  , on_delete= models.CASCADE,null=True)


    def __str__(self):
        return self.title
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, name, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#             name=name,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, name, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             name=name,
#             password=password,
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.save(using=self._db)
#         return user

# class CustomUser(AbstractBaseUser):
#     email = models.EmailField(verbose_name='email', max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#     created_date = models.DateTimeField(auto_now_add=True)

#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self, app_label):
#         return True

# class Role(models.Model):
#     role_id = models.AutoField(primary_key=True)
#     # Add other fields for role if needed

# class UserRole(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)