from django.test import TestCase
from django.contrib.auth.models import User
from my_app.models import Tags, UserQueries


class TagsModelTest(TestCase):
    def setUp(self):
        Tags.objects.create(tag="sample_tag")

    def test_tag_creation(self):
        tag = Tags.objects.get(tag="sample_tag")
        self.assertEqual(tag.__str__(), "sample_tag")


class UserQueriesModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john', password='johnpassword')
        UserQueries.objects.create(
            user=user, 
            input_text="hello",
            output_text="hola",
            pronunciation="ho-la"
        )

    def test_query_creation(self):
        query = UserQueries.objects.get(input_text="hello")
        self.assertIsNotNone(query)

    def test_query_string_representation(self):
        query = UserQueries.objects.get(input_text="hello")
        self.assertEqual(str(query), f'Query by john at {query.creation}')

    def test_default_values(self):
        query = UserQueries.objects.get(input_text="hello")
        self.assertEqual(query.correct_answers, 0)
        self.assertEqual(query.incorrect_answers, 0)


