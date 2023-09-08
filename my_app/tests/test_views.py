import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from my_app.models import UserQueries, Tags


class TranslateViewTest(TestCase):
    def test_translate_view_post_method(self):
        url = reverse('name_of_translate_view_in_urls')
        data = {'query': 'hello'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())


class SubmitGuessTest(TestCase):    
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='johnpassword')
        self.query = UserQueries.objects.create(
            user=self.user, 
            input_text="hello",
            output_text="hola",
            pronunciation="ho-la"
        )
        self.url = reverse('name_of_submit_guess_in_urls')

    def test_submit_guess_post_method(self):
        data = {
            'guess': 'hola',
            'query_id': self.query.id
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())


class AddTagsToUserQueryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='johnpassword')
        self.query = UserQueries.objects.create(
            user=self.user, 
            input_text="hello",
            output_text="hola",
            pronunciation="ho-la"
        )
        self.tag = Tags.objects.create(tag='example')
        self.url = reverse('name_of_add_tags_to_userquery_in_urls', args=[self.query.id])

    def test_add_tags_to_userquery(self):
        data = {
            'tags': ['example']
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())
        self.query.refresh_from_db()
        self.assertTrue(self.query.tags.filter(tag='example').exists())
