from django.db import models

class Score(models.Model):
    # see https://github.com/gregorio-project/GregoBase/blob/master/include/txt.php
    OFFICE_PART_CHOICES = (
        ('Mass', (
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
        ('Divine Office', (
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
    initial = models.IntegerField
    office_part = models.CharField(
        max_length=16,
        db_column='office-part',
        choices=OFFICE_PART_CHOICES,
    )
    mode = models.CharField(max_length=8)
    class Meta:
        db_table = 'gregobase_chants'
        ordering = ('incipit',)
