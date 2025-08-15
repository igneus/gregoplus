from json import JSONDecodeError
from unittest import TestCase

from scores.gabc import Gabc
from scores.models import Chant


class GabcTest(TestCase):
    def test_null(self):
        chant = Chant()
        with self.assertRaisesRegex(ValueError, r'must be a valid JSON'):
            Gabc(chant)

    def test_empty_but_valid(self):
        chant = Chant(gabc='""')
        gabc = Gabc(chant)
        self.assertEqual("name: ;\n%%\n", str(gabc))

    def test_all_relevant_properties(self):
        chant = Chant(
            incipit = 'Amen',
            gabc='"(c3) A(h)men.(h) (::)"',
            gabc_verses='A(g)men.(gh) (::)',
            office_part='va',
            mode='1',
            transcriber='Lampertus Insulensis',
            commentary='fortiter',
        )
        gabc = Gabc(chant)
        self.assertEqual(
            "name: Amen;\noffice-part: Varia;\nmode: 1;\ntranscriber: Lampertus Insulensis;\ncommentary: fortiter;\n%%\n(c3) A(h)men.(h) (::)\nA(g)men.(gh) (::)",
            str(gabc)
        )

    def test_json_array(self):
        chant = Chant(
            incipit='Amen',
            gabc='''[
                ["tex", "some TeX code", {}],
                ["gabc", "(c3) A(h)men.(h) (::)", {}],
                ["gabc", "A(h)men.(gh) (::)", {}]
            ]'''
        )
        gabc = Gabc(chant)
        # GregoPlus ignores everything but the first gabc item.
        self.assertEqual(
            "name: Amen;\n%%\n(c3) A(h)men.(h) (::)",
            str(gabc)
        )

    def test_json_array_no_gabc(self):
        chant = Chant(
            incipit='Amen',
            gabc='[["tex", "some TeX code", {}]]'
        )
        gabc = Gabc(chant)
        with self.assertRaisesRegex(ValueError, r'at least one item of type "gabc"'):
            str(gabc)

    def test_unsupported_type(self):
        chant = Chant(
            incipit='Amen',
            gabc='0' # JSON number
        )
        gabc = Gabc(chant)
        with self.assertRaisesRegex(ValueError, r'Unsupported JSON value type'):
            str(gabc)
