import json
import sys

from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

from ...models import Project
from ...utils import JSONPainter


class Command(createsuperuser.Command):
    help = '''Export a project as json file:
    python manage.py cmd_export_json --project-id 1 --output /tmp/o.json'''

    def add_arguments(self, parser):
        parser.add_argument('--project-id', help='id of project to attach data')
        parser.add_argument('--output', help='output file')

    def handle(self, *args, **options):
        def log(msg):
            sys.stdout.write(msg + '\n')

        try:
            project = Project.objects.get(pk=options.get('project_id'))
        except Project.DoesNotExist:
            raise CommandError('project not found')

        documents = project.documents.all()
        painter = JSONPainter()
        data = painter.paint(documents)

        json_path = options.get('output')
        with open(json_path, 'w') as fp:
            for i, item in enumerate(data):
                log(f'exporting line [{i}]')
                line_data = json.dumps(item)
                fp.write(line_data + '\n')
        log(f'exported data to {json_path}')
