from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, UserLoginForm, AddProductForm
from .models import Book


# Create your views here.
def home(request):
    books = Book.objects.all()

    context = {"books": books}
    return render(request, 'zone/home.html', context)

def signup(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("zone:home")

    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "zone/signup.html", context)

def login_view(request):

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("zone:home")

    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(request, "zone/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("zone:login")

@login_required
def new_item(request):
    form = AddProductForm()

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect("zone:home")

    context = {"form": form}
    return render(request, "zone/new-item.html", context)


@login_required
def edit_item(request, pk=id):

    book = get_object_or_404(Book, pk=pk, created_by=request.user)

    form = AddProductForm(instance=book)

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("zone:home")

    context = {
        "form": form,
        "book": book
        }
    return render(request, "zone/edit-item.html", context)

def detail(request, pk):

    book = get_object_or_404(Book, pk=pk)

    related_books = Book.objects.filter(genre=book.genre).exclude(pk=pk)

    context = {
        "book": book,
        "related_books": related_books,
    }
    return render(request, "zone/detail.html", context)

def delete_view(request, pk):
        book = get_object_or_404(Book, pk=pk, created_by=request.user)

        if request.method == "POST":
            book.delete()
            return redirect("zone:home")

        context = {
            "book": book,
        }
        return render(request, "zone/delete.html", context)

