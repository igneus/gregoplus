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
    help = "Reports Chant property values not covered by the corresponding `choices` mapping"

    def handle(self, *args, **options):
        data = (
            ('office_part', known_office_part_codes()),
            ('mode', {m[0] for m in Chant.MODE_CHOICES}),
        )

        success = True
        for prop, known_values in data:
            success = success and self._check(prop, known_values)

        if not success:
            raise SystemExit(1)

    def _check(self, prop: str, known_values: Set[str]) -> bool:
        distinct_values = set(Chant.objects.values_list(prop, flat=True).distinct())
        unknown_values = sorted(distinct_values - known_values - {None, ''})

        if not unknown_values:
            self.stdout.write(self.style.SUCCESS(f"Chant.{prop} choices mapping is up to date with db contents."))
            return True

        self.stderr.write(f"Chant.{prop} value(s) missing in the choices mapping:")
        for val in unknown_values:
            self.stderr.write(f" - {val}")

        return False
