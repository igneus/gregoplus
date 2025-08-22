from typing import Set

from django.core.management.base import BaseCommand

from scores.models import Chant


def known_office_part_codes() -> Set[str]:
    r: Set[str] = set()
    for _group, items in Chant.OFFICE_PART_CHOICES:
        for code, _label in items:
            r.add(code)
    return r


class Command(BaseCommand):
    help = "Reports Chant.office_part values not included in Chant.OFFICE_PART_CHOICES"

    def handle(self, *args, **options):
        distinct_values = set(Chant.objects.values_list('office_part', flat=True).distinct())
        unknown_values = sorted(distinct_values - known_office_part_codes() - {None, ''})

        if not unknown_values:
            self.stdout.write(self.style.SUCCESS("Chant.OFFICE_PART_CHOICES mapping is up to date with db contents."))
            return

        self.stderr.write("Chant.office_part value(s) missing in Chant.OFFICE_PART_CHOICES:")
        for val in unknown_values:
            self.stderr.write(f" - {val}")

        raise SystemExit(1)
