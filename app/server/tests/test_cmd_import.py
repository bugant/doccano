import os

from rest_framework.test import APITestCase
from model_mommy import mommy
from ..models import User, Document, Email, SequenceAnnotation
from ..models import SEQUENCE_LABELING
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class TestImportCommand(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.labeling_project = mommy.make('server.SequenceLabelingProject',
                                          users=[super_user], project_type=SEQUENCE_LABELING)

    def test_cmd_import(self):
        from django.core.management import call_command
        self.assertEqual(Document.objects.count(), 0)
        user = User.objects.get(email='fizz@buzz.com')
        json_file = os.path.join(DATA_DIR, 'fdsk_import_data_example.json')
        call_command(
            'cmd_import_json',
            'Email',
            '--user-id', user.pk,
            '--project-id', self.labeling_project.pk,
            '--file', json_file
        )
        self.assertEqual(Document.objects.count(), 2)
        self.assertEqual(Email.objects.count(), 2)
        self.assertEqual(SequenceAnnotation.objects.count(), 3)
