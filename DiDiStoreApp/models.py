from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    address = models.CharField(max_length=255,verbose_name="Адрес")
    iin = models.CharField(max_length=25,verbose_name="ИИН")
    bank_iin = models.CharField(max_length=25,blank=True,verbose_name="Банковский счёт")
    cvv_iin = models.CharField(max_length=4,blank=True,verbose_name="cvv")

    def __str__(self):
        return self.user.username


class MainCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    class Meta:
        verbose_name = "Главное Категория"
        verbose_name_plural = "Главные Категории"

    def __str__(self):
        return self.name


class Category(models.Model):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, verbose_name="Главное Категория")
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    desc = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to="author_photos/%Y/%m/%d/", verbose_name="Фото")

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"




class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    desc = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to="publisher_photos/%Y/%m/%d/", verbose_name="Фото")


    class Meta:
        verbose_name = "Издатели"
        verbose_name_plural = "Издатели"

    def __str__(self):
        return self.name

LANGS = (
    ("Руский","Руский"),
    ("Английский","Английский"),
    ("Казахский","Казахский"),
)

class Book(models.Model):
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    author = models.ForeignKey(Author,verbose_name="Автор",on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher,verbose_name="Издатель",on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Название")
    year = models.IntegerField(verbose_name="Год")
    price = models.IntegerField(verbose_name="Цена")
    lang = models.CharField(max_length=255,choices=LANGS,default="Руский")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Последний изм.")
    rating = models.IntegerField(default=5,verbose_name="rating")
    desc = models.TextField(verbose_name="Описание")


    def __str__(self):
        return self.name

    @property
    def get_name_publisher(self):
        return self.publisher.name


    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

PAYMENT_MED = (
    ("Картой","Картой"),
    ("Наличкой","Наличкой")
)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=150)
    payment_method = models.CharField(max_length = 20,choices=PAYMENT_MED)
    iin = models.CharField(max_length = 25)
    bank_iin = models.CharField(max_length=25)
    cvv_iin = models.CharField(max_length=4)
    transaction_id = models.IntegerField()
    totalbook = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
