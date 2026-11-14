import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from brand.models import Brand

from .models import Car, Comment

MEDIA_ROOT = tempfile.mkdtemp()

# A 1x1 transparent GIF, enough for an ImageField.
TINY_GIF = (
    b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00'
    b'\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class CarWorldTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    @classmethod
    def make_car(cls, model, brand, quantity=3):
        return Car.objects.create(
            model=model, brand=brand, price=20000, quantity=quantity,
            image=SimpleUploadedFile(f'{model}.gif', TINY_GIF, content_type='image/gif'),
        )

    @classmethod
    def setUpTestData(cls):
        cls.toyota = Brand.objects.create(name='Toyota', slug='toyota')
        cls.bmw = Brand.objects.create(name='BMW', slug='bmw')
        cls.corolla = cls.make_car('Corolla', cls.toyota)
        cls.x5 = cls.make_car('X5', cls.bmw, quantity=1)
        cls.user = User.objects.create_user('buyer', password='pass12345!', first_name='Sam')

    def login(self):
        self.client.login(username='buyer', password='pass12345!')


class CatalogueTests(CarWorldTestCase):
    def test_home_lists_all_cars(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Corolla')
        self.assertContains(response, 'X5')
        self.assertContains(response, '2 results found')

    def test_home_empty_state(self):
        Car.objects.all().delete()
        self.assertContains(self.client.get(reverse('homepage')), 'No cars yet')

    def test_filter_by_brand(self):
        response = self.client.get(reverse('brand_wise_post', args=['bmw']))
        self.assertEqual(list(response.context['data']), [self.x5])
        self.assertEqual(response.context['selected_brand'], self.bmw)

    def test_unknown_brand_returns_404(self):
        self.assertEqual(self.client.get(reverse('brand_wise_post', args=['nope'])).status_code, 404)

    def test_brand_slug_is_generated_when_blank(self):
        first = Brand.objects.create(name='Land Rover')
        second = Brand.objects.create(name='Land Rover')
        self.assertEqual(first.slug, 'land-rover')
        self.assertEqual(second.slug, 'land-rover-2')

    def test_images_use_media_root(self):
        self.assertTrue(self.corolla.image.url.startswith('/media/cars/'))

    def test_car_details(self):
        response = self.client.get(reverse('car_details', args=[self.corolla.id]))
        self.assertContains(response, 'Remaining: 3')
        self.assertContains(response, 'No comments yet')
        self.assertContains(response, 'to buy this car')  # anonymous users see a login prompt

    def test_missing_car_returns_404(self):
        self.assertEqual(self.client.get(reverse('car_details', args=[999])).status_code, 404)


class CommentTests(CarWorldTestCase):
    def test_visitor_can_comment(self):
        url = reverse('car_details', args=[self.corolla.id])
        response = self.client.post(url, {'name': 'Ann', 'email': 'ann@example.com', 'body': 'Nice car'}, follow=True)
        self.assertRedirects(response, url)
        self.assertContains(response, 'Nice car')
        self.assertEqual(self.corolla.comments.count(), 1)

    def test_invalid_comment_shows_errors(self):
        url = reverse('car_details', args=[self.corolla.id])
        response = self.client.post(url, {'name': 'Ann', 'email': 'not-an-email', 'body': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['comment_form'].errors)
        self.assertEqual(Comment.objects.count(), 0)


class BuyTests(CarWorldTestCase):
    def test_anonymous_user_cannot_buy(self):
        url = reverse('buy_car', args=[self.corolla.id])
        response = self.client.post(url)
        self.assertRedirects(response, f"{reverse('user_login')}?next={url}")
        self.corolla.refresh_from_db()
        self.assertEqual(self.corolla.quantity, 3)

    def test_buying_with_get_is_not_allowed(self):
        self.login()
        response = self.client.get(reverse('buy_car', args=[self.corolla.id]))
        self.assertEqual(response.status_code, 405)
        self.corolla.refresh_from_db()
        self.assertEqual(self.corolla.quantity, 3)

    def test_buy_car(self):
        self.login()
        response = self.client.post(reverse('buy_car', args=[self.corolla.id]), follow=True)
        self.assertRedirects(response, reverse('car_details', args=[self.corolla.id]))
        self.assertContains(response, 'You own this car')
        self.corolla.refresh_from_db()
        self.assertEqual(self.corolla.quantity, 2)
        self.assertIn(self.user, self.corolla.buyers.all())

    def test_buying_same_car_twice_only_counts_once(self):
        self.login()
        self.client.post(reverse('buy_car', args=[self.corolla.id]))
        self.client.post(reverse('buy_car', args=[self.corolla.id]))
        self.corolla.refresh_from_db()
        self.assertEqual(self.corolla.quantity, 2)

    def test_cannot_buy_out_of_stock_car(self):
        other = User.objects.create_user('first', password='pass12345!')
        self.client.force_login(other)
        self.client.post(reverse('buy_car', args=[self.x5.id]))
        self.login()
        response = self.client.post(reverse('buy_car', args=[self.x5.id]), follow=True)
        self.assertContains(response, 'out of stock')
        self.x5.refresh_from_db()
        self.assertEqual(self.x5.quantity, 0)
        self.assertNotIn(self.user, self.x5.buyers.all())

    def test_buy_missing_car_returns_404(self):
        self.login()
        self.assertEqual(self.client.post(reverse('buy_car', args=[999])).status_code, 404)

    def test_profile_lists_bought_cars(self):
        self.login()
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'You have not bought any cars yet')
        self.client.post(reverse('buy_car', args=[self.corolla.id]))
        response = self.client.get(reverse('profile'))
        self.assertEqual(list(response.context['data']), [self.corolla])
