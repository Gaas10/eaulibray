from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime,timedelta

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    status = models.CharField(max_length=25, choices=(('Active','Active'), ('Inactive','Inactive')), default = 'Active')
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

  
    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'
    


class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #name = models.CharField(max_length=250,blank=True, null= True)
    #middle_name = models.CharField(max_length=250, blank=True, null= True)
    #last_name = models.CharField(max_length=250,blank=True, null= True)
    department = models.CharField(max_length=250, blank= True, null = True)
    semester = models.CharField(max_length=250, blank= True, null = True)
    roll_no = models.CharField(max_length=15, blank=True)
    image = models.ImageField(null= True,  blank=True, upload_to="profile/", default="profile/profile.jpg")
    gender = models.CharField(max_length=20, choices=(('Male','Male'), ('Female','Female')), default = 'Male')
    contact = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    
    status = models.CharField(max_length=20, choices=(('Active','Active'), ('Inactive','Inactive')), default = 'Active')
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    #used in issue book
    def __str__(self):
        return str(self.user) +   " ["+str(self.semester)+']'
    
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id
   
   

def expiry():
    return datetime.today() + timedelta(days=14)

class IssuedBook(models.Model):
    #student_id = models.ForeignKey(Student, on_delete= models.CASCADE, related_name="student_id_fk")
    #isbn = models.ForeignKey(Book, on_delete= models.CASCADE, related_name="book_id_fk")
    semester = models.CharField(max_length=100, blank=True) 
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
   
    status = models.CharField(max_length=2, choices=(('1','Pending'), ('2','Returned')), default = 1)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.semester
    
