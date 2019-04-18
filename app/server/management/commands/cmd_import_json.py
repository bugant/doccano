import json
import pathlib

from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

from ...models import Project, User


class Command(createsuperuser.Command):
    help = '''Import a json file: 
    python manage.py cmd_import_json Email --user-id 1 --project-id 1 --file ~/Downloads/test.json'''

    def add_arguments(self, parser):
        parser.add_argument('resource-type')
        parser.add_argument('--file', help='path to your json file')
        parser.add_argument('--project-id', help='id of project to attach data')
        parser.add_argument('--user-id', help='id of user to use')

    def handle(self, *args, **options):
        json_path = pathlib.Path(options.get('file'))
        if not json_path.exists():
            raise CommandError('--file should be a json file path')

        try:
            project = Project.objects.get(pk=options.get('project_id'))
        except Project.DoesNotExist:
            raise CommandError('project not found')

        try:
            user = User.objects.get(pk=options.get('user_id'))
        except User.DoesNotExist:
            raise CommandError('project not found')

        data = []
        with json_path.open('r') as fp:
            for line in fp.readlines():
                data.append([json.loads(line)])
        storage = project.get_storage(data)
        storage.save(user)

