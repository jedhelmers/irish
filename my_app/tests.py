from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Tags, UserQueries, populate_tags
from unittest.mock import patch

class IntegrationTests(TestCase):

    def setUp(self):
        # Create a user for testing purposes
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_populate_tags(self):
        # Ensure there are no tags before running the function
        self.assertEqual(Tags.objects.count(), 0)

        # Run the populate_tags function
        populate_tags()

        # Check if the predefined tags are added
        predefined_tags = ['travel', 'food', 'photography', 'technology', 'music', 'fitness']
        for tag_name in predefined_tags:
            self.assertTrue(Tags.objects.filter(tag=tag_name).exists())

        # If run again, the tags count should remain the same (idempotence check)
        populate_tags()
        self.assertEqual(Tags.objects.count(), len(predefined_tags))

    def test_create_user_query(self):
        # Create a user query
        query = UserQueries.objects.create(
            user=self.user,
            input_text="Hello World",
            output_text="Hello World Translated",
            pronunciation="Hel-lo Wor-ld"
        )

        # Link with a tag
        tag = Tags.objects.create(tag="test")
        query.tags.add(tag)

        # Retrieve and check values
        retrieved_query = UserQueries.objects.get(id=query.id)
        self.assertEqual(retrieved_query.user, self.user)
        self.assertEqual(retrieved_query.input_text, "Hello World")
        self.assertIn(tag, retrieved_query.tags.all())


class ViewsIntegrationTests(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('my_app.tasks.handle_translation_and_pronunciation')  # Mock the Celery task
    def test_translate_view(self, mock_task):
        mock_task.return_value = "MockedResult"
        
        # Sending a POST request
        response = self.client.post('/api/translate/', {'query': 'hello'}, content_type='application/json')
        
        # Assert the task was called
        self.assertTrue(mock_task.called)

        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertIn("Translation and pronunciation of", str(response.content))
