from django.test import TestCase, Client
import json
from .models import Chant, Source, ChantSource
import unittest

class ScoresTest(TestCase):
    "Test that all views load without error"

    def setUp(self):
        self._score = Chant.objects.create(
            incipit='Alleluia',
            gabc='"(c4) Al(h)le(h)lu(hh)ia(f!gaGFE) (::)"',
            office_part='va', # va = varia (codes inherited from gregobase)
        )
        self._source = Source.objects.create(
            year=2018,
            editor='igneus',
            title='Liber brevissimus',
            description='The shortest and most obscure chant edition ever',
            caption='Liber brevissimus',
            pages=1,
        )
        ChantSource.objects.create(
            chant=self._score,
            source=self._source,
            page=1,
            sequence=1,
            extent=1,
        )

    def test_index(self):
        client = Client()
        response = client.get('/scores/')
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        client = Client()
        response = client.get('/scores/{}-va-alleluia'.format(self._score.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._score.incipit)

    def test_detail__incorrect_slug(self):
        """
        URLs with incorrect/incomplete slug are redirected
        """
        client = Client()
        paths = [
            '/scores/{}',
            '/scores/{}-va',
            '/scores/{}-va-all',
            '/scores/{}-xxx',
        ]
        for p in paths:
            with self.subTest(p):
                response = client.get(p.format(self._score.id))
                self.assertEqual(response.status_code, 301)
                self.assertEqual(
                    '/scores/{}-va-alleluia'.format(self._score.id),
                    response.headers['Location']
                )

    def test_detail__empty_properties(self):
        """
        instances with empty properties used in the URL are handled correctly
        """
        empty_office_part = Chant.objects.create(
            incipit='Alleluia',
            office_part=None
        )
        empty_office_part2 = Chant.objects.create(
            incipit='Alleluia',
            office_part=''
        )
        empty_incipit = Chant.objects.create(
            incipit='',
            office_part='va'
        )
        all_empty = Chant.objects.create(
            incipit='',
            office_part=None
        )

        client = Client()
        paths = [
            (empty_office_part, '/scores/{}-alleluia'),
            (empty_office_part2, '/scores/{}-alleluia'),
            (empty_incipit, '/scores/{}-va'),
            (all_empty, '/scores/{}'),
        ]
        for chant, p in paths:
            with self.subTest(p):
                real_path = p.format(chant.id)
                self.assertEqual(real_path, chant.get_absolute_url())

                response = client.get(real_path)
                self.assertNotIn('Location', response.headers)
                self.assertEqual(response.status_code, 200)

    def test_gabc(self):
        client = Client()
        response = client.get('/scores/{}.gabc'.format(self._score.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/plain; charset=utf-8')
        self.assertIn(
            json.loads(self._score.gabc),
            str(response.content)
        )

    def test_incipit(self):
        client = Client()
        response = client.get('/scores/incipit')
        self.assertEqual(response.status_code, 200)

    def test_incipit_detail(self):
        client = Client()
        response = client.get('/scores/incipit/A')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._score.incipit)

    def test_usage(self):
        client = Client()
        response = client.get('/scores/usage')
        self.assertEqual(response.status_code, 200)

    def test_usage_detail(self):
        client = Client()
        response = client.get('/scores/usage/{}'.format(self._score.office_part))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._score.incipit)

    def test_tag(self):
        client = Client()
        response = client.get('/scores/tag')
        self.assertEqual(response.status_code, 200)

    def test_source(self):
        client = Client()
        response = client.get('/scores/source')
        self.assertEqual(response.status_code, 200)

    def test_source_detail(self):
        client = Client()
        response = client.get('/scores/source/{}'.format(self._source.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._score.incipit)
