from collections import OrderedDict

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from gargoyle import models


def search_code_base(switch):
    pass


class Command(BaseCommand):
    args = '<path path ...>'
    help = 'Searches a path for dead gargoyle switches'

    def handle(self, *args, **options):
        self.stdout.write("Entering the grave yard.")

        defined_switches = OrderedDict(
                        sorted(settings.GARGOYLE_SWITCH_DEFAULTS.items(),
                        key=lambda t: t[0])
            )

        for key, value in defined_switches.items():
            try:
                switch = models.Switch.objects.get(
                    key=key,
                    status=models.GLOBAL
                )
                self.stdout.write(str(switch))
            except models.Switch.DoesNotExist:
                # Either the switch exists and is not set to global.
                #   or the switch is not in the database
                continue