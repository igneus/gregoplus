from django.db import models
from django.db.models import CompositePrimaryKey
from django.urls import reverse
from django.utils.text import slugify


class Chant(models.Model):
    # see https://github.com/gregorio-project/GregoBase/blob/master/include/txt.php
    OFFICE_PART_CHOICES = (
        ('Missa', (
            ('in', 'Introitus'),
            ('ky', 'Kyriale'),
            ('gr', 'Graduale'),
            ('al', 'Alleluia'),
            ('se', 'Sequentia'),
            ('of', 'Offertorium'),
            ('pr', 'Praefationes in tono solemni'),
            ('co', 'Communio'),
            ('tr', 'Tractus'),
        )),
        ('Officium divinum', (
            ('an', 'Antiphona'),
            ('ca', 'Canticum'),
            ('hy', 'Hymnus'),
            ('rb', 'Responsorium breve'),  # "breve" is correct
            ('re', 'Responsorium'),
        )),
        ('Cetera', (
            ('or', 'Toni Communes'),
            ('im', 'Improperia'),
            ('ps', 'Psalmus'),
            ('pa', 'Prosa'),
            ('rh', 'Rhythmus'),
            ('su', 'Supplicatio'),
            ('tp', 'Tropus'),
            ('va', 'Varia'),
        ))
    )
    id = models.AutoField(primary_key=True)
    incipit = models.CharField(max_length=256)
    office_part = models.CharField(
        max_length=16,
        db_column='office-part',
        choices=OFFICE_PART_CHOICES,
        null=True,
    )
    mode = models.CharField(max_length=8, null=True)
    mode_var = models.CharField(max_length=16, null=True)
    version = models.CharField(max_length=128, null=True)
    gabc = models.TextField(null=True)
    initial = models.IntegerField(default=1)
    gabc_verses = models.TextField(null=True)
    tex_verses = models.TextField(null=True)
    cantusid = models.CharField(max_length=32, null=True)
    commentary = models.CharField(max_length=256, null=True)
    headers = models.TextField(null=True)
    transcriber = models.CharField(max_length=128, null=True)
    remarks = models.TextField(null=True)
    copyrighted = models.BooleanField(default=False)
    duplicateof = models.ForeignKey('Chant', db_column='duplicateof', null=True, on_delete=models.SET_NULL, related_name='duplicates')
    tags = models.ManyToManyField('Tag', through='ChantTag', related_name='scores')
    sources = models.ManyToManyField('Source', through='ChantSource', related_name='chants')
    class Meta:
        db_table = 'gregobase_chants'
        ordering = ('incipit',)

    def __str__(self):
        return f'#{self.id} {self.incipit} ({self.office_part}, {self.version})'

    def get_absolute_url(self):
        parts = [
            self.id,
            self.office_part,
            self.incipit_slug()
        ]
        args = '-'.join([str(p) for p in parts if p is not None and p != ''])
        return reverse('scores:detail', args=[args])

    def incipit_slug(self):
        return slugify(self.incipit)

class Source(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    year = models.IntegerField()
    editor = models.CharField(max_length=128)
    description = models.TextField()
    caption = models.TextField()
    pages = models.TextField()
    class Meta:
        db_table = 'gregobase_sources'
        ordering = ('-year', 'title')

    def __str__(self):
        return f'#{self.id} {self.title} ({self.editor} {self.year})'

    def get_absolute_url(self):
        return reverse('scores:source_detail', args=[self.id])

class ChantSource(models.Model):
    # TODO in fact this model has a composite primary key, but as of Django 5.2
    #   Django Admin doesn't support that, so we pretend to have a simple one
    chant = models.ForeignKey(Chant, primary_key=True, on_delete=models.CASCADE, related_name='chant_sources')
    source = models.ForeignKey(Source, db_column='source', on_delete=models.CASCADE, related_name='chant_sources')
    page = models.CharField(max_length=16)
    sequence = models.IntegerField()
    extent = models.IntegerField()
    class Meta:
        db_table = 'gregobase_chant_sources'
        unique_together = (('chant', 'source', 'page'),)
        ordering = ('source', 'page', 'sequence',)

class ChantWithSource:
    """
    View model exposing ChantSource data for use cases
    where API compatibility with Chant is desirable
    """

    def __init__(self, chant_source: ChantSource):
        self.chant_source = chant_source
        self.chant = chant_source.chant
        self.source = chant_source.source

    @property
    def page(self):
        return self.chant_source.page

    def __getattr__(self, item):
        return getattr(self.chant, item)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'gregobase_tags'
        ordering = ('tag',)

    def __str__(self):
        return self.tag


class ChantTag(models.Model):
    pk = CompositePrimaryKey('chant_id', 'tag_id')
    chant = models.ForeignKey(
        Chant,
        on_delete=models.CASCADE,
        db_column='chant_id',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        db_column='tag_id',
    )

    class Meta:
        db_table = 'gregobase_chant_tags'
        unique_together = (('chant', 'tag'),)
