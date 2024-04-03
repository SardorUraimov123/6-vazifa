from django.db import models
from django.contrib.auth.models import AbstractUser
from random import sample
import string


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True,unique=True)
    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15)) 
    
    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/',default='avatar/default.png')
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.username}'
    
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
    
    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'default.png'
        super().save(*args, **kwargs)
    

class Category(CodeGenerate):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Product(CodeGenerate):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, 
                                         blank=True, null=True)
    banner_img = models.ImageField(upload_to='banner-img/')
    quantity = models.IntegerField() 
    delivery = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'
    
    @property
    def stock_status(self):
        return bool(self.quantity)
    
class EnterProduct(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name}'

    def save(self, *args, **kwargs):
        if self.pk:

            object = EnterProduct.objects.get(id=self.id)
            self.product.quantity -= object.quantity

        self.product.quantity +=self.quantity
        self.product.save()
        
        super(EnterProduct, self).save(*args, **kwargs)

class ProductImg(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img/')

    def __str__(self):
        return f'{self.product.name}'


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    video = models.FileField(upload_to='video', blank=True, null=True)
    link = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.product.name}'


class Review(models.Model):
    mark = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str__(self):
        return f'{self.product.name}, {self.user.username}, {self.text}'

    def save(self, *args, **kwargs):
        if self.pk:
            obj = Review.objects.filter(product=self.product, user=self.user).exclude(pk=self.pk).first()
        else:
            obj = Review.objects.filter(product=self.product, user=self.user).first()
        
        if obj:
            obj.mark = self.mark
            obj.text = self.text
            obj.save() 
        else:
            super().save(*args, **kwargs)

class Cart(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    is_active = models.BooleanField(default=True)
    order_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username},{self.is_active}'

    @property
    def total(self):
        count = 0
        queryset = CartProduct.objects.filter(cart = self)
        for i in queryset:
            count +=i.count
        return count
    
    @property
    def price(self):
        count = 0
        queryset = CartProduct.objects.filter(cart = self)
        for i in queryset:
            if i.product.discount_price:
                count += i.count * i.product.discount_price
            else:
                count += i.count * i.product.price
        return count
    
    @property
    def total_price(self):
        count = 0
        queryset = CartProduct.objects.filter(cart = self)
        for i in queryset:
            count += i.count * i.product.price
        return count



class CartProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f'{self.product.name,self.count,self.cart.is_active}'

    @property
    def price(self):
        count = self.count * self.product.price
        return count
    

class WishList(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username},{self.product.name}'
    
    def save(self, *args, **kwargs):
        if WishList.objects.filter(user=self.user, product=self.product).count():
            raise ValueError('Dual')
        super(WishList, self).save(*args, **kwargs)

    def toggle_active(self):
        self.active = not self.active
        self.save()

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
# Review create ---
        
# Cart create +
# Cart list +
# Cart update + 

# Cart product list + 
# Cart product create + 
# Cart product update + 
# Cart product delete +

# Wishlist create + 
# Wishlist update - 
# Wishlist delete +
# Wishlist list + 
        
