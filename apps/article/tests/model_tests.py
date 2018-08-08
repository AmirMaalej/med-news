from django.urls import reverse

from rest_framework.test import APITestCase

from tests import recipes

from apps.author import models


class ArticleModelTest(APITestCase):

    def setUp(self):
        self.url = reverse('api:article-list')
        self.user = recipes.UserRecipe.make()
        self.client.force_login(self.user)
        author = models.Author.objects.create(name='author', title='title', bio='bio')
        self.initial_data = {'title': 'article', 'body': 'article body', 'author': author.id, }

    def test_create_article(self):
        response = self.client.post(self.url, self.initial_data, format='json')
        self.assertEqual(response.data['title'], 'article')
        self.assertEqual(response.data['body'], 'article body')
        self.assertEqual(response.data['author'], 1)

    def test_create_article_author(self):
        initial_data = {
            'title': 'article',
            'body': 'article body',
            'author': {
                'name': 'author',
                'title': 'title',
                'bio': 'bio',
            },
        }
        response = self.client.post(self.url, initial_data, format='json')
        self.assertEqual(response.data['title'], 'article')
        self.assertEqual(response.data['body'], 'article body')

    def test_patch_article(self):
        response = self.client.post(self.url, self.initial_data, format='json')

        response = self.client.patch(
            reverse('api:article-detail', args=[response.data['id']]),
            dict(title='Updated'),
            format='json'
        )
        self.assertEqual(response.data['title'], 'Updated')

    def test_update_article(self):
        response = self.client.post(self.url, self.initial_data, format='json')

        updated_data = {
            'title': 'Updated',
            'body': 'article body',
            'author': 1,
        }
        response = self.client.put(
            reverse('api:article-detail', args=[response.data['id']]),
            updated_data, format='json')
        self.assertEqual(response.data['title'], 'Updated')
