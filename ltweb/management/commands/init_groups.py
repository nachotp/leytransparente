from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
import time
import json

class Command(BaseCommand):
    help = 'Initializes user groups and permissions'

    def add_arguments(self, parser):
        parser.add_argument('filename',metavar='Filename', type=str,
                            help='Filename of the Group and permissions file')

    def handle(self, *args, **options):
        begin = time.time()
        filename = options['filename']
        self.stdout.write(f'Creating User Groups from {filename}')

        groups_file = open(filename)
        groups_data = json.loads(groups_file.read())
        groups_file.close()

        for group in groups_data:
            name = group['name']
            permissions = group['permissions']
            group_obj, _ = Group.objects.get_or_create(name=name)
            self.stdout.write(f'Creating group "{name}"... ', ending='')
            for perm in permissions:
                if perm != "*":
                    group_obj.permissions.add(Permission.objects.get(codename=perm))
                else:
                    group_obj.permissions.add(*list(Permission.objects.all()))

            group_obj.save()
            self.stdout.write(self.style.SUCCESS('OK'))
            self.stdout.flush()

        self.stdout.write(f'')
        self.stdout.write(self.style.SUCCESS('Successfully inserted groups to DB.'))
        self.stdout.write(f'Time elapsed: {round(time.time() - begin,2)} seconds.')