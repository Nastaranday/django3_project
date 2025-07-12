from django.urls import resolve, reverse
from .views import HomeView, contactus, AboutView
from django.test import TestCase , Client

class TestUrl(TestCase):
    def test_url_home(self):
        url = reverse("root:home")
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_url_contact(self):
        url = reverse("root:contact")
        self.assertEqual(resolve(url).func, contactus)

    def test_url_about(self):
        url = reverse("root:about")
        self.assertEqual(resolve(url).func.view_class, AboutView)