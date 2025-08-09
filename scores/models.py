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
    incipit = models.CharField(max_length=256)
    office_part = models.CharField(
        max_length=16,
        db_column='office-part',
        choices=OFFICE_PART_CHOICES,
    )
    mode = models.CharField(max_length=8)
    version = models.CharField(max_length=128)
    gabc = models.TextField()
    initial = models.IntegerField(default=1)
    gabc_verses = models.TextField()
    commentary = models.CharField(max_length=256)
    transcriber = models.CharField(max_length=128)
    class Meta:
        db_table = 'gregobase_chants'
        ordering = ('incipit',)

    def __str__(self):
        return f'#{self.id} {self.incipit} ({self.office_part}, {self.version})'

class Source(models.Model):
    title = models.CharField(max_length=256)
    year = models.IntegerField()
    editor = models.CharField(max_length=128)
    description = models.TextField()
    caption = models.TextField()
    pages = models.TextField()
    scores = models.ManyToManyField(Score, through='ChantSource')
    class Meta:
        db_table = 'gregobase_sources'
        ordering = ('-year', 'title')

    def __str__(self):
        return f'#{self.id} {self.title} ({self.editor} {self.year})'

class ChantSource(models.Model):
    chant = models.ForeignKey(Score, primary_key=True, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, db_column='source', on_delete=models.CASCADE)
    page = models.CharField(max_length=16)
    sequence = models.IntegerField()
    extent = models.IntegerField()
    class Meta:
        db_table = 'gregobase_chant_sources'
        unique_together = (('chant', 'source', 'page'),)
        ordering = ('source', 'page', 'sequence',)
