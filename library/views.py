from multiprocessing import context
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render ,redirect
from django.contrib.auth.models import Group
from django.http import HttpResponse
from .models import *
from datetime import date
from . import forms, models
from .forms import BookForm,StudentUserForm,StudentExtraForm,IssuedBookForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test


from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@unauthenticated_user
def registerPage(request):

    form = StudentUserForm()
    if request.method == 'POST':
        form = StudentUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='STUDENT')
            user.groups.add(group)
            #Added username after video because of error returning customer name if not added
            Student.objects.create(
                user=user,
                name=user.username,
                )

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
        

    context = {'form':form}
    return render(request, 'library/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'library/newlogin.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')
""" def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/index.html')
    else:
        return render(request,'library/arday.html')
 """
@login_required(login_url='login')
#@user_passes_test(is_admin)

def home(request):
    issued=IssuedBook.objects.all()
    books = Book.objects.all()
    students = Student.objects.all()
    total_books = books.count()
    total_students = students.count()
    total_issued=issued.count()
    context = {'books':books, 'students':students,
	'total_books':total_books,'total_students':total_students,'issued':issued,'total_issued':total_issued }
    return render(request, 'library/index.html', context)

#@login_required(login_url='login')
#@user_passes_test(is_admin)
def books(request):
    books = Book.objects.all()
    
    context={
        'books':books,'students':students
    }
    return render(request, 'library/books.html',context)

#@login_required(login_url='login')
#@user_passes_test(is_admin))
def students(request):
    students = Student.objects.all()
    context={
        'students':students
    }

    return render(request,'library/student.html', context)

#@login_required(login_url='login')
#@user_passes_test(is_admin)
def issuebook_view(request):
    form=IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.semester=request.POST.get('semester2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return redirect('view_issued_book')
    return render(request,'library/issueform.html',{'form':form})



#@login_required(login_url='login')
#@user_passes_test(is_admin)
def view_issued_book(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issued_date.day)+'-'+str(ib.issued_date.month)+'-'+str(ib.issued_date.year)
        expdate=str(ib.expiry_date.day)+'-'+str(ib.expiry_date.month)+'-'+str(ib.expiry_date.year)
        #fine calculation
        days=(date.today()-ib.issued_date)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.Student.objects.filter(semester=ib.semester))
        i=0
        for l in books:
            t=(students[i].get_name,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'library/view_issued.html',{'li':li})

def deleteissue(request,pk):

    order = IssuedBook.objects.get(id=pk)
    order.delete()
    return redirect('view_issued_book')


#@login_required(login_url='login')
#@user_passes_test(is_admin)
""" def create_boo(request):
    form=BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            
            user=form.save()
            return render(request,'library/addbook.html')
    context={'form':form}
    return render(request, 'library/addbook.html' ,context)  """

def create_book(request):
    submitted = False
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
          
            user=form.save()
            return redirect('books')
    else:
        form = BookForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request,'library/add.html', {'form':form, 'submitted':submitted
    })

def deletebook(request, pk):
    order = Book.objects.get(id=pk)
    order.delete()
    return redirect('books')


def updateBook(request, pk):

	order = Book.objects.get(id=pk)
	form = BookForm(instance=order)

	if request.method == 'POST':
		form = BookForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('books')

	context = {'form':form}
	return render(request, 'library/add.html', context)


def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('login')
    return render(request,'library/adminsignup.html',{'form':form}) 


#@login_required(login_url='login')
#@user_passes_test(is_admin)
def addstudent(request):
    form1=StudentUserForm()
    form2=StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=StudentUserForm(request.POST)
        form2=StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return redirect('home')

    return render(request,'library/addstudents.html',context=mydict)

def updatestudent(request, pk):

	order = Student.objects.get(id=pk)
	form = StudentExtraForm(instance=order)

	if request.method == 'POST':
		form = StudentExtraForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('home')

	context = {'form':form}
	return render(request, 'library/updatestudent.html', context)

def deletestudent(request, pk):
    order = Student.objects.get(id=pk)
    order.delete()
    return redirect('home')   


def hello(request):


    return render(request, 'library/moh.html' )   


def user_page(request):


    return render(request, 'library/user_page.html' )       