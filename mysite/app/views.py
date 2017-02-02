import re
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from app.models import Product

patternLogin = re.compile("^([a-zA-Z0-9]+[\.\-]?){3,}$")
patternEmail = re.compile("^[^\@]+@[^\@]+$")


# Create your views here.

def index(request):
    return render(request, 'index.html')


def products(request):
    count = Product.objects.count()
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products.html', context)


def add_product(request):
    if not request.user.is_authenticated():
        return redirect(products)

    return render(request, 'add_product.html')


def save_product(request):
    if not request.user.is_authenticated():
        return redirect(products)

    if 'product_id' in request.POST:
        product_id = int(request.POST['product_id'].strip())
    else:
        raise Http404()

    if product_id > 0:
        product = get_object_or_404(Product, pk=product_id)
    else:
        product = Product.objects.create()

    if 'name' in request.POST:
        product.name = request.POST['name'].strip()
    else:
        raise Http404()

    if 'count' in request.POST:
        try:
            product.count = int(request.POST['count'].strip())
        except ValueError:
            product.count = 0
    else:
        raise Http404()

    if 'address' in request.POST:
        product.address = request.POST['address'].strip()
    else:
        raise Http404()

    if 'deliv_date' in request.POST:
        try:
            valid_date = datetime.strptime(request.POST['deliv_date'].strip(), "%Y-%m-%dT%H:%M")
            if valid_date != None:
                product.delivery_date = valid_date.strftime('%Y-%m-%d %H:%M')
                print('==========================\n\n\ndate is correct: ')
                print(product.delivery_date)
                print('\n\n\n==========================')
        except:
            print('==========================\n\n\n')
            print('no date')
            print('==========================\n\n\n')

    else:
        return redirect(index)

    product.status = ('status' in request.POST)

    product.save()
    return redirect(products)


def edit_product(request, product_id):
    if not request.user.is_authenticated():
        return redirect(products)

    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}

    return render(request, 'edit_product.html', context)


def remove_product(request, product_id):
    if not request.user.is_authenticated():
        return redirect(products)

    product = get_object_or_404(Product, pk=product_id)
    product.delete()

    return redirect(products)


def sign_up(request):
    if request.user.is_authenticated():
        return redirect('index')

    context = {}
    if 'login' in request.POST:
        login = request.POST['login'].strip()
        if not patternLogin.match(login):
            context['error'] = "Invalid login"

        if 'email' in request.POST:
            email = request.POST['email'].strip()
            if not patternEmail.match(email):
                context['error'] = "Invalid email"
        else:
            raise Http404()

        if 'password' in request.POST:
            password = request.POST.get('password')

            b = bool(re.search(r'[a-z]', password)) and \
                bool(re.search(r'[A-Z]', password)) and \
                bool(re.search(r'[0-9]', password)) and \
                (len(password) > 4)
            if not b:
                context['error'] = "Invalid password"
        else:
            raise Http404()

        if 'password_repeat' in request.POST:
            password_repeat = request.POST.get('password-repeat')
            # if password != password_repeat:
            #     context['error'] = "Invalid repeated password"

        if 'error' in context:
            return render(request, 'sign_up.html', context)
        else:
            try:
                User.objects.get(username=login)
            except User.DoesNotExist:
                user = User.objects.create_user(login, email, password)
                return redirect('index')

    return render(request, 'sign_up.html', context)


def sign_in(request):
    if request.user.is_authenticated():
        return redirect('index')

    context = {}
    if 'login' in request.POST:
        user_login = request.POST['login']

        if 'password' in request.POST:
            password = request.POST['password']
        else:
            raise Http404()

        user = authenticate(username=user_login, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                context['error'] = "Your account is suspended"
        else:
            context['login'] = user_login
            context['error'] = "Invalid username or password"
            return render(request, 'sign_problems.html', context)

        return render(request, 'index.html', context)

    return render(request, 'sign_in.html', context)


def log_out(request):
    logout(request)
    return redirect('index')
