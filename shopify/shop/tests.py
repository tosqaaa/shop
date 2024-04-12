from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Product, Category, ProductProxy

class ProductViewTest(TestCase):
    def setUp(self):
        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )
        
        uploaded = SimpleUploadedFile('test_image.jpg', small_gif, content_type='image/jpeg')
        self.category = Category.objects.create(title='Teстовая категория', slug='test-category')
        self.product_1 = Product.objects.create(
            title='Product1', category=self.category, image=uploaded, slug='product1')
        self.product_2 = Product.objects.create(
            title='Product2', category=self.category, image=uploaded, slug='product2')
    
    def test_status_code(self):
        
        response = self.client.get(reverse('shop:products'))
        
        self.assertEqual(response.status_code, 200)
        
    def test_context_data(self):
        response = self.client.get(reverse('shop:products'))
        product_1 = ProductProxy.objects.get(id=self.product_1.id)
        product_2 = ProductProxy.objects.get(id=self.product_2.id)
        self.assertEqual(response.context['products'].count(), 2)
        self.assertEqual(list(response.context['products']), [product_1, product_2])

    def test_template_user(self):
        response = self.client.get(reverse('shop:products'))
        self.assertTemplateUsed(response, 'shop/products.html')
        
class ProductDetailViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(title='Category 1')
        self.product = Product.objects.create(
            title='Product 1', category=self.category, slug='product-1', image=uploaded)
    
    def test_status_code(self):
        response = self.client.get(
            reverse('shop:product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        
    def test_context_data(self):
        response = self.client.get(
            reverse('shop:product_detail', args=[self.product.slug]))
        self.assertEqual(response.context['product'], self.product)
        self.assertEqual(response.context['product'].slug, self.product.slug)
        
        
    def test_template_used(self):
        response = self.client.get(
            reverse('shop:product_detail', args=[self.product.slug]))
        self.assertTemplateUsed(response, 'shop/product_detail.html')
        
        
class ProductCategoryViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(
            title='Test Category', slug='test-category')
        self.product = ProductProxy.objects.create(
            title='Test Product', slug='test-product', category=self.category, image=uploaded)

    def test_status_code(self):
        response = self.client.get(
            reverse('shop:product_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse('shop:product_category', args=[self.category.slug]))
        self.assertTemplateUsed(response, 'shop/product_category.html')

    def test_context_data(self):
        response = self.client.get(
            reverse('shop:product_category', args=[self.category.slug]))
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)