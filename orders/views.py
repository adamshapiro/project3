from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import is_safe_url

from decimal import Decimal

from .forms import RegisterForm, LoginForm
from .models import Food, Topping, ShoppingCart, Order, OrderItem

# Create your views here.
@login_required(login_url='login')
def index(request):
    user = request.user
    # Give a user a shopping cart with a new order if they don't have one.
    if not hasattr(user, 'cart') or not hasattr(user.cart, 'order'):
        user.cart = ShoppingCart.objects.\
            create(owner=user, order=Order.objects.create(user=user, status='o'))

    food = {subclass.__name__:list(Food.objects.instance_of(subclass))
            for subclass in Food.__subclasses__()}

    context = {
        'user': user,
        'food': food,
        'toppings': list(Topping.objects.all()),
        'items': user.cart.order.items.all()
    }
    return render(request, 'orders/index.html', context)

@login_required(login_url='login')
def view_cart(request):
    user = request.user
    items = list(user.cart.order.items.all())

    context = {
        'user': user,
        'items': items
    }
    return render(request, 'orders/cart.html', context)

@login_required(login_url='login')
def confirm_cart(request):
    # when a user confirms their cart, set the order to pending
    user = request.user
    user.cart.order.status = 'p'
    # then get rid of the cart
    user.cart.delete()
    user.cart = None
    # and finally, redirect to index
    return HttpResponseRedirect(reverse('index'))


def add_item(request):
    user = request.user
    price = Decimal(request.GET.get('price'))
    id = int(request.GET.get('food'))
    add_ons = request.GET.get('add_ons', None)
    toppings = request.GET.get('toppings', None)
    # create a new order item based on the request data and add it to the shopping cart
    new_item = OrderItem.objects.create(
        food=Food.objects.get(pk=id),
        price=price,
        order=request.user.cart.order
    )

    # if the requested menu item has add ons, add each to the new OrderItem
    if add_ons is not None:
        for add_on in add_ons.split(','):
            new_item.new_add_on(int(add_on))

    # same as above with toppings
    if toppings is not None:
        for topping in toppings.split(','):
            new_item.new_topping(int(topping))

    # save any updates to the menu item
    new_item.save()

    # return the number of items in the cart to update the 'View Cart' button
    return JsonResponse({
        'success': True,
        'items': len(request.user.cart.order.items.all())
        })

@login_required(login_url='login')
def orders(request):
    # get all the users orders that are not ongoing
    user = request.user
    orders = Order.objects.filter(user=user).exclude(status='o').order_by('status')

    context = {
        'user': user,
        'orders': orders
    }
    return render(request, 'orders/orders.html', context)

@staff_member_required(login_url='index')
def all_orders(request):
    user = request.user
    # get ALL orders that are not ongoing
    pending = Order.objects.filter(status='p')
    confirmed = Order.objects.filter(status='c')

    context = {
        'user': user,
        'pending': pending,
        'confirmed': confirmed
    }
    return render(request, 'orders/all_orders.html', context)

def confirm_order(request):
    # find the requested order and update its status
    id = request.GET.get('order')
    order = Order.objects.get(pk=id)
    order.status = 'c'
    order.save()

    # send the new order info back to the user
    return JsonResponse({
        'success': True,
        'order': str(order),
        'status': order.get_status_display()
        })

def login_view(request):
    # retain the 'next' context and sanitize it
    redirect_to = request.POST.get('next', request.GET.get('next', reverse('index')))
    redirect_to = (redirect_to
                    if is_safe_url(redirect_to, request.get_host())
                    else reverse('index'))

    # On a POST, get the form data
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # authenticate the user and log in if they exist
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(redirect_to)

            # add an error and continue to rendering the login page if user doesn't exist
            form.add_error(None, 'That username and password do not match any user')
    else:
        # generate an empty form on a GET request
        form = LoginForm()
    context = {
        'form': form,
        'new_user': False,
        'next': redirect_to
    }
    return render(request, 'orders/login.html', context)

# similar to login_view (even uses the same html!) but creates a user
# rather than authenticating an existing one
def register_view(request):
    # retain the 'next' context and sanitize it
    redirect_to = request.POST.get('next', request.GET.get('next', reverse('index')))
    redirect_to = (redirect_to
                    if is_safe_url(redirect_to, request.get_host())
                    else reverse('index'))

    # On a POST, get the form data
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # if the form is valid, create a new user and log in
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            login(request, user)
            return HttpResponseRedirect(redirect_to)
    else:
        form = RegisterForm()
    context = {
        'form': form,
        'new_user': True,
        'next': redirect_to
    }
    return render(request, 'orders/login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
