from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order, Address

class AccountDashboardViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='admin@admin.com', password='project123')
        self.address = Address.objects.create(
            user=self.user,
            label="Home",
            address_line="123 Main Street",
            city="New York",
            state="NY",
            postal_code="10001",
            country="USA",
            is_default=True
        )
        self.order = Order.objects.create(
            user=self.user,
            order_id="ORD-123456",
            total_price=100.00,
            status="Processing"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('account:account'))
        self.assertRedirects(response, '/accounts/login/?next=/account/')

    def test_account_dashboard_status_code(self):
        self.client.login(email='admin@admin.com', password='project123')
        response = self.client.get(reverse('account:account'))
        self.assertEqual(response.status_code, 200)

    def test_account_dashboard_template_used(self):
        self.client.login(email='admin@admin.com', password='project123')
        response = self.client.get(reverse('account:account'))
        self.assertTemplateUsed(response, 'account.html')

    def test_orders_section_contains_order(self):
        self.client.login(email='admin@admin.com', password='project123')
        response = self.client.get(reverse('account:account'))
        self.assertContains(response, self.order.order_id)
        self.assertContains(response, "Processing")

    def test_address_section_contains_address(self):
        self.client.login(email='admin@admin.com', password='project123')
        response = self.client.get(reverse('account:account'))
        self.assertContains(response, "123 Main Street")
        self.assertContains(response, "New York")

    def test_dashboard_tabs_present(self):
        self.client.login(email='admin@admin.com', password='project123')
        response = self.client.get(reverse('account:account'))
        tabs = ["My Orders", "Wishlist", "Payment Methods", "My Reviews", "Addresses", "Account Settings"]
        for tab in tabs:
            self.assertContains(response, tab)

    def test_user_info_displayed(self):
        self.client.login(email='admin@admin.com', password='project123')
        response = self.client.get(reverse('account:account'))
        self.assertContains(response, "Sarah Anderson") 
        
class ShippingInfoViewTests(TestCase):

    def test_shipping_info_status_code(self):
        response = self.client.get(reverse('account:shipping'))
        self.assertEqual(response.status_code, 200)

    def test_shipping_info_template_used(self):
        response = self.client.get(reverse('account:shipping'))
        self.assertTemplateUsed(response, 'shiping-info.html')

    def test_main_title_present(self):
        response = self.client.get(reverse('account:shipping'))
        self.assertContains(response, template_name="accounts/shiping-info.html")

    def test_shipping_options_displayed(self):
        response = self.client.get(reverse('account:shipping'))
        self.assertContains(response, "Express Delivery")
        self.assertContains(response, "Standard Shipping")
        self.assertContains(response, "Local Delivery")

    def test_shipping_features_present(self):
        response = self.client.get(reverse('account:shipping'))
        self.assertContains(response, "Secure Packaging")
        self.assertContains(response, "Global Coverage")
        self.assertContains(response, "Free Returns")

    def test_international_shipping_section(self):
        response = self.client.get(reverse('account:shipping'))
        self.assertContains(response, "International Shipping")
        self.assertContains(response, "Reliable tracking system")
        self.assertContains(response, "Express worldwide delivery")

    def test_faq_section_rendered(self):
        response = self.client.get(reverse('account:shipping'))
        self.assertContains(response, "Frequently Asked Questions")
        self.assertContains(response, "When will my order arrive?")
        self.assertContains(response, "Do you ship to P.O. boxes?")
        self.assertContains(response, "What about shipping insurance?")
        self.assertContains(response, "Can I change my shipping address?")

    def test_meta_title_tag_present(self):
        response = self.client.get(reverse('account:shipping'))
        self.assertContains(response, template_name="accounts/shiping-info.html")