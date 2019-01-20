from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import AboutUsModel
from .views import about_data


class AboutData(TestCase):
    def test_get_object_creating(self):
        self.assertFalse(AboutUsModel.objects.exists())
        about_data()
        self.assertTrue(AboutUsModel.objects.exists())

    def test_get_object_getting(self):
        data = AboutUsModel.objects.create(headline='h1', content='p')
        self.assertTrue(AboutUsModel.objects.exists())
        self.assertEqual(about_data(), data)

    def test_only_single_instance(self):
        about_data()
        about_data()
        about_data()
        about_data()
        self.assertTrue(AboutUsModel.objects.exists())
        self.assertEqual(len(AboutUsModel.objects.all()), 1)


class AboutUsViewTests(TestCase):
    def test_about_us_view_without_data(self):
        self.assertFalse(AboutUsModel.objects.exists())
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['about_data'])

    def test_about_us_view_with_data(self):
        data = AboutUsModel.objects.create(headline='Заголовок', content='p')
        response = self.client.get(reverse('about_us'))
        self.assertContains(response, 'Заголовок', status_code=200)
        self.assertEqual(response.context['about_data'], data)





