from django.urls import path
from . import views


app_name = 'front'


urlpatterns = [
    path('', views.index, name='index'),
    path('product/<str:code>/', views.product_detail, name='product_detail'),
    path('category/<str:code>/', views.product_list, name='product_list'),
    path('carts/', views.carts, name='carts'),
    path('cart/<str:code>/', views.cart_detail, name='cart_detail'),
    path('active/cart/', views.active_cart, name='active_cart'),
    path('product_delete/<int:id>/',views.product_delete, name='product_delete'),
    path('wish-list', views.list_wishlist, name='list_wishlist'),
    path('remove-wishlist/<str:code>/', views.remove_wishlist, name='remove_wishlist'),
    path('create-wishlist/<str:code>/', views.add_wishlist, name='add_wishlist'),
]