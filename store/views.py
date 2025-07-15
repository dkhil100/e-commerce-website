# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from .models import Product, Category

# Display homepage with categories
def home(request):
    categories = Category.objects.filter(status=False)  # Only visible categories
    return render(request, 'store/home.html', {'categories': categories})

# Store page with all products
def shopping(request):
    products = Product.objects.all()
    return render(request, 'store/store.html', {'products': products})

# Product detail page
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request , 'store/product.html',  {'product': product}) 

# Category detail page
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products,
    })

# User login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return render(request, 'store/home.html')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'store/login.html')
    else:       
        return render(request, 'store/login.html')

# User logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return render(request, 'store/home.html')    

# User registration
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered and logged in successfully.")
            return render(request, 'store/home.html')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    return render(request, 'store/register.html' , {'form': form})
