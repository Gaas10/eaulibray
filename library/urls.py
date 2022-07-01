from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns =[

    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    


    path('',views.home,name="home"),
    path('books',views.books, name="books"),
    path('students',views.students, name="students"),
    path('view_issued_book',views.view_issued_book, name='view_issued_book'),
    path('hello',views.hello, name="hello"),
    path('addbook',views.create_book, name='addbook'),
    path('addstudent',views.addstudent, name='addstudent'),
    path('issuebook',views.issuebook_view, name='issuebook'),

     path('user_page',views.user_page, name="user_page"),

     path('updatebook/<str:pk>/', views.updateBook, name="updatebook"),
     path('deletebook/<str:pk>', views.deletebook, name="deletebook"),
     path('updatestudent/<str:pk>/', views.updatestudent, name="updatestudent"),
     path('deletestudent/<str:pk>', views.deletestudent, name="deletestudent"),

     path('deleteissue/<str:pk>', views.deleteissue, name="deleteissue"),



]