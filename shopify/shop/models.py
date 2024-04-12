from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from mptt.models import TreeForeignKey, MPTTModel


class Category(MPTTModel):
    title = models.CharField(verbose_name='Название',
                             max_length=255, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                            related_name='children', db_index=True, verbose_name='Родительская категория')
    slug = models.SlugField(
        verbose_name='URL', max_length=255, unique=True, null=False, editable=True)
    created_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True)
    
    class MPTTMeta:
        order_instertion_by = ['title']

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products_category", kwargs={'slug': self.slug})


class Product(models.Model):
    title = models.CharField(verbose_name='Название',
                             max_length=255)
    description = models.TextField(verbose_name='Описание', blank=True)
    brand = models.CharField(verbose_name='Бренд', max_length=255)
    price = models.DecimalField(
        verbose_name='Цена', max_digits=7, decimal_places=2, default=0.00)
    category = TreeForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Категория')
    slug = models.SlugField(
        verbose_name='URL', max_length=255, unique=True, null=False, editable=True)
    created_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='Дата изменения', auto_now=True)
    image = models.ImageField(
        verbose_name='Изображение', upload_to='products/%Y/%m/%d', blank=True)
    available = models.BooleanField(verbose_name='Доступен', default=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.slug})


class ProductManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(available=True)


class ProductProxy(Product):
    objects = ProductManager()

    class Meta:
        proxy = True
