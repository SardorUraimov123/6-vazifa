from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main import models

def index(request):
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    reviews = models.Review.objects.all()
    mark = 0
    for i in reviews:
        mark += i.mark
    
    mark = int(mark/len(reviews)) if reviews else 0

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = models.Product.objects.get(id=product_id)
        cart = models.Cart.objects.filter(is_active=True)
        is_product = models.CartProduct.objects.filter(product=product,cart__is_active=True).first()
        if is_product:
            is_product.count += 1
            is_product.save()
            return redirect('front:active_cart')
        if not cart:
            cart = models.Cart.objects.create(
                user=request.user,
                is_active=True
            )
        
        models.CartProduct.objects.create(
            product=product,
            cart=cart.first(),
            count=1
        )
        return redirect('front:active_cart')

    context = {
        'categories':categories,
        'products':products,
        'rating':range(1,6),
        'mark':mark,
        }
    return render(request, 'front/index.html',context)

def product_detail(request,code):
    product = models.Product.objects.get(code=code)
    reviews = models.Review.objects.filter(product=product)
    images = models.ProductImg.objects.filter(product=product)
    mark = 0

    for i in reviews:
        mark += i.mark

    mark = int(mark/len(reviews)) if reviews else 0

    if request.method == 'POST':
        try:
            is_product = models.CartProduct.objects.get(product=product,cart__is_active=True)
            if is_product:
                is_product.count += int(request.POST.get('count'))
                is_product.save()
                return redirect('front:active_cart')
        except models.CartProduct.DoesNotExist:
            pass
        cart = models.Cart.objects.filter(is_active=True)
        if not cart:
            cart = models.Cart.objects.create(
                user=request.user,
                is_active=True
            )
        cart = models.Cart.objects.get(is_active=True)
        models.CartProduct.objects.create(
            product=product,
            cart=cart,
            count=request.POST.get('count')
        )
        return redirect('front:active_cart')

    context = {
        'product':product,
        'mark':mark,
        'rating':range(1,6),
        'images':images,
        'reviews':reviews,
    }
    return render(request, 'front/product/detail.html',context)

def product_list(request,code):
    queryset = models.Product.objects.filter(category__code=code)
    categories = models.Category.objects.all()
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = models.Product.objects.get(id=product_id)
        cart = models.Cart.objects.filter(is_active=True)
        try:
            is_product = models.CartProduct.objects.get(product=product,cart__is_active=True)
            if is_product:
                is_product.count += int(request.POST.get('count'))
                is_product.save()
                return redirect('front:active_cart')
        except models.CartProduct.DoesNotExist:
            pass
        cart = models.Cart.objects.filter(is_active=True)
        if not cart:
            cart = models.Cart.objects.create(
                user=request.user,
                is_active=True
            )
        cart = models.Cart.objects.get(is_active=True)
        models.CartProduct.objects.create(
            product=product,
            cart=cart,
            count=1
        )
        return redirect('front:active_cart')
    
    context = {
        'queryset':queryset,
        'categories':categories,
        }
    return render(request, 'front/category/product_list.html',context)

def product_delete(request,id):
    product = models.CartProduct.objects.get(id=id)
    product.delete()
    return redirect('front:active_cart')

@login_required(login_url='auth:login')
def carts(request):
    queryset = models.Cart.objects.filter(user=request.user, is_active=False)
    context = {'queryset':queryset}
    return render(request, 'front/carts/list.html', context)


@login_required(login_url='auth:login')
def active_cart(request):
    queryset , _ = models.Cart.objects.get_or_create(user=request.user, is_active=True)
    return redirect('front:cart_detail', queryset.code)


@login_required(login_url='auth:login')
def cart_detail(request, code):
    cart = models.Cart.objects.get(code=code)
    queryset = models.CartProduct.objects.filter(cart=cart)
    if request.method == 'POST':
        cart.is_active = False
        cart.save()
        data = list(request.POST.items())[1::]
        for id,value in data:
            product = models.CartProduct.objects.get(id=id)
            product.count = value
            product.save()
    context = {
        'cart': cart,
        'queryset':queryset
        }
    return render(request, 'front/carts/detail.html', context)


@login_required(login_url='auth:login')
def list_wishlist(request):
    queryset = models.WishList.objects.filter(user=request.user)
    context = {'queryset':queryset}
    return render(request, 'front/wishlist/list.html', context)


@login_required(login_url='auth:login')
def remove_wishlist(request, code):
    wishlist = models.WishList.objects.get(product__code = code, user=request.user)
    wishlist.delete()


@login_required(login_url='auth:login')
def add_wishlist(request, code):
    product = models.Product.objects.get(code=code)
    models.WishList.objects.create(product = product, user=request.user)
    return redirect('front:list_wishlist')



def add_cart(request):
    ...
