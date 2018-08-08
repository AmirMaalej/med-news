from django.urls import reverse

from rest_framework.test import APITestCase

from tests import recipes

from apps.author import models


class ArticleCacheTest(APITestCase):

    def setUp(self):
        """
        WIP: testing if the second get takes the result from cache or db. does not work here yet
        works with API: I retrieve an article, then patch it in admin page then retrieve it again: result doesn't change
        => it is getting it from cache
        """
        self.url = reverse('api:article-list')
        self.user = recipes.UserRecipe.make()
        self.client.force_login(self.user)
        author = models.Author.objects.create(name='author', title='title', bio='bio')
        self.initial_data = {'title': 'article', 'body': 'article body', 'author': author.id, }

    def test_patch_article(self):
        response = self.client.post(self.url, self.initial_data, format='json')
        test = self.client.get(
            reverse('api:article-detail', args=[response.data['id']]),
            format='json'
        )
        print(test.data)
        response = self.client.patch(
            reverse('api:article-detail', args=[response.data['id']]),
            dict(title='Updated'),
            format='json'
        )
        test_two = self.client.get(
            reverse('api:article-detail', args=[response.data['id']]),
            format='json'
        )
        self.assertEqual(response.data['title'], 'Updated')
        self.assertEqual(test_two.data['title'], 'article')
