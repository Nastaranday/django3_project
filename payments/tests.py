from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from .models import Products,Category


class ProductDetailViewTests(TestCase):

    def setUp(self):
        self.product = Products.objects.create(
            title="Test Headphones",
            description="High quality wireless headphones",
            price=249.99,
            stock=24,
            category="Headphones"
        )

    def test_product_detail_status_code(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_template_used(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertTemplateUsed(response, 'product-details.html')

    def test_product_title_displayed(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertContains(response, "Test Headphones")

    def test_product_price_displayed(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertContains(response, "$249.99")

    def test_stock_count_displayed(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertContains(response, "(24 items left)")

    def test_review_section_exists(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertContains(response, "Customer Reviews")
        self.assertContains(response, "Write a Review")

    def test_add_to_cart_button_exists(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertContains(response, "Add to Cart")

    def test_meta_title_tag_present(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertContains(response, "<title>", html=True)


class CategoryPageTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.brand = Brand.objects.create(name="Apple")
        self.product = Products.objects.create(
            title="iPhone 14",
            price=999.99,
            stock=10,
            category=self.category,
            brand=self.brand,
        )

    def test_category_page_status_code(self):
        url = reverse('category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_page_template_used(self):
        url = reverse('category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'category.html')

    def test_category_name_displayed(self):
        url = reverse('category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertContains(response, self.category.name)

    def test_product_displayed_in_category_page(self):
        url = reverse('category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertContains(response, self.product.title)
        self.assertContains(response, f"${self.product.price}")

    def test_filters_visible(self):
        url = reverse('category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertContains(response, "Price Range")
        self.assertContains(response, "Filter by Brand")
        self.assertContains(response, "Filter by Color")

    def test_add_to_cart_button_exists(self):
        url = reverse('category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertContains(response, "Add to Cart")

    def test_search_bar_exists(self):
        url = reverse('category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertContains(response, "Search Products")

    def test_sorting_dropdown_present(self):
        url = reverse('category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertContains(response, "Sort By")
        self.assertContains(response, "Price: Low to High")

    def test_pagination_displayed(self):
        url = reverse('category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertContains(response, "Next")
        self.assertContains(response, "Previous")
        

class SearchResultsViewTests(TestCase):

    def setUp(self):
        self.product1 = Products.objects.create(
            title="Tempor Incididunt",
            price=129.00,
            rating=4.8,
            category="Women's Fashion"
        )
        self.product2 = Product.objects.create(
            title="Elit Consectetur",
            price=95.00,
            rating=4.6,
            category="Men's Collection"
        )

    def test_search_results_status_code(self):
        response = self.client.get(reverse('search') + '?q=Tempor')
        self.assertEqual(response.status_code, 200)

    def test_search_results_template_used(self):
        response = self.client.get(reverse('search') + '?q=Tempor')
        self.assertTemplateUsed(response, 'search-results.html')

    def test_search_product_is_shown(self):
        response = self.client.get(reverse('search') + '?q=Tempor')
        self.assertContains(response, "Tempor Incididunt")
        self.assertContains(response, "$129.00")

    def test_non_matching_product_not_shown(self):
        response = self.client.get(reverse('search') + '?q=Tempor')
        self.assertNotContains(response, "Elit Consectetur")

    def test_search_term_displayed(self):
        response = self.client.get(reverse('search') + '?q=Tempor')
        self.assertContains(response, 'We found')
        self.assertContains(response, 'Tempor')

    def test_filters_and_sorting_visible(self):
        response = self.client.get(reverse('search') + '?q=Tempor')
        self.assertContains(response, 'Sort by:')
        self.assertContains(response, 'Relevance')
        self.assertContains(response, 'Newest First')

    def test_product_rating_displayed(self):
        response = self.client.get(reverse('search') + '?q=Tempor')
        self.assertContains(response, '4.8')
        self.assertContains(response, 'star-fill')

    def test_pagination_displayed(self):
        response = self.client.get(reverse('search') + '?q=Tempor')
        self.assertContains(response, 'Previous')
        self.assertContains(response, 'Next')