from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_users, admin_only
from .models import *
from .forms import *
from .filter import CustomerFilter



# Create your views here.
@unauthenticated_user
def registerPage(request):    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user,name=user.username,email=user.email,)

            messages.success(request,'Account was created for '+username)
            return redirect('login')
    context={'form':form}
    return render(request,'BooksApp/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username OR Password is incorrct')
    context={}
    return render(request,'BooksApp/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    books = Book.objects.all()
    totalCustomers = customers.count()
    totalBooks = books.count()
    context={'customers':customers,'books':books,'totalCustomers':totalCustomers,'totalBooks':totalBooks,}
    return render(request,'BooksApp/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    books = request.user.customer.book_set.all()
    totalBooks = books.count()
    context={'books':books,'totalBooks':totalBooks}
    return render(request,'BooksApp/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    books = customer.book_set.all()
    booksCount = books.count()
    context = {'customer':customer,'books':books,'booksCount':booksCount}
    return render(request,'BooksApp/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addBook(request,pk):
    BookFormSet = inlineformset_factory(Customer,Book,fields=('Bookname','author','price'),extra=10)
    customer = Customer.objects.get(id=pk)
    formset = BookFormSet(queryset=Book.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = BookFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset,'customer':customer}
    return render(request,'BooksApp/book_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def addBookUser(request,pk):
    BookFormSet = inlineformset_factory(Customer,Book,fields=('Bookname','author','price'),extra=5)
    customer = Customer.objects.get(id=pk)
    formset = BookFormSet(queryset=Book.objects.none(),instance=customer)

    if request.method == 'POST':
        formset = BookFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset,'customer':customer}
    return render(request,'BooksApp/book_form_user.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addCustomer(request):
    form = CustomerForm()
    context={'form':form}

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'BooksApp/customer_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateBook(request,pk):    
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST,instance=book)
        if form.is_valid():
            form.save()
            return redirect('/')   
    context = {'form':form}
    return render(request,'BooksApp/update_book.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateBookUser(request,pk):
    book = Book.objects.get(id=pk)
    form = BookFormUser(instance=book)

    if request.method == 'POST':
        form = BookFormUser(request.POST,instance=book)
        if form.is_valid():
            form.save()
            return redirect('/')   
    context = {'form':form}
    return render(request,'BooksApp/update_book_user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request,pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)    

    if request.method == 'POST':
        form = CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'BooksApp/customer_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteBook(request,pk):
    book = Book.objects.get(id=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('/')
    context={'book':book}
    return render(request,'BooksApp/delete_book.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def deleteBookUser(request,pk):
    book = Book.objects.get(id=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('/')
    context={'book':book}
    return render(request,'BooksApp/delete_book_user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request,pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')
    context = {'customer':customer}
    return render(request,'BooksApp/delete_customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def makeAdmin(request,pk):
    customer = Customer.objects.get(id=pk)
    user = customer.user

    if request.method == 'POST':
        group = Group.objects.get(name='admin')
        group1 = Group.objects.get(name='customer')
        user.groups.add(group)
        user.groups.remove(group1)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        customer.delete()
        return redirect('/')
    context = {'user':user}
    return render(request,'BooksApp/make_admin.html',context)
