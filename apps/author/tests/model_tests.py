from django.urls import reverse

from rest_framework.test import APITestCase

from tests import recipes


class AuthorModelTest(APITestCase):

    def setUp(self):
        self.url = reverse('api:author-list')
        self.user = recipes.UserRecipe.make()
        self.client.force_login(self.user)
        self.initial_data = {'name': 'author', 'title': 'author title', 'bio': 'author bio', }

    def test_create_author(self):
        response = self.client.post(self.url, self.initial_data, format='json')
        self.assertEqual(response.data['name'], 'author')
        self.assertEqual(response.data['title'], 'author title')
        self.assertEqual(response.data['bio'], 'author bio')

    def test_patch_author(self):
        response = self.client.post(self.url, self.initial_data, format='json')

        response = self.client.patch(
            reverse('api:author-detail', args=[response.data['id']]),
            dict(name='Updated'),
            format='json'
        )
        self.assertEqual(response.data['name'], 'Updated')

    def test_update_author(self):
        response = self.client.post(self.url, self.initial_data, format='json')

        updated_data = {
            'name': 'Updated',
            'title': 'author title updated',
            'bio': 'bio updated',
        }
        response = self.client.put(
            reverse('api:author-detail', args=[response.data['id']]),
            updated_data, format='json')
        self.assertEqual(response.data['name'], 'Updated')
        self.assertEqual(response.data['title'], 'author title updated')
        self.assertEqual(response.data['bio'], 'bio updated')