from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from product.models import Product
from .models import Cart, CartItem

class CartViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='admin@admin.com', password='project123')
        self.product1 = Product.objects.create(title='Product One', price=89.99, quantity=10)
        self.product2 = Product.objects.create(title='Product Two', price=64.99, quantity=5)
        self.product3 = Product.objects.create(title='Product Three', price=49.99, qunatity=3)
      
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product3, quantity=1)

    def test_cart_page_accessible_by_logged_in_user(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertEqual(response.status_code, 200)

    def test_cart_template_used(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertTemplateUsed(response, 'cart.html')

    def test_cart_items_displayed(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertContains(response, 'Product One')
        self.assertContains(response, 'Product Two')
        self.assertContains(response, 'Product Three')

    def test_cart_quantities_displayed_correctly(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertContains(response, 'value="1"')  # برای محصول 1 و 3
        self.assertContains(response, 'value="2"')  # برای محصول 2

    def test_cart_subtotal_calculated_correctly(self):
        expected_subtotal = (89.99 * 1) + (64.99 * 2) + (49.99 * 1)
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertContains(response, f"${expected_subtotal:.2f}")

    def test_shipping_options_displayed(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertContains(response, 'Standard Delivery - $4.99')
        self.assertContains(response, 'Express Delivery - $12.99')
        self.assertContains(response, 'Free Shipping (Orders over $300)')

    def test_coupon_input_displayed(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertContains(response, 'Coupon code')

    def test_clear_and_update_buttons_exist(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertContains(response, 'Update')
        self.assertContains(response, 'Clear')

    def test_checkout_button_exists(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertContains(response, 'Proceed to Checkout')

    def test_continue_shopping_button_exists(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertContains(response, 'Continue Shopping')

    def test_remove_buttons_exist_for_each_item(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertContains(response, 'Remove', count=3)

    def test_payment_methods_icons_exist(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cartview'))
        self.assertContains(response, 'bi-credit-card-2-front')
        self.assertContains(response, 'bi-paypal')
        self.assertContains(response, 'bi-wallet2')
