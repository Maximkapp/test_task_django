from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad

class AdModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        Ad.objects.create(user=user, title='Тест', description='Описание', category='Книги', condition='new')

    def test_ad_created(self):
        ad = Ad.objects.get(title='Тест')
        self.assertEqual(ad.description, 'Описание')
