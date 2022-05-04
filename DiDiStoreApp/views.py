import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .cart import Cart
from .forms import ProfileUserForm, ProfielExtrForm, LoginForm, OrderCreateForm
from .models import Category, Book, Publisher, Author, Profile, OrderItem, Order


def is_client(user):
    return user.groups.filter(name='CLIENT').exists()


def afterlogin_view(request):
    if is_client(request.user):
        accountapproval=Profile.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('account')


def index(request):
    form = ProfileUserForm()
    form2 = ProfielExtrForm()
    form3 = LoginForm()
    if request.method == "POST":
        form = ProfileUserForm(request.POST)
        form2 = ProfielExtrForm(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            user2 = form2.save(commit=False)
            user2.user = user
            user2.save()
            my_profile_group = Group.objects.get_or_create(name="CLIENT")
            my_profile_group[0].user_set.add(user)
            return redirect("home")

    if request.method == "POST":
        form3 = LoginForm(request.POST)
        if form3.is_valid():
            user3 = authenticate(username=form3.cleaned_data['username'], password=form3.cleaned_data['password'])
            if user3 is not None:
                login(request, user3)
                return redirect("afterlogin_view")

    category = Category.objects.all()
    books = Book.objects.all()
    context = {
        "category":category,
        "books":books,
        "form": form,
        "form2": form2,
        "form3": form3,
    }
    return render(request, 'DiDiStoreApp/index.html',context)

def show_category(request, id):
    category = Category.objects.all()
    books  = Book.objects.filter(category_id=id)
    context = {
        "category" : category,
        "books" : books,
    }
    return render(request, "DiDiStoreApp/index.html",context)


@user_passes_test(is_client)
def account(request):
    count_order_item = OrderItem.objects.filter(order__customer_id=request.user.id).count()
    profile = get_object_or_404(Profile,user_id=request.user.id)
    user = get_object_or_404(User, id=request.user.id)
    profile_order = Order.objects.filter(customer_id=request.user.id)
    context = {
        "profile_order":profile_order,
        "profile" : profile,
        "user": user,
        "count_order_item" : count_order_item,
    }
    return render(request, 'DiDiStoreApp/account.html', context)


def details(request, id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=id)
    author = Author.objects.filter(book__category_id=id)

    context = {
        "cart": cart,

        "book" : book,
        "author":author,
    }
    return render(request, 'DiDiStoreApp/details.html',context)


def searches(request):
    category = Category.objects.all()
    searches_post = request.GET.get("search")
    if searches_post:
        books = Book.objects.filter(Q(name__icontains=searches_post))
    context = {
        "books" : books,
        "category" : category,
    }
    return render(request,"DiDiStoreApp/index.html",context)

@user_passes_test(is_client)
def cart_add(request, bookid):
    cart = Cart(request)
    book = get_object_or_404(Book, id=bookid)
    cart.add(book=book)
    return redirect('card_details')



@user_passes_test(is_client)
def cart_remove(request, bookid):
    cart = Cart(request)
    book = get_object_or_404(Book, id=bookid)
    cart.remove(book)
    return redirect('card_details')

@user_passes_test(is_client)
def cart_details(request):
    cart = Cart(request)
    context = {
        "cart": cart,
    }
    return render(request, 'DiDiStoreApp/desired.html', context)

@user_passes_test(is_client)
def order_create(request):
    profile = get_object_or_404(Profile, user_id=request.user.id)
    cart = Cart(request)
    if request.user.is_authenticated:
        customer = get_object_or_404(User, id=request.user.id)
        profile = Profile.objects.get(user_id=request.user.id)
        form = OrderCreateForm(request.POST or None, initial={"cvv_iin":profile.cvv_iin,"bank_iin":profile.bank_iin,"iin":profile.iin,"name": customer.first_name, "email": customer.email,"address":profile.address})
        if request.method == 'POST':
            if form.is_valid():
                order = form.save(commit=False)
                order.transaction_id = random.randint(request.user.id,100000)
                order.customer = User.objects.get(id=request.user.id)
                order.totalbook = len(cart)  # len(cart.cart) // number of individual book
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        book=item['book'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                cart.clear()
                return render(request, 'DiDiStoreApp/scc.html', {'order': order})

            else:
                messages.error(request, "Fill out your information correctly.")
        cart = Cart(request)
        if len(cart) > 0:
            return render(request, 'DiDiStoreApp/payments.html', {"form": form,"profile":profile,"cart":cart})
        else:
            return redirect('home')
    else:
        return redirect('home')



@user_passes_test(is_client)
def profile_report(request):
    profile = get_object_or_404(User,id=request.user.id)
    order_items = OrderItem.objects.filter(order__customer_id=request.user.id).order_by("-id")

    context = {
        "profile" : profile,
        "orders_items": order_items,
    }
    return render(request, "DiDiStoreApp/table_buy.html",context)

