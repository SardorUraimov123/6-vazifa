from django.shortcuts import render, redirect
from main.funcs import staff_required
from main import models
from main.models import WishList, Product

@staff_required
def index(request):
    context = {}
    return render(request, 'dashboard/index.html', context)

# ---------CATEGORY-------------

@staff_required
def category_list(request):
    queryset = models.Category.objects.all()
    context = {
        'queryset':queryset
        }
    return render(request, 'dashboard/category/list.html', context)

@staff_required
def category_create(request):
    if request.method == 'POST':
        models.Category.objects.create(
            name = request.POST['name']
        )
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/category/create.html')


def category_update(request, code):
    queryset = models.Category.objects.get(code=code)
    queryset.name = request.POST['name']
    queryset.save()
    return redirect('dashboard:category_list')


def category_delete(request, code):
    queryset = models.Category.objects.get(code=code)
    queryset.delete()
    return redirect('dashboard:category_list')

# ---------PRODUCT----------------

def product_list(request):
    categories = models.Category.objects.all()
    category_code = request.GET.get('category_code')
    if category_code and category_code != '0':
        queryset = models.Product.objects.filter(category__code=category_code)
    else:
        queryset = models.Product.objects.all()
    context = {
          'queryset':queryset,
          'categories':categories,
          'category_code':category_code,
    }
    return render(request, 'dashboard/product/list.html', context)


def product_detail(request, code):
    queryset = models.Product.objects.get(code=code)
    images = models.ProductImg.objects.filter(product=queryset)
    reviews = models.Review.objects.filter(product=queryset)
    ratings = range(5,0,-1)
    videos = models.ProductVideo.objects.filter(product=queryset)
    context = {
          'queryset':queryset,
          'images':images,
          'reviews':reviews,
          'ratings':ratings,
          'videos':videos
    }
    return render(request, 'dashboard/product/detail.html', context)
    

def product_create(request):
    categorys = models.Category.objects.all()
    context = {'categorys':categorys}
    if request.method == 'POST':
        delivery = True if request.POST.get('delivery') else False
        product = models.Product.objects.create(
            category_id = request.POST.get('category_id'),
            name = request.POST.get('name'),
            body = request.POST.get('body'),
            price = request.POST.get('price'),
            banner_img = request.FILES.get('banner_img'),
            quantity = request.POST.get('quantity'),
            delivery = delivery
        )
    if request.FILES.getlist('product_img'):
        for img in request.FILES.getlist('product_img'):
            models.ProductImg.objects.create(
                product = product,
                img = img
        )
    if request.FILES.getlist('product_video'):
        for video in request.FILES.getlist('product_video'):
            models.ProductVideo.objects.create(
                product = product,
                video = video
        )
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/create.html', context)


def product_update(request, code):

    images = models.ProductImg.objects.filter(product__code=code)
    videos = models.ProductVideo.objects.filter(product__code=code)
    categories = models.Category.objects.all()
    product = models.Product.objects.get(code=code)

    if request.method == 'POST':
        if request.FILES.get('banner_img'):
            product.banner_img = request.FILES.get('banner_img')
        delivery = True if request.POST.get('delivery') else False
        product.category_id = request.POST.get('category_id')
        product.name = request.POST.get('name')
        product.body = request.POST.get('body')
        product.price = request.POST.get('price')
        product.delivery = delivery
        product.save()
    
    if request.FILES.getlist('product_img'):
        for img in request.FILES.getlist('product_img'):
            models.ProductImg.objects.create(
                product = product,
                img = img
        )
    if request.FILES.getlist('product_video'):
        for video in request.FILES.getlist('product_video'):
            models.ProductVideo.objects.create(
                product = product,
                video = video
        )
        return redirect('dashboard:product_update',product.code)
    
    context = {
          'images':images,
          'videos':videos,
          'categories':categories,
          'product':product

    }
    return render(request,'dashboard/product/update.html',context=context)


def product_delete(request, code):
    product = models.Product.objects.get(code=code)
    product.delete()
    return redirect('dashboard:product_list')


def product_img_delete(request, id):
    product_img = models.ProductImg.objects.get(id=id)
    product_img.delete()
    return redirect('dashboard:product_update',product_img.product_id)


def product_video_delete(request, id):
    product_video = models.ProductVideo.objects.get(id=id)
    product_video.delete()
    return redirect('dashboard:product_update',product_video.product_id)


def product_enter(request):
    if request.method == 'POST':
        product = models.Product.objects.get(code=request.POST['code'])
        quantity = request.POST['quantity']
        models.EnterProduct.objects.create(
            product=product,
            quantity=quantity
        )
        return redirect()
    return render(request, 'dashboard/product/enter.html')


def list_product_enter(request):
    queryset = models.EnterProduct.objects.all()
    ...


def detail_product_enter(request, code):
    queryset = models.EnterProduct.objects.filter(product__code=code)
    ...


def product_history(request, code):
    queryset = models.EnterProduct.objects.filter(product__code=code)
    outs = models.CartProduct.objects.filter(product__code=code, cart__is_active=False)
    result = queryset.union(outs)
    
def wishlist_toggle(request, product_id):
    user = request.user
    product = Product.objects.get(pk=product_id)

    try:
        wishlist_item = WishList.objects.get(user=user, product=product)
        wishlist_item.toggle_active()
    except WishList.DoesNotExist:
        WishList.objects.create(user=user, product=product)

    return redirect('wishlist-list-page')


"""
kirim ...
kirim ...
chiqiim ...
kirim ...
chiqim ...


"""