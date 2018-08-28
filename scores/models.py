from django.db import models

class Score(models.Model):
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
            ('ps', 'Offertorium'),
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
            ('va', 'Varia'),
        ))
    )
    version = models.CharField(max_length=128)
    incipit = models.CharField(max_length=256)
    initial = models.IntegerField()
    office_part = models.CharField(
        max_length=16,
        db_column='office-part',
        choices=OFFICE_PART_CHOICES,
    )
    mode = models.CharField(max_length=8)
    gabc = models.TextField()
    gabc_verses = models.TextField()
    transcriber = models.CharField(max_length=128)
    commentary = models.CharField(max_length=256)
    class Meta:
        db_table = 'gregobase_chants'
        ordering = ('incipit',)

class Source(models.Model):
    year = models.IntegerField()
    editor = models.CharField(max_length=128)
    title = models.CharField(max_length=256)
    description = models.TextField()
    caption = models.TextField()
    pages = models.TextField()
    scores = models.ManyToManyField(Score, through='ChantSource')
    class Meta:
        db_table = 'gregobase_sources'
        ordering = ('-year', 'title')

class ChantSource(models.Model):
    chant = models.ForeignKey(Score, primary_key=True)
    source = models.ForeignKey(Source, db_column='source')
    page = models.CharField(max_length=16)
    sequence = models.IntegerField()
    extent = models.IntegerField()
    class Meta:
        db_table = 'gregobase_chant_sources'
        unique_together = (('chant', 'source', 'page'),)
        ordering = ('sequence',)
