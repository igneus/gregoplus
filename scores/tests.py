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
        response = client.get('/scores/{}'.format(self._score.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._score.incipit)

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
        response = client.get('/scores/incipit'.format(self._score.id))
        self.assertEqual(response.status_code, 200)

    def test_incipit_detail(self):
        client = Client()
        response = client.get('/scores/incipit/A'.format(self._score.id))
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

    @unittest.skip('view not implemented yet')
    def test_tag(self):
        client = Client()
        response = client.get('/scores/tag')
        self.assertEqual(response.status_code, 200)

    def test_source(self):
        client = Client()
        response = client.get('/scores/source')
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        client = Client()
        response = client.get('/scores/source/{}'.format(self._source.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._score.incipit)
