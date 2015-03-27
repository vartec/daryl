from optparse import make_option
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import yesno
from django.utils import timezone

from gargoyle import models


"""
TODO - check for orphans in database, but gargoyle might remove them
"""


class Command(BaseCommand):
    args = '<path path ...>'
    help = 'Searches a path for dead gargoyle switches'

    option_list = BaseCommand.option_list + (
        make_option('-i', '--ignore',
            dest='ignore',
            default="",
            help='Ignore a file.'),
        )

    def handle(self, *args, **options):
        try:
            path = args[0]
        except IndexError:
            path = '.'

        self.cache_modules(options['ignore'], path)

        self.results = []

        self.stdout.write("Entering the grave yard...")
        self.stdout.write("Please wait... many tombstones...")

        for key in sorted(settings.GARGOYLE_SWITCH_DEFAULTS.keys()):
            result = {
                        'key': key,
                        'record': None,
                        'count': 0,
                        'status': None,
                        'is_old': False
                }
            try:
                result['record'] = models.Switch.objects.get(
                    key=key,
                    status=models.GLOBAL
                )
            except models.Switch.DoesNotExist:
                # Either the switch exists and is not set to global.
                #   or the switch is not in the database.
                self.results.append(result)
                continue

            # List the status!
            result['status'] = result['record'].get_status_label()

            # Is the record too old?
            result['is_old'] = result['record'].date_modified < timezone.now() - timezone.timedelta(days=180)

            # Count how many times we can find the Gargoyle switch key in the code base.
            result['count'] = self.search_code_base(key)

            # TODO conditions for reporting:
            #  A. The switch at global state hasn't been modified in six months (settable?)
            #  B. The code base returns a 0
            self.results.append(result)
        self.display_results()

    def display_results(self):
        self.stdout.write('')
        self.stdout.write('Candidates for Removal')
        self.stdout.write('======================')
        self.stdout.write('Is Old?  Is Used?  Key')
        for result in self.results:
            self.stdout.write(
                '   {0}        {1}      {2}'.format(
                    self.yes_no_cap(result['is_old']),
                    self.yes_no_cap(result['count']),
                    result['key']
                )
            )

    def yes_no_cap(self, value):
        return yesno(value).upper()[0]

    def set_module(self, file_name):
        # Check if it's in the page cache
        if file_name in self.modules:
            return

        # grab it otherwise
        with open(file_name) as f:
            code = f.read()
        self.modules[file_name] = code

    def cache_modules(self, ignore, path):
        self.modules = {}
        for root, dirs, files in os.walk(path):
            for name in files:
                if name == ignore:
                    continue
                if name.endswith(".py"):
                    file_name = os.path.join(root, name)
                    self.set_module(file_name)

    def search_code_base(self, key):
        KEY = key.upper()
        count = 0

        for file_name, code in self.modules.items():
            if key in code or KEY in code:
                count += 1
        return count
